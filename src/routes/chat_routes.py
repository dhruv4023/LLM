from fastapi import APIRouter
from src.controllers.chat.chats_controller import router as chat_routes
from src.controllers.chat.bot_controller import router as bot_routes
from src.controllers.chat.history_controller import router as history_routes

main_chat_router = APIRouter()

main_chat_router.include_router(chat_routes, prefix="", tags=["chatbot"])
main_chat_router.include_router(bot_routes, prefix="/bot", tags=["chatbot"])
main_chat_router.include_router(history_routes, prefix="/history", tags=["chatbot"])
