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


@app.get("/api/chat")
def get_chat_messages(db: Session = Depends(database.get_db)):
    messages = (
        db.query(models.ChatMessage)
        .order_by(models.ChatMessage.created_at.desc(), models.ChatMessage.id.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "username": chat_message.username,
            "message": chat_message.message,
            "created_at": chat_message.created_at.isoformat(),
        }
        for chat_message in reversed(messages)
    ]


@app.post("/api/chat")
def create_chat_message(
    chat_message: schemas.ChatMessageCreate,
    db: Session = Depends(database.get_db),
):
    message = chat_message.message.strip()
    if not message:
        return JSONResponse(
            status_code=400,
            content={"error": "訊息不能是空的"},
        )

    new_message = models.ChatMessage(
        username=chat_message.username,
        message=message,
    )
    db.add(new_message)
    db.commit()
    return {"message": "已送出"}


@app.post("/api/friends/add")
def add_friend(
    friendship: schemas.FriendAdd,
    db: Session = Depends(database.get_db),
):
    if friendship.username == friendship.friend_username:
        return JSONResponse(
            status_code=400,
            content={"error": "不能把自己加為好友"},
        )

    user = (
        db.query(models.User)
        .filter(models.User.username == friendship.username)
        .first()
    )
    friend = (
        db.query(models.User)
        .filter(models.User.username == friendship.friend_username)
        .first()
    )
    if user is None or friend is None:
        return JSONResponse(
            status_code=400,
            content={"error": "找不到使用者"},
        )

    existing_friendship = (
        db.query(models.Friendship)
        .filter(
            models.Friendship.user_id == user.id,
            models.Friendship.friend_id == friend.id,
        )
        .first()
    )
    if existing_friendship is not None:
        return JSONResponse(
            status_code=400,
            content={"error": "已經是好友"},
        )

    db.add_all(
        [
            models.Friendship(user_id=user.id, friend_id=friend.id),
            models.Friendship(user_id=friend.id, friend_id=user.id),
        ]
    )
    db.commit()
    return {"message": "已新增好友"}


@app.get("/api/friends")
def get_friends(username: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        return JSONResponse(
            status_code=400,
            content={"error": "找不到使用者"},
        )

    friend_ids = [
        friendship.friend_id
        for friendship in db.query(models.Friendship)
        .filter(models.Friendship.user_id == user.id)
        .all()
    ]
    friends = db.query(models.User).filter(models.User.id.in_(friend_ids)).all()
    return [{"username": friend.username} for friend in friends]


@app.get("/api/groups")
def get_groups(username: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        return JSONResponse(
            status_code=400,
            content={"error": "找不到使用者"},
        )

    group_ids = [
        membership.group_id
        for membership in db.query(models.GroupMember)
        .filter(models.GroupMember.user_id == user.id)
        .all()
    ]
    groups = db.query(models.Group).filter(models.Group.id.in_(group_ids)).all()
    return [{"id": group.id, "name": group.name} for group in groups]


@app.post("/api/groups/create")
def create_group(
    group: schemas.GroupCreate,
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.username == group.username).first()
    if user is None:
        return JSONResponse(
            status_code=400,
            content={"error": "找不到使用者"},
        )

    existing_group = (
        db.query(models.Group)
        .filter(models.Group.name == group.name)
        .first()
    )
    if existing_group is not None:
        return JSONResponse(
            status_code=400,
            content={"error": "群組名稱已被使用"},
        )

    new_group = models.Group(name=group.name, created_by=user.id)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    db.add(models.GroupMember(group_id=new_group.id, user_id=user.id))
    db.commit()
    return {"message": "群組已建立"}


@app.post("/api/groups/join")
def join_group(
    membership: schemas.GroupJoin,
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.username == membership.username)
        .first()
    )
    if user is None:
        return JSONResponse(
            status_code=400,
            content={"error": "找不到使用者"},
        )

    group = (
        db.query(models.Group)
        .filter(models.Group.name == membership.group_name)
        .first()
    )
    if group is None:
        return JSONResponse(
            status_code=400,
            content={"error": "找不到群組"},
        )

    existing_membership = (
        db.query(models.GroupMember)
        .filter(
            models.GroupMember.group_id == group.id,
            models.GroupMember.user_id == user.id,
        )
        .first()
    )
    if existing_membership is not None:
        return JSONResponse(
            status_code=400,
            content={"error": "已經加入這個群組"},
        )

    db.add(models.GroupMember(group_id=group.id, user_id=user.id))
    db.commit()
    return {"message": "已加入群組"}


app.mount("/", StaticFiles(directory="sites", html=True), name="sites")
