from fastapi import APIRouter, Request, UploadFile, Header
from src.config.appConfig import ENV_VAR
from src.helpers.response import ResponseHandler
from src.helpers.send_request import sendRequest
from typing import Optional

router = APIRouter()
AUTH_API_END = ENV_VAR.AUTH_API_END


@router.get("/userid/{uid}")
async def get_users(uid: str):
    try:
        response = get_user_date(uid)
        return ResponseHandler.success_mediator(response)
    except Exception as error:
        return ResponseHandler.error(error)

def get_user_date(uid):
    return sendRequest(
        url=f"{AUTH_API_END}/api/v1/user/get/userid/{uid}",
        headers={"Content-Type": "application/json"},
    )

@router.put("/update/")
async def update_user_data(
    req: Request, picPath: UploadFile = None, authorization: str = Header(None)
):
    try:
        form_data = await req.form()

        payload = {key: form_data[key] for key in form_data if key != "picPath"}

        files = None

        if picPath:
            files = {"picPath": (picPath.filename, picPath.file, picPath.content_type)}

        headers = {"Authorization": authorization}
        response = sendRequest(
            f"{AUTH_API_END}/api/v1/user/update/",
            "put",
            payload,
            files,
            headers,
        )
        return ResponseHandler.success_mediator(response)
    except Exception as e:
        return ResponseHandler.error(9999, e)
