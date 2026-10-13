# WebUI Lab

Web Programming 課程實作專案。

## 學號
112213070

## 專案結構
```
.
├─ server.py            # FastAPI 進入點：/api/status、/api/whitelist-apply，其餘掛載 sites/
├─ sites/                # 實際被 serve 的網站內容
│  ├─ index.html
│  ├─ css/                # variables.css / layout.css / components.css
│  └─ js/app.js
├─ data/                # 白名單申請紀錄（執行時自動產生，不進git）
├─ requirements.txt     # fastapi / uvicorn / mcstatus
├─ assets/              # 圖片/圖示等靜態資源
├─ docs/                # 企劃書、架構說明、資安檢查、期末報告
├─ web.md                # 每週技術學習筆記
└─ ai.md                 # 每週 AI 協作反思紀錄
```

## 本機執行

安裝套件：
```bash
pip install -r requirements.txt
```

啟動（本機測試，不需要設定 `ROOT_PATH`）：
```bash
uvicorn server:app --host 0.0.0.0 --port 7777
```
啟動後於瀏覽器開啟 `http://127.0.0.1:7777`，API 文件在 `http://127.0.0.1:7777/api/docs`。

## 公開部署（助教登記用）

啟動前需設定 `ROOT_PATH` 環境變數（依助教配的學號前綴，例如 `/s112213070`）；**`ROOT_PATH` 環境變數和 `--root-path` 這個 CLI 參數只能擇一使用，不要同時設定**：

**PowerShell**
```powershell
$env:ROOT_PATH = "/s112213070"
uvicorn server:app --host 0.0.0.0 --port 7777
```

**Git Bash / macOS / Linux**
```bash
ROOT_PATH=/s112213070 uvicorn server:app --host 0.0.0.0 --port 7777
```

> 若中途變更過 `ROOT_PATH`，需要整個重新啟動 uvicorn process（不能只重新整理瀏覽器），因為 FastAPI 會把 OpenAPI schema 快取在第一次請求的結果，process 不重啟的話快取不會更新。

登記後，助教會把它掛到 `https://demo.wke.csie.ncnu.edu.tw/s112213070/`（注意結尾斜線）。
