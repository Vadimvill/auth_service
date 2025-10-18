# unit_of_work.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dals import UserDAL, RoleDAL, PermissionDAL
from src.auth.db import get_db_session
from src.auth.mappers import UserMapper
from src.auth.service import UserService, RoleService, PermissionService
from src.auth.use_cases import UserUseCases
from src.auth.utils import PasswordHasher


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._users = UserDAL(session)
        self._roles = RoleDAL(session)
        self._permissions = PermissionDAL(session)
        self.user_service = UserService(self._users)
        self.role_service = RoleService(self._roles)
        self.permission_service = PermissionService(self._permissions)
        self.user_mapper = UserMapper
        self.password_hasher = PasswordHasher()


# dependencies.py
async def get_uow(db: AsyncSession = Depends(get_db_session)) -> UnitOfWork:
    return UnitOfWork(db)


async def get_user_use_case(uow: UnitOfWork = Depends(get_uow)) -> UserUseCases:
    return UserUseCases(uow.user_service, uow.role_service, uow.permission_service, uow.password_hasher,
                        uow.user_mapper, uow.session)
