import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from mcstatus import JavaServer
from pydantic import BaseModel

MC_SERVER_ADDRESS = "schmidt-lawsuits.tun.ply.gg"
WHITELIST_FILE = Path("data/whitelist_requests.json")
MINECRAFT_ID_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,16}$")

app = FastAPI(
    docs_url="/api/docs",
    root_path=os.getenv("ROOT_PATH", "")
)


class WhitelistApplication(BaseModel):
    minecraft_id: str
    note: str = ""


@app.get("/api/status")
def get_status():
    try:
        server = JavaServer.lookup(MC_SERVER_ADDRESS, timeout=3)
        status = server.status()
        return {
            "online": True,
            "players_online": status.players.online,
            "players_max": status.players.max,
            "motd": status.motd.to_plain(),
            "version": status.version.name,
        }
    except Exception:
        # 伺服器離線或查詢逾時都算正常情境，不應該讓整個 request 500
        return {"online": False}


@app.post("/api/whitelist-apply")
def apply_whitelist(application: WhitelistApplication):
    if not MINECRAFT_ID_PATTERN.match(application.minecraft_id):
        return JSONResponse(
            status_code=400,
            content={"error": "minecraft_id 格式不正確（需為 3-16 個英數字或底線）"},
        )

    WHITELIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    if WHITELIST_FILE.exists():
        requests = json.loads(WHITELIST_FILE.read_text(encoding="utf-8"))
    else:
        requests = []

    requests.append({
        "minecraft_id": application.minecraft_id,
        "note": application.note,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    })
    WHITELIST_FILE.write_text(json.dumps(requests, ensure_ascii=False, indent=2), encoding="utf-8")

    return {"message": "申請已收到，管理員審核後會手動加入白名單"}


# 關鍵：html=True 讓它自動找 index.html；必須掛在所有 /api 路由之後
app.mount("/", StaticFiles(directory="sites", html=True), name="sites")
