import json

from fastapi import FastAPI
from fastapi.params import Depends

from src.auth.dependencies import get_user_use_case, check_permission, get_role_use_case, get_permission_use_case, \
    get_auth_use_case, get_refresh_token
from src.auth.middleware import JWTMiddleware, ExceptionMiddleware
from fastapi import Response

from src.auth.schemas import UserCreate, RoleCreate, PermissionCreate, AddPermissionToRole, Login, DeleteRole, \
    UpdateRole, DeletePermission, UpdatePermission, UserUpdate
from src.auth.use_cases import UserUseCases, RoleCases, PermissionCases, AuthCases

app = FastAPI()
app.add_middleware(JWTMiddleware)
app.add_middleware(ExceptionMiddleware)


@app.post("/registration")
async def create_user(
        user_create: UserCreate,
        user_use_cases: UserUseCases = Depends(get_user_use_case)
):
    return await user_use_cases.create_user(user_create)


@app.patch("/update_user")
async def update_user(
        update_user: UserUpdate,
        payload: dict = Depends(check_permission('user:update')),
        user_use_cases: UserUseCases = Depends(get_user_use_case)
):
    return await user_use_cases.update_user(payload, update_user)


@app.delete("/delete_user")
async def delete_user(
        payload: dict = Depends(check_permission('user:delete')),
        user_use_cases: UserUseCases = Depends(get_user_use_case)
):
    await user_use_cases.delete_user(payload)
    response = Response(
        content=json.dumps({"message": "delete successful"}),
        media_type="application/json"
    )
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=0,
        expires=0,
        path="/"
    )
    return response


@app.post("/create_role")
async def create_role(
        create_role: RoleCreate,
        payload: dict = Depends(check_permission('role:create')),
        role_use_cases: RoleCases = Depends(get_role_use_case)

):
    return await role_use_cases.create_role(create_role)


@app.delete("/delete_role")
async def delete_role(
        delete_role: DeleteRole,
        payload: dict = Depends(check_permission('role:delete')),
        role_use_cases: RoleCases = Depends(get_role_use_case)
):
    return await role_use_cases.delete_role(delete_role)


@app.patch("/update_role")
async def update_role(
        update_role: UpdateRole,
        payload: dict = Depends(check_permission('role:update')),
        role_use_cases: RoleCases = Depends(get_role_use_case)
):
    return await role_use_cases.update_role(update_role)


@app.post("/create_permission")
async def create_permission(
        permission_create: PermissionCreate,
        payload: dict = Depends(check_permission('permission:create')),
        permission_use_cases: PermissionCases = Depends(get_permission_use_case)
):
    return await permission_use_cases.create_permission(permission_create)


@app.patch("/update_permission")
async def update_permission(
        permission_update: UpdatePermission,
        payload: dict = Depends(check_permission('permission:update')),
        permission_use_cases: PermissionCases = Depends(get_permission_use_case)
):
    return await permission_use_cases.update_permission(permission_update)


@app.delete("/delete_permission")
async def delete_permission(
        permission_delete: DeletePermission,
        payload: dict = Depends(check_permission('permission:delete')),
        permission_use_cases: PermissionCases = Depends(get_permission_use_case)
):
    return await permission_use_cases.delete_permission(permission_delete)


@app.post("/add_permission_to_role")
async def add_permission_to_role(
        add_perm_to_role: AddPermissionToRole,
        payload: dict = Depends(check_permission('role_permission:update')),
        permission_use_cases: PermissionCases = Depends(get_permission_use_case)
):
    return await permission_use_cases.add_permission_to_role(add_perm_to_role)


@app.post("/login_from_refresh_token")
async def login_from_refresh_token(
        refresh_token: str = Depends(get_refresh_token),
        auth_use_cases: AuthCases = Depends(get_auth_use_case)
):
    token = await auth_use_cases.refresh_token(refresh_token)
    response = Response(
        content=json.dumps({"message": "Login successful"}),
        media_type="application/json"
    )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=24 * 60 * 60,
        path="/"
    )

    return response


@app.post("/login")
async def login(
        log: Login,
        auth_use_cases: AuthCases = Depends(get_auth_use_case)
):
    tokens = await auth_use_cases.login(log)
    response = Response(
        content=json.dumps({"message": "Login successful"}),
        media_type="application/json"
    )
    response.set_cookie(
        key="access_token",
        value=tokens[0],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=24 * 60 * 60,
        path="/"
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens[1],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=24 * 60 * 60,
        path="/"
    )

    return response


@app.post("/logout")
async def logout(
        payload: dict = Depends(check_permission('user:logout')),
        auth_use_cases: AuthCases = Depends(get_auth_use_case)
):
    await auth_use_cases.logout(payload)
    response = Response(
        content=json.dumps({"message": "Logout successful"}),
        media_type="application/json"
    )
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=False,  # для тестов на http
        samesite="lax",
        max_age=0,
        expires=0,
        path="/"
    )
    response.set_cookie(
        key="refresh_token",
        value="",
        httponly=True,
        secure=False,  # для тестов на http
        samesite="lax",
        max_age=0,
        expires=0,
        path="/"
    )
    return response
