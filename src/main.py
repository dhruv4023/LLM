from fastapi import APIRouter
from src.routes.main import main_router
import src.config.cloudinaryConfig
from src.config.databaseConfig import DATABASE

origins = ["http://localhost:3000"]

main = APIRouter()

DATABASE()

main.include_router(main_router, prefix="/api", tags=["main"])

from src.helpers.response import ResponseHandler


@main.get("/")
async def home():
    return ResponseHandler.success(message_code=9000)
