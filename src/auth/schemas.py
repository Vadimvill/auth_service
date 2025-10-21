import re

from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from uuid import UUID


class Login(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    full_name: str
    email: str
    user_role: str

    @field_validator('full_name')
    def validate_full_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Full name cannot be empty or just whitespace.')

        words = v.split()
        if len(words) != 3:
            raise ValueError('Full name must contain exactly 3 words.')

        for word in words:
            if not word.isalpha():
                if re.search(r'\d', word):
                    raise ValueError(f'Full name cannot contain numbers. Found: "{word}"')
                else:
                    raise ValueError(f'Full name can only contain letters. Found: "{word}"')

        formatted_name = ' '.join(word.capitalize() for word in words)
        return formatted_name

    @field_validator('email')
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email address.')
        return v.lower()


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    password_repeat: str
    user_role: str

    @field_validator('full_name')
    def validate_full_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Full name cannot be empty or just whitespace.')

        words = v.split()
        if len(words) != 3:
            raise ValueError('Full name must contain exactly 3 words.')

        for word in words:
            if not word.isalpha():
                if re.search(r'\d', word):
                    raise ValueError(f'Full name cannot contain numbers. Found: "{word}"')
                else:
                    raise ValueError(f'Full name can only contain letters. Found: "{word}"')

        formatted_name = ' '.join(word.capitalize() for word in words)
        return formatted_name

    @field_validator('email')
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email address.')
        return v.lower()

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        return v

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match.')
        return self


class RoleCreate(BaseModel):
    name: str


class RoleResponse(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class PermissionCreate(BaseModel):
    name: str


class AddPermissionToRole(BaseModel):
    permission_name: str
    role_name: str


class DeletePermissionFromRole(BaseModel):
    permission_name: str
    role_name: str


class DeletePermission(BaseModel):
    permission_name: str


class UpdatePermission(BaseModel):
    permission_name: str
    new_name: str


class DeleteRole(BaseModel):
    role_name: str


class UpdateRole(BaseModel):
    role_name: str
    new_name: str


class PermissionResponse(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class PermissionRoleResponse(BaseModel):
    status: bool
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    user_id: UUID
    full_name: str
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
