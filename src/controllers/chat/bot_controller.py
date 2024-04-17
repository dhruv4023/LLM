from fastapi import BackgroundTasks, APIRouter, Request, UploadFile, Depends, File
from typing import List

from src.helpers.response import ResponseHandler
from src.helpers.json_convertor import convert_to_json

from src.middleware.verifyToken import verify_token
from src.services.message_services import save_question_and_answer_to_chat_history

from src.bot.main import Main
from src.bot.OtherFun import delete_chain_after_delay, process_file

router = APIRouter()

model = Main()


@router.post("/ask-question")
async def askQ(req: Request, token: str = Depends(verify_token)):
    try:
        form_data = await req.json()
        answer = model.ask_question(
            form_data["query"],
            (
                token["username"]
                if form_data["collectionName"] is None
                else form_data["collectionName"]
            ),
        )
        await save_question_and_answer_to_chat_history(
            token["username"],
            {
                "question": form_data["query"],
                "answer": answer,
                "collectionName": (
                    form_data["query"] if form_data["query"] else "CHAT WITH YOUR PDF"
                ),
            },
        )
        return ResponseHandler.success(2001, answer)
    except Exception as error:
        print(error)
        return ResponseHandler.error(9999, error, 500)


@router.post("/create/embedding/{collection_name}")
async def createEmbedding(
    collection_name: str,
    files: List[UploadFile] = File(None),
    tokenData: str = Depends(verify_token),
):
    try:
        if not files:
            return ResponseHandler.error(2003)

        responses = []
        for file in files:
            response = process_file(model, collection_name, file)
            responses.append(response)

        return ResponseHandler.success(2002, response)
    except Exception as error:
        return ResponseHandler.error(9999, error, 500)


@router.post("/create/tmp/chain")
async def createTmpChain(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    tokenData: str = Depends(verify_token),
):
    try:
        if not files:
            return ResponseHandler.error(2003, error, 500)

        all_contents = b""
        for file in files:
            contents = await file.read()
            all_contents += contents

        file_extension = files[0].filename.split(".")[-1]
        if file_extension == "pdf":
            chain_name = tokenData["username"]
            model.generate_tmp_embedding_and_chain(all_contents, chain_name)
            background_tasks.add_task(delete_chain_after_delay(model, chain_name))
            return ResponseHandler.success(2001)
        elif file_extension == "txt":
            all_contents.decode("utf-8")
            return ResponseHandler.error(2004, error, 500)

    except Exception as error:
        return ResponseHandler.error(9999, error, 500)
