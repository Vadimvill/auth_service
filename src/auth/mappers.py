from uuid import UUID

from src.auth.schemas import UserCreate, UserResponse, PermissionRoleResponse


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
