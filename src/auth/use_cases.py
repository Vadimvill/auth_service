from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt

from src.auth.schemas import UserCreate, UserResponse, RoleCreate, RoleResponse, PermissionCreate, PermissionResponse, \
    AddPermissionToRole, PermissionRoleResponse


class UserUseCases:
    def __init__(self, user_service, role_service, permission_service, password_hasher, user_mapper, session):
        self.user_service = user_service
        self.permission_service = permission_service
        self.role_service = role_service
        self.session = session
        self.password_hasher = password_hasher
        self.user_mapper = user_mapper

    async def create_user(self, user_create: UserCreate):
        async with self.session.begin():
            role = await self.role_service.get_role_by_name(user_create.user_role)

            hashed_password = self.password_hasher.hash(user_create.password)

            self.password_hasher.verify(user_create.password_repeat, hashed_password)

            user_data = self.user_mapper.to_entity(user_create, role.role_id, hashed_password)

            user_entity = await self.user_service.create_user(**user_data)

            return self.user_mapper.to_response(user_entity)

    async def create_role(self, role_create: RoleCreate):
        async with self.session.begin():
            orm_response = await self.role_service.add_role_by_name(role_create.name)
            return RoleResponse.model_validate(orm_response)

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
