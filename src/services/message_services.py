from src.config.databaseConfig import DATABASE
from src.config.appConfig import ENV_VAR
from bson import ObjectId


async def save_question_and_answer_to_chat_history(username, history_obj):
    try:
        existing_chat_history = DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS][
            "chathistories"
        ].find_one({"username": username})
        history_obj["_id"] = ObjectId()
        if not existing_chat_history:
            new_chat_history = {
                "username": username,
                "history": [history_obj],
                "historyCount": 1,
            }
            DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS]["chathistories"].insert_one(
                new_chat_history
            )
        else:
            DATABASE.client[ENV_VAR.MONGO_DB_NAME_CHATS]["chathistories"].update_one(
                {"username": username},
                {
                    "$push": {"history": {"$each": [history_obj], "$position": 0}},
                    "$inc": {"historyCount": 1},
                },
            )
    except Exception as error:
        raise ValueError(f"Error saving question and answer to chat history: {error}")
