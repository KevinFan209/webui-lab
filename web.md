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

---

## W05 — 登入/註冊頁面 UI 原型（CSS-only）

**本週目標**：從空白頁面重新開始，練習用純 CSS 設計登入/註冊雙表單排版，暫不接任何 JS 邏輯。

**完成清單**
- [x] 把 `sites/index.html` 還原成最基礎的 HTML5 骨架，`css/`、`js/` 下的舊檔案（`variables.css`/`layout.css`/`components.css`/`app.js`，原本是 Minecraft 入口網站 MVP 的版面）清空重來
- [x] 重寫 `sites/index.html`：加入 `.login-form`、`.register-form` 兩個 `<form>`
- [x] 新增 `sites/css/index.css`：CSS 變數（`:root` 設色/深色主題）、Grid 雙欄排版、`::before`/`::after` 裝飾文字、focus 狀態、RWD breakpoint（`max-width: 680px`）、`prefers-reduced-motion`
- [x] 新增 `sites/js/index.js`（目前為空檔案，尚未實作表單送出邏輯）
- [ ] 表單目前沒有接任何 `fetch`，`/api/status`、`/api/whitelist-apply` 這兩個既有後端路由暫時沒有被前端呼叫到

**本週 Web 概念**
_待填_

**除錯紀錄**
_待填_

**心得**
_待填_

---

## 剩餘規劃（W10–W15，共 6 週）

> 目標改為：把企劃書/簡報裡提過的完整功能都做出來——不只是帳號系統，還包括聊天、查看世界地圖、玩家交易看板，對應之前「未來擴充路線圖」投影片的三個方向（管理後台整合／玩家社群功能／資訊與通知）。時間剩約 6 週，每週任務比原來多，排序原則：**先把帳號系統這個地基做穩，再疊上去的功能才有登入保護可用**。對照 `lesson_file/web05.md` 課程大綱，還沒落地的主題依序是：W06 Fetch API/AJAX、W07 表單驗證/XSS、W08 OAuth概念、W09 JWT、W10 Session/Cookie、W11 整合重構、W12 資安檢查清單，分別對應到下面各週。
>
> **安全邊界維持不變**（跟企劃書/簡報裡「刻意不做」一致）：聊天只做**網站自己的聊天室**，不會透過 RCON 把訊息寫回遊戲內；交易做**純文字配對的揭示板**，不會真的操作遊戲內物品（dupe風險）；地圖是把既有 BlueMap 串接進來顯示，不會新增寫入權限。

## W10 — 帳號系統核心：註冊 + 登入 + 保護機制

**本週目標**：把 register/login 從「指令測試」變成真正能動的功能，並讓「登入」這件事能保護後面所有功能，對應課程 W09（JWT/token）登入機制的起點。

**完成清單**
- [ ] `/api/register`：bcrypt 雜湊密碼、寫入資料庫（`database.py`/`models.py`），前端 `register-form` 用 `fetch` POST，依「使用者名稱重複」「密碼格式不符」分別跳出對應 alert
- [ ] `/api/login`：驗證帳密是否一致，驗證通過後建立登入狀態（session 或 JWT，下週任務再定案用哪個），前端 `login-form` 用 `fetch` POST 並處理成功/失敗
- [ ] `/api/logout`：清除登入狀態
- [ ] 設計一個簡單的「登入保護」檢查機制（例如一個 `require_login` 的 dependency/decorator），之後每個新功能的 API 都掛上去
- [ ] 把之前拿掉的 `/api/status`、`/api/whitelist-apply` 重新接回來，改成登入後才能查詢/送出，驗證未登入時會被擋下來

**本週 Web 概念**
_待填_

**除錯紀錄**
_待填_

**心得**
_待填_

---

## W11 — 表單驗證、Fetch 錯誤處理 + 聊天室第一版

**本週目標**：補齊課程 W06（Fetch API 錯誤處理）、W07（表單驗證/XSS 防護）的細節，並做出第一版「網站自己的聊天室」（不是遊戲內聊天）。

**完成清單**
- [ ] 前端輸入驗證：使用者名稱/密碼格式、必填檢查；避免把使用者輸入直接塞進 `innerHTML` 造成 XSS
- [ ] 全面檢查所有 `fetch` 呼叫的錯誤處理（網路失敗、後端回 4xx/5xx 各自要顯示什麼），不是只處理成功情境
- [ ] `/api/chat`：`GET` 回傳最近訊息列表、`POST` 需登入才能發言（掛上 W10 做的登入保護）
- [ ] 前端聊天室頁面：用定時 `fetch`（polling）更新訊息列表，訊息內容用 `textContent` 而不是 `innerHTML` 顯示（防 XSS）
- [ ] 確認：未登入的訪客可以「看」聊天室，但不能「發言」

