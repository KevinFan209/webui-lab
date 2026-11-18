import os

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
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


app.mount("/", StaticFiles(directory="sites", html=True), name="sites")
