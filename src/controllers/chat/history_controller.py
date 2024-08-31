from typing import Optional
from fastapi import APIRouter, Depends
from bson import ObjectId

from src.config.appConfig import ENV_VAR
from src.config.databaseConfig import DATABASE

from src.helpers.response import ResponseHandler
from src.helpers.pagination import get_paginated_response

from src.middleware.verifyToken import verify_token

router = APIRouter()


@router.delete("/delete")
async def delete_chat_history(tokenData: str = Depends(verify_token)):
    try:
        username = tokenData["username"]
        deleted_chat_history = DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS][
            "chathistories"
        ].delete_one({"username": username})

        if deleted_chat_history.deleted_count == 0:
            return ResponseHandler.error(4002, 404)
        else:
            return ResponseHandler.success(4004)
    except Exception as error:
        print("Error deleting chat history:", error)
        return ResponseHandler.error(9000, 500, error)


@router.delete("/delete/question/{questionId}")
async def delete_question_from_history(
    questionId: str, tokenData: str = Depends(verify_token)
):
    try:
        username = tokenData["username"]
        update_query = {
            "$pull": {"history": {"_id": ObjectId(questionId)}},
            "$inc": {"historyCount": -1},
        }

        result = DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS][
            "chathistories"
        ].update_one(
            {"username": username, "history._id": ObjectId(questionId)}, update_query
        )
        print(result)
        if result.matched_count != 0:
            return ResponseHandler.success(4005)
        else:
            return ResponseHandler.error(4006, 404)
    except Exception as error:
        print("error:", error)
        return ResponseHandler.error(9000, 500, error)


@router.get("/get")
async def get_chat_history_by_user_id(
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
    tokenData: str = Depends(verify_token),
):
    try:
        print(tokenData)
        username = tokenData["username"]

        start_index = (page - 1) * limit

        chat_history = DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS][
            "chathistories"
        ].find_one(
            {"username": username}, {"history": {"$slice": [start_index, limit]}}
        )

        if chat_history:
            paginated_response = get_paginated_response(
                chat_history["history"], page, limit, chat_history["historyCount"]
            )
            return ResponseHandler.success(4001, paginated_response)
        else:
            return ResponseHandler.error(4002, 404)
    except Exception as error:
        print("Error getting chat history:", error)
        return ResponseHandler.error(9000)
