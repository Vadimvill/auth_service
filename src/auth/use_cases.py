import secrets

from fastapi import HTTPException
from starlette import status

from src.auth.schemas import UserCreate, RoleCreate, RoleResponse, PermissionCreate, PermissionResponse, \
    AddPermissionToRole, Login, UserUpdate, DeletePermissionFromRole, DeletePermission, UpdatePermission, DeleteRole, \
    UpdateRole
from src.config import settings


class UserUseCases:
    def __init__(self, user_service, role_service, permission_service, password_hasher, user_mapper, jwt,
                 payload_mapper, redis_service, session, user_update_mapper):
        self.user_service = user_service
        self.permission_service = permission_service
        self.role_service = role_service
        self.redis_service = redis_service
        self.session = session
        self.password_hasher = password_hasher
        self.user_mapper = user_mapper
        self.jwt = jwt
        self.payload_mapper = payload_mapper
        self.user_update_mapper = user_update_mapper

    async def create_user(self, user_create: UserCreate):
        async with self.session.begin():
            role = await self.role_service.get_role_by_name(user_create.user_role)

            hashed_password = self.password_hasher.hash(user_create.password)

            self.password_hasher.verify(user_create.password_repeat, hashed_password)

            user_data = self.user_mapper.to_entity(user_create, role.role_id, hashed_password)

            user_entity = await self.user_service.create_user(**user_data)

            return self.user_mapper.to_response(user_entity)

    async def update_user(self, payload, user_update: UserUpdate):
        async with self.session.begin():
            user_data = self.user_update_mapper.to_entity(user_update)

            user_entity = await self.user_service.update_user(payload['user_id'], **user_data)

            return self.user_mapper.to_response(user_entity)

    async def delete_user(self, payload):
        async with self.session.begin():
            user_entity = await self.user_service.soft_delete(payload['user_id'])
            self.redis_service.delete_key(payload['user_id'])
            return self.user_mapper.to_response(user_entity)


class AuthCases:
    def __init__(self, user_service, permission_service, password_hasher, user_mapper, jwt,
                 payload_mapper, redis_service, session):
        self.user_service = user_service
        self.permission_service = permission_service
        self.redis_service = redis_service
        self.session = session
        self.password_hasher = password_hasher
        self.user_mapper = user_mapper
        self.jwt = jwt
        self.payload_mapper = payload_mapper

    async def login(self, login: Login):
        async with self.session.begin():
            user = await self.user_service.get_user_by_email(login.email)

            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is deactivated"
                )

            self.password_hasher.verify(login.password, user.password_hash)

            permissions = await self.permission_service.get_permissions_by_role(user.user_role_id)
            user_data = self.payload_mapper.to_entity(login.email, user.user_role_id, user.user_id, permissions)

            access_token = self.jwt.create_access_token(user_data)

            refresh_token = secrets.token_urlsafe(32)

            await self.redis_service.set_key(
                f"refresh_token:{refresh_token}",
                str(user.user_id),
                settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
            )

            await self.redis_service.set_key(
                f"user_refresh_tokens:{user.user_id}",
                refresh_token,
                settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
            )

            return access_token, refresh_token

    async def refresh_token(self, refresh_token: str):
        user_id = await self.redis_service.get_key(f"refresh_token:{refresh_token}")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        async with self.session.begin():
            user = await self.user_service.get_user_by_id(user_id)

            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is deactivated"
                )

            permissions = await self.permission_service.get_permissions_by_role(user.user_role_id)
            user_data = self.payload_mapper.to_entity(
                user.email,
                user.user_role_id,
                user.user_id,
                permissions
            )

            access_token = self.jwt.create_access_token(user_data)

            return access_token

    async def logout(self, payload):
        async with self.session.begin():
            await self.redis_service.delete_key(payload['user_id'])
            refresh_token_key = await self.redis_service.get_key(f"user_refresh_tokens:{payload['user_id']}")
            await self.redis_service.delete_key(refresh_token_key)
            await self.redis_service.delete_key(f"user_refresh_tokens:{payload['user_id']}")


class RoleCases:
    def __init__(self, role_service, session):
        self.role_service = role_service
        self.session = session

    async def create_role(self, role_create: RoleCreate):
        async with self.session.begin():
            orm_response = await self.role_service.add_role_by_name(role_create.name)
            return RoleResponse.model_validate(orm_response)

    async def delete_role(self, delete_role: DeleteRole):
        async with self.session.begin():
            role_id = await self.role_service.get_role_id(delete_role.role_name)
            orm_response = await self.role_service.delete_role(
                role_id)
            return orm_response

    async def update_role(self, update_role: UpdateRole):
        async with self.session.begin():
            role_id = await self.role_service.get_role_id(update_role.role_name)
            orm_response = await self.role_service.update_role(
                role_id, update_role.new_name)
            return orm_response


class PermissionCases:
    def __init__(self, role_service, permission_service, session):
        self.permission_service = permission_service
        self.role_service = role_service
        self.session = session

    async def create_permission(self, permission_create: PermissionCreate):
        async with self.session.begin():
            orm_response = await self.permission_service.create_permission(permission_create.name)
            return PermissionResponse.model_validate(orm_response)

    async def add_permission_to_role(self, add_permission_to_role: AddPermissionToRole):
        async with self.session.begin():
            role_id = await self.role_service.get_role_id(add_permission_to_role.role_name)
            permission_id = await self.permission_service.get_permission_id_by_name(
                add_permission_to_role.permission_name)
            orm_response = await self.permission_service.add_permission_to_role(role_id, permission_id)
            return orm_response

    async def remove_permission_from_role(self, delete_perm_from_role: DeletePermissionFromRole):
        async with self.session.begin():
            role_id = await self.role_service.get_role_id(delete_perm_from_role.role_name)
            permission_id = await self.permission_service.get_permission_id_by_name(
                delete_perm_from_role.permission_name)
            orm_response = await self.permission_service.remove_permission_from_role(role_id, permission_id)
            return orm_response

    async def delete_permission(self, delete_perm: DeletePermission):
        async with self.session.begin():
            permission_id = await self.permission_service.get_permission_id_by_name(
                delete_perm.permission_name)
            orm_response = await self.permission_service.delete_permission(permission_id)
            return orm_response

    async def update_permission(self, update_perm: UpdatePermission):
        async with self.session.begin():
            permission_id = await self.permission_service.get_permission_id_by_name(
                update_perm.permission_name)
            orm_response = await self.permission_service.update_permission(permission_id, update_perm.new_name)
            return orm_response
