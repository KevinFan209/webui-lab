# 系統架構說明 (Architecture)

## 技術選型
- **前端**：純 HTML/CSS/JS，沿用課程教的 CSS 變數設計系統 + Grid/Flexbox + mobile-first RWD，不用框架。
- **後端**：FastAPI + uvicorn（`server.py`），延續 W03 已完成的本機→公開部署（IIS reverse proxy）架構。
- **Minecraft 狀態查詢**：`mcstatus` 套件，走 Minecraft 本來就公開、不需認證的 Server List Ping 協定——跟 Minecraft 遊戲用戶端在多人伺服器列表顯示資訊時用的是同一招，不需要在 Minecraft 伺服器那端額外開放任何東西。

## 模組劃分

這個專案其實涉及**兩套獨立系統**，刻意分開：

```
┌─────────────────────────────┐        ┌──────────────────────────────────┐
│ 這個課程 repo（Windows）      │        │ Mac mini（既有，這次完全不動）      │
│                              │        │                                    │
│ sites/ (前端靜態頁面)         │        │ server/ (Paper Minecraft 伺服器)    │
│ server.py (FastAPI)          │        │ panel/  (私人管理後台, port 8209)   │
│  ├─ GET  /api/status ────────┼───────▶│   - 不對外公開                     │
│  │   (mcstatus查詢)           │ SLP協定 │   - 有 RCON console/世界管理等高危 │
│  └─ POST /api/whitelist-apply│        │     操作，這次刻意不互通            │
│      (寫入本機 json)          │        │                                    │
└─────────────────────────────┘        └──────────────────────────────────┘
        │ 部署在
        ▼
https://demo.wke.csie.ncnu.edu.tw/s112213070/
```

- **公開網站**只透過 Minecraft 伺服器本身公開的 Server List Ping 協定查狀態，完全不碰私人管理後台（`panel/`，port 8209）。
- 白名單申請走「收件 → 存成待審清單」，不會自動對 Mac mini 發送任何指令；核准仍由管理員（我）手動用既有的 `ops/console.sh "whitelist add"` 處理。

## 資料流
1. 使用者開啟首頁 → `app.js` 的 `loadStatus()` 向自己的後端發 `fetch("api/status")`。
2. `server.py` 的 `/api/status` 用 `mcstatus.JavaServer.lookup("schmidt-lawsuits.tun.ply.gg")` 查詢，查詢失敗/逾時時回傳 `{online: false}`（不讓整個 request 500）。
3. 前端依回應渲染「在線/離線＋人數」。
4. 使用者填白名單申請表單 → `fetch POST "api/whitelist-apply"` → 後端驗證 Minecraft ID 格式 → 寫入 `data/whitelist_requests.json`（陣列，含時間戳）。
5. 管理員（我）事後自行查看這個 JSON 檔案，決定是否核准，核准的話手動在 Mac mini 上執行 `./ops/console.sh "whitelist add <id>"`。

## 為什麼不放 BlueMap 連結
Mac mini 的 BlueMap（3D地圖，`http://192.168.0.109:8100`）目前僅限內網或 Tailscale 存取，未對外開放。公開網站的訪客（外部朋友）本來就打不開這個網址，放一個對他們來說會失敗的連結沒有意義，因此刻意不放進公開首頁。

## 部署方式
延續 W03 已完成的架構：本機用 `uvicorn server:app --host 0.0.0.0 --port 7777` 開發測試；正式對外展示時設定 `ROOT_PATH` 環境變數，透過 IIS reverse proxy 掛到 `https://demo.wke.csie.ncnu.edu.tw/s112213070/`。
