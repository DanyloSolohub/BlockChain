import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv
import web

load_dotenv(find_dotenv())
SWAGGER_URL = os.getenv('SWAGGER_URL')
KEY_SIZE = int(os.getenv('KEY_SIZE'))

app = FastAPI(docs_url=SWAGGER_URL, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(web.router)
