from fastapi import APIRouter
from src.controllers.auth.auth_controller import router as auth_routes
from src.controllers.auth.user_controller import router as user_routes
from src.controllers.auth.otp_controller import router as otp_routes

main_auth_router = APIRouter()

main_auth_router.include_router(auth_routes, prefix="/auth", tags=["Authentication"])
main_auth_router.include_router(user_routes, prefix="/user", tags=["Authentication"])
main_auth_router.include_router(otp_routes, prefix="/mail", tags=["Authentication"])
