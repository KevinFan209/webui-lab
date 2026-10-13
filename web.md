# 每週技術學習筆記 (web.md)

> 每週依課程節奏更新：本週目標 / 完成清單 / 本週 Web 概念 / 除錯紀錄 / 心得

## W01 — 環境與 Git

**本週目標**：建立開發環境、初始化 Git/GitHub 專案。

**完成清單**
- [x] 安裝並確認 VS Code / Git / Node.js
- [x] `git init`、建立 `.gitignore`、`README.md`、`index.html`
- [x] 建立 GitHub public repo 並完成首次 commit/push

**本週 Web 概念**
_待填：用自己的話說明 VSCode / Git / GitHub / Node.js 之間的關係。_

**除錯紀錄**
_待填：問題 / 錯誤訊息 / 根因 / 如何發現 / 解法_

**心得**
_待填_

---

## W02 — Web UI and HTML

**本週目標**：拆分 CSS、練習語意化 HTML、填寫 Project Milestone 學習單。

**完成清單**
- [x] 建立 `css/style.css`、`js/app.js` 並於 `index.html` 引入（此二檔案於 W03 已搬移至 `sites/`，見 W03 紀錄）
- [ ] 使用語意化標籤重構頁面結構
- [x] 填寫 `docs/proposal.md` 的 Project Milestone 表格

**本週 Web 概念**
_待填：為何不建議所有版面都用 `<div>`？_

**除錯紀錄**
_待填_

**心得**
_待填_

---

## W03 — 從本機開發到公開部署

**本週目標**：把靜態網站改用 FastAPI + uvicorn 提供服務，完成助教登記前檢查清單，讓網站可以透過 IIS reverse proxy 公開展示。

**完成清單**
- [x] 建立 `server.py`，用 `FastAPI` + `StaticFiles(html=True)` 掛載網站
- [x] 把 `index.html`、`css/`、`js/` 整理進 `sites/`，統一由 `server.py` serve
- [x] 設定 `docs_url="/api/docs"`，並透過 `root_path=os.getenv("ROOT_PATH", "")` 讀取部署前綴
- [x] 本機用 `curl` 驗證 `/`、`/api/docs` 回應 `HTTP/1.1 200`
- [ ] 依檢查清單完成校內網/防火牆設定、向助教回報學號/IP/port（進行中）

**本週 Web 概念**
- **反向代理與 `root_path`**：本機直接開發時，網站是用 `http://127.0.0.1:port/` 存取；但助教的 IIS 會把 `https://demo.wke.csie.ncnu.edu.tw/s學號/` 這個公開網址，內部轉發到我本機的 `http://我的IP:port/`，過程中會把 `/s學號` 這段前綴拿掉再轉發。`root_path` 就是讓 FastAPI 知道「我其實是被掛在這個前綴底下」，這樣它自動產生的連結（例如 Swagger UI 用來抓 `openapi.json` 的網址）才會正確帶上前綴。**本機直接測試時網址列本來就不會出現前綴，這是正常的**，前綴只有透過 IIS 進來時才看得到。
- **部署設定不該寫死在程式邏輯裡**：`root_path` 應該用環境變數在啟動時注入，而不是寫死在 `server.py` 裡的字串——因為「掛在哪個路徑」是部署當下才決定的事，不是程式本身的邏輯。

**除錯紀錄**

| 問題 | 根因 | 如何發現 | 解法 |
|---|---|---|---|
| Swagger UI / API 路徑在部署後可能失效 | `server.py` 原本寫 `FastAPI(ROOT_PATH="/s112213070")`，但 FastAPI 建構子的參數名稱是小寫 `root_path`；大寫版本會被當成未知參數靜默吞掉，`app.root_path` 實際上還是空字串 | 直接用 Python 建立 `FastAPI(...)` 物件後印 `app.root_path`，發現值是 `''` 而不是預期的前綴 | 改成 `root_path=os.getenv("ROOT_PATH", "")`，並用環境變數在啟動 uvicorn 時注入 |
| `css/style.css`、`js/app.js` 載入會 404 | `server.py` 用 `StaticFiles(directory="sites", ...)` 掛載，但 `css/`、`js/` 資料夾還留在專案根目錄，沒有搬進 `sites/` | 實際跑起 uvicorn 用 `curl` 打 `/css/style.css`、`/js/app.js`，回應不是 200 | 把 `css/`、`js/` 整個搬進 `sites/css/`、`sites/js/`，再重測 `curl` 都回 200 |
| 改了 `ROOT_PATH` 重新整理瀏覽器，`/api/docs` 的 Servers 下拉選單卻沒有更新 | FastAPI 會把 OpenAPI schema 快取在 **process 第一次**收到請求時的結果；如果 process 啟動後第一個打進來的請求 `root_path` 是空的，schema 就會被永久快取成「沒有 servers」，之後同一個 process 內怎麼改環境變數都不會反映 | 讀 FastAPI 原始碼的 `setup()` 方法，發現 `self.openapi()` 有「只在第一次呼叫時產生，之後回傳快取」的行為 | 每次變更 `ROOT_PATH` 後，必須整個重啟 uvicorn process（不能只重新整理頁面），讓 schema 快取重算 |

**心得**
_待填_

---

## W04 — 期末專案主題確定：Minecraft 伺服器玩家入口網站

**本週目標**：原訂的「Python 程式碼學習網」主題被教授否決（市面同類產品太多），重新發想並確定新主題，完成 MVP 並驗證可動。

**完成清單**
- [x] 與教授討論後確定新主題：把自己在 Mac mini 上維運的 Minecraft 伺服器，做成一個對外公開的玩家入口網站（跟既有的私人管理後台刻意分開）
- [x] 透過 SSH 檢視 Mac mini 上既有的伺服器/管理後台現況，確認可以重用、不需重做的部分
- [x] `server.py` 新增 `GET /api/status`（用 `mcstatus` 查 Minecraft Server List Ping）、`POST /api/whitelist-apply`（驗證格式後寫入 `data/whitelist_requests.json`）
- [x] 重寫 `sites/` 首頁：連線資訊、即時狀態 widget、白名單申請表單；CSS 拆成 `variables`/`layout`/`components` 三檔，套用 CSS 變數設計系統＋mobile-first RWD
- [x] 新增 `requirements.txt`（`fastapi`/`uvicorn`/`mcstatus`），`data/` 加進 `.gitignore`
- [x] 改寫 `docs/proposal.md`、`architecture.md`、`security.md` 為新主題內容
- [x] 本機 `curl` 實測 `/api/status` 真的連到家裡那台 Mac mini 的真實伺服器（回傳在線人數/MOTD），`/api/whitelist-apply` 合法/不合法輸入分別驗證成功

**本週 Web 概念**
_待填：為什麼前端 `fetch()` 自己後端的 API、而不是直接從瀏覽器打 Mac mini 上的服務，可以避開 CORS 問題？_

**除錯紀錄**

| 問題 | 根因 | 如何發現 | 解法 |
|---|---|---|---|
| SSH 連 Mac mini 時，用 `KevinFandeMac-mini.local` 這個主機名稱時連時斷 | `.local` 是 mDNS（Bonjour）主機名稱，通常只能在**同一個區域網路**內可靠解析，跨網路/跨VPN時解析結果不穩定 | 同一條指令重複執行，有時候成功有時候「Could not resolve hostname」 | 改用 Mac mini 的實際區域網路 IP（`192.168.0.109`）直接連，就穩定了 |

**心得**
_待填_
