from fastapi import FastAPI
from src.config.appConfig import ENV_VAR
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.main import main

# import os
origins = ["http://localhost:3000","https://chatbothub.vercel.app"]

# origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
app = FastAPI(debug=ENV_VAR.DEBUG)

app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # You can replace '*' with specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # or specific methods
    allow_headers=["Authorization", "Content-Type", "Accept"],  # or specific headers
)

app.include_router(main)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=ENV_VAR.DEBUG)
