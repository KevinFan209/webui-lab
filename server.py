import json
import os
import re
from datetime import datetime, timezone

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from mcstatus import JavaServer
from sqlalchemy.orm import Session
import database, models
import schemas
from passlib.context import CryptContext

database.Base.metadata.create_all(bind=database.engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    docs_url="/api/docs",
    root_path=os.getenv("ROOT_PATH", "")
)

@app.post("/api/register")
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db),
):
    if db.query(models.User).filter(models.User.username == user.username).first():
        return JSONResponse(
            status_code=400,
            content={"error": "使用者名稱已被使用"},
        )

    if db.query(models.User).filter(models.User.email == user.email).first():
        return JSONResponse(
            status_code=400,
            content={"error": "Email已被使用"},
        )

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=pwd_context.hash(user.password),
    )
    db.add(new_user)
    db.commit()
    return {"message": "註冊成功"}


@app.post("/api/login")
def login_user(
    user: schemas.UserLogin,
    db: Session = Depends(database.get_db),
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )
    if existing_user is None or not pwd_context.verify(
        user.password,
        existing_user.hashed_password,
    ):
        return JSONResponse(
            status_code=400,
            content={"error": "帳號或密碼錯誤"},
        )

    return {"message": "登入成功"}


@app.get("/api/status")
def get_server_status():
    try:
        server = JavaServer.lookup("schmidt-lawsuits.tun.ply.gg")
        status = server.status()
        return {
            "online": True,
            "players_online": status.players.online,
            "players_max": status.players.max,
            "motd": status.description,
            "version": status.version.name,
        }
    except Exception:
        return {"online": False}


@app.post("/api/whitelist-apply")
def apply_for_whitelist(application: schemas.WhitelistApply):
    if not re.fullmatch(r"[A-Za-z0-9_]{3,16}", application.minecraft_id):
        return JSONResponse(
            status_code=400,
            content={"error": "Minecraft ID 格式錯誤（3-16字元，只能英數字與底線）"},
        )

    os.makedirs("data", exist_ok=True)
    requests_path = os.path.join("data", "whitelist_requests.json")
    if os.path.exists(requests_path):
        with open(requests_path, encoding="utf-8") as requests_file:
            requests = json.load(requests_file)
    else:
        requests = []

    requests.append(
        {
            "minecraft_id": application.minecraft_id,
            "note": application.note,
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    with open(requests_path, "w", encoding="utf-8") as requests_file:
        json.dump(requests, requests_file, ensure_ascii=False, indent=4)

    return {"message": "申請已送出，等待審核"}


app.mount("/", StaticFiles(directory="sites", html=True), name="sites")
