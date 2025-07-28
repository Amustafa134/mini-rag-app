from fastapi import FastAPI # type: ignore
from dotenv import load_dotenv
load_dotenv(".env")

from routes import base 

app = FastAPI()

app.include_router(base.base_router)
