from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Depends, Form, BackgroundTasks

from OtherFun import * 
from Middleware import Main
from verifyToken import verify_token_and_role
# import os
origins = ["https://chatbotservernode.onrender.com","https://cbns.vercel.app", "https://hfhchatbot.vercel.app", "http://localhost:5000", "http://localhost:3000", "https://localhost:5000"]

# origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app = FastAPI(debug=True)

app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # You can replace '*' with specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # or specific methods
    allow_headers=["Authorization", "Content-Type", "Accept"]  # or specific headers
)

model = Main()

class BodyModel(BaseModel):
    query: str
    chain_name: Optional[str] = None  # Made chain_name optional
    
@app.get("/")
async def home():
    return "chatbot api server is running..."


@app.post("/ask")
async def askQ(body: BodyModel, token: str = Depends(verify_token_and_role)):
    try:
        response = model.ask_question(body.query, token["username"] if body.chain_name is None else body.chain_name)
        return JSONResponse(content={"success": True, "data": response})
    except Exception as e:  # Catch specific exceptions
        return JSONResponse(content={"success": False, "error": str(e)})


@app.post("/create/embedding")
async def createEmbedding(collection_name: str = Form(...), files: List[UploadFile] = File(None), token: str = Depends(verify_token_and_role)):
    try:
        if not files:
            return JSONResponse(content={"success": False, "error":"No files provided"})
        
        responses = []
        for file in files:
            response = await process_file(model, collection_name, file)
            responses.append(response)

        return JSONResponse(content={"success": True,"responses": responses})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)})


@app.post("/create/tmp/chain")
async def createTmpChain(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...), token: str = Depends(verify_token_and_role)):
    try:
        if not files:
            return JSONResponse(content={"success": False, "error":"No files provided"})
                                
        all_contents = b""
        for file in files:
            contents = await file.read()
            all_contents += contents

        file_extension = files[0].filename.split(".")[-1]
        if file_extension == "pdf":
            chain_name = token["username"]
            model.generate_tmp_embedding_and_chain(all_contents, chain_name)
            background_tasks.add_task(delete_chain_after_delay(model, chain_name))
            return JSONResponse(content={"success": True, "message": "Chain created. Will be deleted after 2 hours."})
        elif file_extension == "txt":
            all_contents.decode("utf-8")
            return JSONResponse(content={"success": False, "error": "Unsupported file format"})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)})

