from fastapi import Response
from src.langs.en.messages import get_message
from src.helpers.json_convertor import convert_to_json

class ResponseHandler:
    @staticmethod
    def success(message_code=None, data=None, status_code=200):
        response = {
            "success": True,
            "message": get_message(message_code),
            "data": data
        }
        return Response(content=convert_to_json(response), status_code=status_code, media_type="application/json")

    @staticmethod
    def error(message_code=9999, error=None, status_code=422, data=None):
        response = {
            "success": False,
            "message": get_message(message_code),
            "error": str(error) if error else None,
            "data": data
        }
        return Response(content=convert_to_json(response), status_code=(500 if message_code == 9999 else status_code), media_type="application/json")

    @staticmethod
    def success_mediator(response):
        return Response(content=(response.content), status_code=response.status_code, media_type="application/json")