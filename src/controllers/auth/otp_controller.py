from fastapi import APIRouter, Request
from src.config.appConfig import ENV_VAR
from src.helpers.response import ResponseHandler
from src.helpers.send_request import sendRequest

router = APIRouter()
AUTH_API_END = ENV_VAR.AUTH_API_END


@router.post("/send-otp")
async def send_otp_controller(req: Request):
    try:
        # Make the request to the authentication API endpoint
        response = sendRequest(
            f"{AUTH_API_END}/api/v1/mail/send-otp",
            "post",
            req,
            None,
            {"Content-Type": "application/json"},
        )
        # Handle the response using the ResponseHandler
        return ResponseHandler.success_mediator(response)
    except Exception as e:
        # Log and handle any exceptions
        print(e)
        return ResponseHandler.error(9999, e)
