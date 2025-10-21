from sqlalchemy import UUID
from src.auth.dals import RoleDAL, UserDAL, PermissionDAL, RedisDAL


class UserService:
    def __init__(self, user_dal: UserDAL):
        self.user_dal = user_dal

    async def create_user(self, **kwargs):
        if user := await self.user_dal.create_user(**kwargs):
            return user
        raise RuntimeError('User Not Created')

    async def get_user_by_id(self, user_id: UUID):
        if user := await self.user_dal.get_user_by_id(user_id):
            return user
        raise LookupError('User Not Found')

    async def get_user_by_email(self, email: str):
        if user := await self.user_dal.get_user_by_email(email):
            return user
        raise LookupError('User Not Found')

    async def update_user(self, user_id: UUID, **kwargs):
        if user := await self.user_dal.update_user(user_id, **kwargs):
            return user
        raise RuntimeError('User Not Updated')

    async def soft_delete(self, user_id: UUID):
        if user := await self.user_dal.soft_delete_user(user_id):
            return user
        raise RuntimeError('User Not Deleted')


class RoleService:
    def __init__(self, role_dal: RoleDAL):
        self.role_dal = role_dal

    async def get_role_id(self, role_name: str):
        if role_id := await self.role_dal.get_role_id_by_name(role_name):
            return role_id
        raise LookupError('Role Not Found')

    async def get_role_by_name(self, role_name: str):
        if role := await self.role_dal.get_role_by_name(role_name):
            return role
        raise LookupError('Role Not Found')

    async def add_role_by_name(self, role_name: str):
        if role := await self.role_dal.create_role(role_name):
            return role
        raise RuntimeError('Role Not Created')

    async def assign_role_to_user(self, role_id, user_id):
        if user := await self.role_dal.assign_role_to_user(user_id, role_id):
            return user
        raise RuntimeError('Role Not Assigned')

    async def delete_role(self, role_id):
        if role := await self.role_dal.delete_role(role_id):
            return role
        raise RuntimeError('Role Not Deleted')

    async def update_role(self, role_id, name):
        if role := await self.role_dal.update_role(role_id, name):
            return role
        raise RuntimeError('Role Not Updated')


class PermissionService:
    def __init__(self, permission_dal: PermissionDAL):
        self.permission_dal = permission_dal

    async def create_permission(self, name):
        if permission := await self.permission_dal.create_permission(name):
            return permission
        raise RuntimeError('Permission Not Created')

    async def check_role_has_permission(self, role_id, permission_id):
        if role_permission := await self.permission_dal.check_role_has_permission(role_id, permission_id):
            return role_permission
        raise PermissionError('Forbidden')

    async def remove_permission_from_role(self, role_id, permission_id):
        if permission := await self.permission_dal.remove_permission_from_role(role_id, permission_id):
            return permission
        raise RuntimeError('Permission Not Deleted')

    async def add_permission_to_role(self, role_id, permission_id):
        if permission := await self.permission_dal.add_permission_to_role(role_id, permission_id):
            return permission
        raise RuntimeError('Permission Not Added')

    async def get_permission_id_by_name(self, name):
        if permission_id := await self.permission_dal.get_permission_id_by_name(name):
            return permission_id
        raise LookupError('Permission Not Found')

    async def get_permissions_by_role(self, role_id):
        if permissions := await self.permission_dal.get_permissions_by_role(role_id):
            return permissions
        raise LookupError('Permission Not Found')

    async def delete_permission(self, permission_id):
        if permissions := await self.permission_dal.delete_permission(permission_id):
            return permissions
        raise RuntimeError('Permission Not Deleted')

    async def update_permission(self, permission_id, name):
        if permissions := await self.permission_dal.update_permission(permission_id, name):
            return permissions
        raise RuntimeError('Permission Not Updated')


class RedisService:
    def __init__(self, redis_dal: RedisDAL):
        self.redis_dal = redis_dal

    async def set_key(self, key: str, value: str, expire_seconds: int = None):
        key = str(key)
        await self.redis_dal.set_key(key, value, expire_seconds)

    async def get_key(self, key: str):
        key = str(key)
        if key := await self.redis_dal.get_key(key):
            return key

    async def delete_key(self, key: str):
        key = str(key)
        if key := await self.redis_dal.delete_key(key):
            return key

    async def key_exists(self, key: str) -> bool:
        return await self.redis_dal.key_exists(key)