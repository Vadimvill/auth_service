from fastapi import FastAPI
from fastapi.params import Depends
from src.auth.dependencies import get_user_use_case

from src.auth.schemas import UserCreate, RoleCreate, PermissionCreate, AddPermissionToRole
from src.auth.use_cases import UserUseCases

app = FastAPI()


@app.post("/create_user")
async def create_user(
        user_create: UserCreate,
        user_use_cases: UserUseCases = Depends(get_user_use_case)
):
    return await user_use_cases.create_user(user_create)


@app.post("/create_role")
async def create_role(
        create_role: RoleCreate,
        user_use_cases: UserUseCases = Depends(get_user_use_case)
):
    return await user_use_cases.create_role(create_role)


@app.post("/create_permission")
async def create_permission(
        permission_create: PermissionCreate,
        user_use_cases: UserUseCases = Depends(get_user_use_case)
):
    return await user_use_cases.create_permission(permission_create)


@app.post("/add_permission_to_role")
async def add_permission_to_role(
        add_perm_to_role: AddPermissionToRole,
        user_use_cases: UserUseCases = Depends(get_user_use_case)
):
    return await user_use_cases.add_permission_to_role(add_perm_to_role)
