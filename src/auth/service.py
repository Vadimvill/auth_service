# service.py
from sqlalchemy import UUID
from src.auth.dals import RoleDAL, UserDAL, PermissionDAL


class UserService:
    def __init__(self, user_dal: UserDAL):
        self.user_dal = user_dal

    async def create_user(
            self, **kwargs
    ):
        if user := await self.user_dal.create_user(**kwargs):
            return user
        raise ValueError('User Not Created')

    async def get_user(self, user_id: UUID):
        if user := await self.user_dal.get_user_by_id(user_id):
            return user
        raise ValueError('User Not Found')

    async def update_user(
            self, user_id: UUID, **kwargs
    ):
        if user := await self.user_dal.update_user(user_id, **kwargs):
            return user
        raise ValueError('User Not Updated')

    async def soft_delete(self, user_id: UUID):
        if user := await self.user_dal.soft_delete_user(user_id):
            return user
        raise ValueError('User Not Deleted')


class RoleService:
    def __init__(self, role_dal: RoleDAL):
        self.role_dal = role_dal

    async def get_role_id(self, role_name: str):
        if role_id := await self.role_dal.get_role_id_by_name(role_name):
            return role_id
        raise ValueError('Role Not Found')

    async def get_role_by_name(self, role_name: str):
        if role := await self.role_dal.get_role_by_name(role_name):
            return role
        raise ValueError('Role Not Found')

    async def add_role_by_name(self, role_name: str):
        if role := await self.role_dal.create_role(role_name):
            return role
        raise ValueError('Role Not Created')

    async def assign_role_to_user(self, role_id, user_id):
        if user := await self.role_dal.assign_role_to_user(user_id, role_id):
            return user
        raise ValueError('Role Not Assigned')


class PermissionService:
    def __init__(self, permission_dal: PermissionDAL):
        self.permission_dal = permission_dal

    async def create_permission(self, name):
        if permission := await self.permission_dal.create_permission(name):
            return permission
        raise ValueError('Permission Not Created')

    async def check_role_has_permission(self, role_id, permission_id):
        if role_permission := await self.permission_dal.check_role_has_permission(role_id, permission_id):
            return role_permission
        raise ValueError('Forbidden')

    async def remove_permission_from_role(self, role_id, permission_id):
        if permission := await self.permission_dal.remove_permission_from_role(role_id, permission_id):
            return permission
        raise ValueError('Permission Not Deleted')

    async def add_permission_to_role(self, role_id, permission_id):
        if permission := await self.permission_dal.add_permission_to_role(role_id, permission_id):
            return permission
        raise ValueError('Permission Not Added')

    async def get_permission_id_by_name(self, name):
        if permission_id := await self.permission_dal.get_permission_id_by_name(name):
            return permission_id
        raise ValueError('Permission Not Found')
