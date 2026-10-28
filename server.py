import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    docs_url="/api/docs",
    root_path=os.getenv("ROOT_PATH", "")
)

app.mount("/", StaticFiles(directory="sites", html=True), name="sites")
