from fastapi import Depends, HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from src.auth.dals import UserDAL, RoleDAL, PermissionDAL, RedisDAL
from src.auth.db import get_db_session, get_redis_connection
from src.auth.mappers import UserMapper, PayloadMapper, UserUpdateMapper
from src.auth.service import UserService, RoleService, PermissionService, RedisService
from src.auth.use_cases import UserUseCases, RoleCases, PermissionCases, AuthCases
from src.auth.utils import PasswordHasher, JWT


class UnitOfWork:
    def __init__(self, session: AsyncSession, rd):
        self.session = session
        self._users = UserDAL(session)
        self._redis = RedisDAL(rd)
        self._roles = RoleDAL(session)
        self._permissions = PermissionDAL(session)
        self.user_service = UserService(self._users)
        self.role_service = RoleService(self._roles)
        self.permission_service = PermissionService(self._permissions)
        self.user_mapper = UserMapper
        self.password_hasher = PasswordHasher()
        self.payload_mapper = PayloadMapper()
        self.redis_service = RedisService(self._redis)
        self.user_update_mapper = UserUpdateMapper()


async def get_uow(db: AsyncSession = Depends(get_db_session), rd: Redis = Depends(get_redis_connection)) -> UnitOfWork:
    return UnitOfWork(db, rd)


async def get_user_use_case(uow: UnitOfWork = Depends(get_uow)) -> UserUseCases:
    return UserUseCases(uow.user_service, uow.role_service, uow.permission_service, uow.password_hasher,
                        uow.user_mapper, JWT(), uow.payload_mapper, uow.redis_service, uow.session,
                        uow.user_update_mapper)


async def get_role_use_case(uow: UnitOfWork = Depends(get_uow)) -> RoleCases:
    return RoleCases(uow.role_service, uow.session)


async def get_permission_use_case(uow: UnitOfWork = Depends(get_uow)) -> PermissionCases:
    return PermissionCases(uow.role_service, uow.permission_service, uow.session)


async def get_auth_use_case(uow: UnitOfWork = Depends(get_uow)) -> AuthCases:
    return AuthCases(uow.user_service, uow.permission_service, uow.password_hasher,
                     uow.user_mapper, JWT(), uow.payload_mapper, uow.redis_service, uow.session)


def check_permission(required_permission: str):
    async def dependency(request: Request):
        if not hasattr(request.state, 'user'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        user_data = request.state.user
        permissions = user_data.get('permissions', [])

        if required_permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{required_permission}' required"
            )

        return user_data

    return dependency


async def get_refresh_token(request: Request):
    if refresh_token := request.cookies.get("refresh_token"):
        return refresh_token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not refresh token"
    )
