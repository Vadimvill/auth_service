import uuid

from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    func, Text, UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    full_name = Column(String(50), nullable=False)

    email = Column(String(50), nullable=False, unique=True)

    is_active = Column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    password_hash = Column(Text)

    user_role_id = Column(UUID(as_uuid=True), ForeignKey("roles.role_id"))

    user_role = relationship("Role", back_populates="users", foreign_keys=[user_role_id])

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.role_id"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.permission_id"), primary_key=True),
    UniqueConstraint('role_id', 'permission_id', name='uq_role_permission'),
)


class Role(Base):
    __tablename__ = "roles"
    role_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String(50), nullable=False, unique=True)

    users = relationship("User", back_populates="user_role")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"
    permission_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String(50), nullable=False, unique=True)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
