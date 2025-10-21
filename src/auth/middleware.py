from http import HTTPStatus
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.config import settings

DEBUG = False


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        public_paths = ["/docs", "/redoc", "/openapi.json", "/login", "/login_from_refresh_token", "/registration"]

        if DEBUG:
            return await call_next(request)

        if request.url.path in public_paths:
            return await call_next(request)

        token = request.cookies.get("access_token")

        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token cookie required"}
            )

        try:
            payload = jwt.decode(token, str(settings.SECRET_KEY), algorithms=[settings.ALGORITHM])
            request.state.user = payload
        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )

        return await call_next(request)


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except LookupError as exc:
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={
                    "error": "Not Found",
                    "message": str(exc),
                    "detail": "The requested resource was not found"
                }
            )

        except PermissionError as exc:
            return JSONResponse(
                status_code=HTTPStatus.FORBIDDEN,
                content={
                    "error": "Forbidden",
                    "message": str(exc),
                    "detail": "Insufficient permissions to access this resource"
                }
            )

        except ValueError as exc:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={
                    "error": "Bad Request",
                    "message": str(exc),
                    "detail": "Invalid input data or validation error"
                }
            )

        except RuntimeError as exc:
            return JSONResponse(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                content={
                    "error": "Unprocessable Entity",
                    "message": str(exc),
                    "detail": "The operation could not be completed"
                }
            )

        except KeyError as exc:
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={
                    "error": "Not Found",
                    "message": str(exc),
                    "detail": "The requested key was not found"
                }
            )

        except Exception as exc:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                    "detail": str(exc) if str(exc) else "Unknown error"
                }
            )