**本週 Web 概念**
_待填_

**除錯紀錄**
_待填_

**心得**
_待填_

---

## W12 — 世界地圖串接 + 玩家交易看板

**本週目標**：把 Mac mini 上既有的 BlueMap 地圖串接進公開網站（登入後才能看），並做一個安全版的玩家交易功能。

**完成清單**
- [ ] 確認 BlueMap 目前的對外可達性（README 提過原本只限內網/Tailscale），決定要開一個安全的對外入口還是透過 Tailscale，並在 `docs/architecture.md` 記錄決定與理由
- [ ] 把 BlueMap 地圖嵌入網站一個新頁面/區塊，限制只有登入後才能看到連結或 iframe
- [ ] `/api/trade-posts`：`GET` 列出交易貼文、`POST`（需登入）新增一則貼文（例如「我有鑽石想換鐵」），純文字配對，**不會**透過任何方式真的操作遊戲內物品
- [ ] 前端交易看板頁面：列表呈現、張貼表單，一樣要做 XSS 防護與輸入驗證

**本週 Web 概念**
_待填_

**除錯紀錄**
_待填_

**心得**
_待填_

---

## W13 — Session/Cookie 設計定案 + 程式結構整理 + 管理後台整合評估

**本週目標**：對應課程 W10（Session/Cookie 狀態管理），把登入狀態保存方式定案；把目前累積的多個功能程式整理乾淨；評估管理後台整合的範圍。

**完成清單**
- [ ] 決定並實作 session/cookie（或 JWT）保存登入狀態的具體做法，設定 `httponly`/`secure`/`samesite`，並說明為什麼選這個而不是另一個（對應課程 W08 OAuth 概念比較）
- [ ] 把 `server.py` 依功能拆成多個 router 模組（auth / status / whitelist / chat / trade），`database.py`/`models.py` 的資料庫 schema 定稿
- [ ] 評估「管理員登入 + 白名單審核頁」要做到什麼程度：獨立做一個簡化版，還是串接 Mac mini 既有 `panel/` 的 auth（**不**串接其中的 RCON/世界管理等高危功能），並記錄決定理由
- [ ] 視時間決定是否實作管理員審核頁（把原本「手動看 JSON 檔案」換成網頁介面）

**本週 Web 概念**
_待填_

**除錯紀錄**
_待填_

**心得**
_待填_

---

## W14 — 資安檢查清單 + 端到端測試 + 選配的通知/圖表

**本週目標**：對應課程 W12（部署前資安檢查清單），在正式收尾前做一次完整檢查，並視時間補上簡報提過的加分項目。

**完成清單**
- [ ] 資安檢查：密碼雜湊方式複查、cookie/session 設定、CSRF 風險評估、`SECRET_KEY` 等敏感設定改用環境變數，不寫死在程式碼或進 git
- [ ] 完整走一次「註冊 → 登入 → 查詢伺服器狀態 → 申請白名單 → 聊天 → 交易看板 → 看地圖 → 登出」流程，記錄測試結果（含故意測試失敗情境、未登入時各功能是否真的被擋下來）
- [ ] （時間允許再做）Discord webhook 通知：伺服器上下線、白名單核准時發通知
- [ ] （時間允許再做）在線人數歷史圖表：定期記錄 `/api/status` 查詢結果，畫成簡單折線圖

**本週 Web 概念**
_待填_

**除錯紀錄**
_待填_

**心得**
_待填_

---

## W15 — 正式部署驗證 + 文件與展示收尾

**本週目標**：確保公開網址上的最終版本真的能動，並把文件/簡報更新成跟實作一致，準備期末展示。

**完成清單**
- [ ] 透過 IIS 反向代理的公開網址重新測試整個流程（所有功能都要測，不只首頁），確認沒有 CORS、路徑、cookie-domain 等部署後才會出現的問題
- [ ] 更新 `README.md`、`docs/proposal.md`/`architecture.md`/`security.md` 反映最終實際功能
- [ ] 把簡報（roadmap 投影片）更新成「已完成」vs「未完成」的對照，確認跟實作一致
- [ ] 準備期末展示 demo 流程（示範順序、要秀哪些功能、備用方案如果網路臨時出問題）

**本週 Web 概念**
_待填_

**除錯紀錄**
_待填_

**心得**
_待填_
