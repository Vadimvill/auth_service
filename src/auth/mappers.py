from uuid import UUID

from src.auth.schemas import UserCreate, UserResponse, UserUpdate


class UserMapper:
    @staticmethod
    def to_entity(user_create: UserCreate, role_id: UUID, hashed_password: str) -> dict:
        return {
            'full_name': user_create.full_name,
            'email': user_create.email,
            'user_role_id': role_id,
            'password_hash': hashed_password
        }

    @staticmethod
    def to_response(user_entity) -> UserResponse:
        return UserResponse.model_validate(user_entity)


class UserUpdateMapper:
    @staticmethod
    def to_entity(user_update: UserUpdate) -> dict:
        return {
            'full_name': user_update.full_name,
            'email': user_update.email,
        }

    @staticmethod
    def to_response(user_entity) -> UserResponse:
        return UserResponse.model_validate(user_entity)


class PayloadMapper:
    @staticmethod
    def to_entity(email, user_role_id, user_id, permissions) -> dict:
        permissions_lst = []
        for item in permissions:
            permissions_lst.append(item.name)
        return {
            'email': email,
            'user_id': user_id,
            'user_role_id': user_role_id,
            'permissions': permissions_lst
        }
