from fastapi_users.authentication import JWTStrategy
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users import FastAPIUsers

from src.models import User

from src.settings import settings
from src.database import get_user_db

from src.auth.schemas.input import UserCreate, UserRead, UserUpdate

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_db,
    [auth_backend],
)


current_active_user = fastapi_users.current_user(active=True)


user_router = fastapi_users.get_users_router(user_schema=UserRead, user_update_schema=UserUpdate)
auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
