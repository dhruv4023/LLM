from fastapi import APIRouter
from src.routes.auth_routes import main_auth_router
from src.routes.chat_routes import main_chat_router

main_router = APIRouter()

main_router.include_router(main_auth_router)
main_router.include_router(main_chat_router)
