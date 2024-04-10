from fastapi import APIRouter, Depends, Request, UploadFile

from src.config.databaseConfig import DATABASE
from src.config.appConfig import ENV_VAR

from src.helpers.pagination import *
from src.helpers.response import ResponseHandler
from src.helpers.upload_file_cloudinary import upload_file

from src.middleware.verifyToken import verify_token

router = APIRouter()

# Your route definitions


from typing import Dict, List


def convert_form_data_to_dict(form_data) -> Dict[str, List[str]]:
    data_dict = {}

    for key, value in form_data.items():
        if isinstance(value, str):
            if key in data_dict:
                if isinstance(data_dict[key], list):
                    data_dict[key].append(value)
                else:
                    data_dict[key] = [data_dict[key], value]
            else:
                data_dict[key] = value
        elif isinstance(value, UploadFile):
            # Handle UploadFile separately if needed
            pass
        else:
            # Handle other types of values if needed
            pass

    # Convert keys with multiple values to lists
    for key in data_dict:
        if isinstance(data_dict[key], list) and len(data_dict[key]) > 1:
            continue  # Skip if it's already a list with multiple values
        elif key in form_data.getlist():
            data_dict[key] = form_data.getlist(key)

    return data_dict


@router.post("/create")
async def create_chat(
    req: Request, icon: UploadFile = None, tokenData=Depends(verify_token)
):
    try:
        username = tokenData["username"]
        form_data = await req.form()
        # payload = {key: form_data[key] for key in form_data if key != "picPath"}
        # dt = {}
        # print(convert_form_data_to_dict(form_data))

        if icon is None:
            return ResponseHandler.error(3007, None, 400)

        file_data = await upload_file(
            icon, form_data["collectionName"] + "_icon", "ChatIcons/"
        )

        icon_public_id = file_data["public_id"]
        # print(icon_public_id)
        # print(form_data["title"])
        # print(form_data["templateContext"])
        # print(form_data["collectionName"])
        # print(form_data["sampleQuetions"])
        # print(form_data)
        # print(ENV_VAR.MONGO_DB_NAME_CHATS)

        chat = DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS]["chats"].insert_one(
            {
                "username": username,
                "title": form_data["title"],
                "templateContext": form_data["templateContext"],
                "collectionName": form_data["collectionName"],
                "sampleQuetions": (
                    (form_data["sampleQuetions"])
                    if form_data["sampleQuetions"] is not None
                    else []
                ),
                "buttonIcon": icon_public_id,
            }
        )

        return ResponseHandler.success(3000, chat.acknowledged)
    except Exception as error:
        print(error)
        return ResponseHandler.error(9999, error, 500)


@router.get("/get")
async def get_paginated_chats(req: Request):
    try:
        page = int(req.query_params.get("page", 1))
        limit = int(req.query_params.get("limit", 10))

        total_count = DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS][
            "chats"
        ].estimated_document_count()

        chats = (
            DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS]["chats"]
            .find()
            .skip((page - 1) * limit)
            .limit(limit)
        )

        paginated_response = get_paginated_response(
            list(chats), page, limit, total_count
        )
        # print(paginated_response)
        return ResponseHandler.success(3001, paginated_response)
    except Exception as error:
        return ResponseHandler.error(9000, 500, error)


@router.get("/get/{collection_name}")
async def get_chat_by_collection_name(req: Request, collection_name: str):
    try:
        chat = DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS]["chats"].find_one(
            {"collectionName": collection_name}
        )
        if not chat:
            return ResponseHandler.error(3003, 404)
        return ResponseHandler.success(3002, chat)
    except Exception as error:
        return ResponseHandler.error(9000, 500, error)


@router.put("/edit/{collection_name}")
async def update_chat(
    req: Request,
    collection_name: str,
    icon: UploadFile = None,
    tokenData=Depends(verify_token),
):
    try:
        username = tokenData["username"]
        form_data = await req.form()
        chat = DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS]["chats"].find_one(
            {"collectionName": collection_name, "username": username}
        )

        if not chat:
            return ResponseHandler.error(3003, 404)

        icon_public_id = None
        if icon is not None:
            file_data = await upload_file(
                icon, form_data["collectionName"] + "_icon", "ChatIcons/"
            )
            icon_public_id = file_data["public_id"]

        updated_chat = DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS][
            "chats"
        ].find_one_and_update(
            {"collectionName": collection_name},
            {
                "$set": {
                    "title": form_data["title"],
                    "templateContext": form_data["templateContext"],
                    "buttonIcon": icon_public_id or chat.get("buttonIcon"),
                }
            },
        )

        if not updated_chat:
            return ResponseHandler.error(3003, 404)
        return ResponseHandler.success(3004)
    except Exception as error:
        return ResponseHandler.error(9000, 500, error)


@router.delete("/delete/{collection_name}")
async def delete_chat(collection_name: str, tokenData=Depends(verify_token)):
    try:
        username = tokenData["username"]
        deleted_chat = DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS][
            "chats"
        ].find_one_and_delete({"collectionName": collection_name, "username": username})
        if not deleted_chat:
            return ResponseHandler.error(3003, 404)
        return ResponseHandler.success(3005)
    except Exception as error:
        return ResponseHandler.error(9000, 500, error)
