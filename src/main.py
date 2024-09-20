from fastapi import FastAPI

import uvicorn
import asyncio

from sqladmin import Admin
from starlette.staticfiles import StaticFiles

from src.admin_schemas.admin_schema import BookAdmin
from src.database import engine
from src.auth.auth import auth_router, register_router, user_router

app = FastAPI(
    title="Library Book API",
    description="API для управления книгами в библиотеке. Включает операции по созданию, обновлению, удалению и получению данных о книгах.",
    version="1.0.0",
)


app.include_router(auth_router, prefix="/auth/jwt", tags=["Auth"])
app.include_router(register_router, prefix="/auth", tags=["Register"])
app.include_router(user_router, prefix="/users", tags=["Users"])

admin = Admin(app, engine)
admin.add_view(BookAdmin)


async def main() -> None:
    uvicorn.run(app=app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    asyncio.run(main())
