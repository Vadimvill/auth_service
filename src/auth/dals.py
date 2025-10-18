# dals.py
from sqlalchemy import select

from src.auth.models import User, Role, Permission, role_permissions


class UserDAL:
    def __init__(self, session):
        self.session = session

    async def get_user_by_id(self, user_id):
        return await self.session.get(User, user_id)

    async def create_user(self, **kwargs):
        user = User(**kwargs)
        self.session.add(user)
        await self.session.flush()
        return user

    async def soft_delete_user(self, user_id):
        user = await self.session.get(User, user_id)
        if user:
            user.is_active = False
            await self.session.flush()
            return user

    async def update_user(self, user_id, **kwargs):
        user = await self.session.get(User, user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            await self.session.flush()
            return user


class RoleDAL:
    def __init__(self, session):
        self.session = session

    async def get_role_id_by_name(self, name):
        stmt = select(Role).where(Role.name == name)
        result = await self.session.execute(stmt)
        role = result.scalar_one_or_none()
        return role.role_id if role else None

    async def get_role_by_id(self, role_id):
        return await self.session.get(Role, role_id)

    async def get_role_by_name(self, name):
        stmt = select(Role).where(Role.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_role(self, name):
        role = Role(name=name)
        self.session.add(role)
        await self.session.flush()
        return role

    async def delete_role(self, role_id):
        role = await self.session.get(Role, role_id)
        if role:
            await self.session.delete(role)
            await self.session.flush()
            return True
        return False

    async def update_role(self, role_id, name):
        role = await self.session.get(Role, role_id)
        if role:
            role.name = name
            await self.session.flush()
            return role
        return None

    async def get_all_roles(self):
        stmt = select(Role)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def assign_role_to_user(self, user_id, role_id):
        user = await self.session.get(User, user_id)
        if user:
            user.user_role_id = role_id
            await self.session.flush()
            return user
        return None

    async def get_user_role(self, user_id):
        user = await self.session.get(User, user_id)
        if user and user.user_role_id:
            return await self.session.get(Role, user.user_role_id)
        return None


class PermissionDAL:
    def __init__(self, session):
        self.session = session

    async def get_permission_by_id(self, permission_id):
        return await self.session.get(Permission, permission_id)

    async def get_permission_by_name(self, name):
        stmt = select(Permission).where(Permission.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_permission_id_by_name(self, name):
        permission = await self.get_permission_by_name(name)
        return permission.permission_id if permission else None

    async def create_permission(self, name):
        permission = Permission(name=name)
        self.session.add(permission)
        await self.session.flush()
        return permission

    async def delete_permission(self, permission_id):
        permission = await self.session.get(Permission, permission_id)
        if permission:
            await self.session.delete(permission)
            await self.session.flush()
            return permission

    async def update_permission(self, permission_id, name):
        permission = await self.session.get(Permission, permission_id)
        if permission:
            permission.name = name
            await self.session.flush()
            return permission

    async def get_all_permissions(self):
        stmt = select(Permission)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_permissions_by_role(self, role_id):
        stmt = (
            select(Permission)
            .join(role_permissions, Permission.permission_id == role_permissions.c.permission_id)
            .where(role_permissions.c.role_id == role_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_permission_to_role(self, role_id, permission_id):
        stmt = select(role_permissions).where(
            role_permissions.c.role_id == role_id,
            role_permissions.c.permission_id == permission_id
        )
        result = await self.session.execute(stmt)
        existing = result.first()

        if not existing:
            stmt = role_permissions.insert().values(
                role_id=role_id,
                permission_id=permission_id
            )
            await self.session.execute(stmt)
            await self.session.flush()
            return permission_id, role_id
        return permission_id, role_id

    async def remove_permission_from_role(self, role_id, permission_id):
        stmt = role_permissions.delete().where(
            role_permissions.c.role_id == role_id,
            role_permissions.c.permission_id == permission_id
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result

    async def check_role_has_permission(self, role_id, permission_id):
        stmt = select(role_permissions).where(
            role_permissions.c.role_id == role_id,
            role_permissions.c.permission_id == permission_id
        )
        result = await self.session.execute(stmt)
        return result.first() is not None

    async def get_roles_by_permission(self, permission_id):
        stmt = (
            select(Role)
            .join(role_permissions, Role.role_id == role_permissions.c.role_id)
            .where(role_permissions.c.permission_id == permission_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
