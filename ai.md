# AI 協作反思紀錄 (ai.md)

> 不需記錄每一次對話，只記錄重要的決策/經驗/洞察。
> 格式：問題 → AI 的建議 → 我如何驗證 → 採納或拒絕（及理由）

## W01

_待填：本週向 AI 提出的重要問題與反思。_

## W02

_待填_

## W03

- **問題**：`server.py` 裡的 `FastAPI(ROOT_PATH="/s112213070")` 是不是就能讓助教的 IIS 反向代理正確運作？
  **AI 建議**：FastAPI 建構子的參數是小寫 `root_path`，大寫寫法不會報錯但也不會真的生效（會被當成未知的額外參數靜默忽略），建議改成 `root_path=os.getenv("ROOT_PATH", "")`，並且部署前綴應該用環境變數在啟動時注入，而不是寫死在程式碼裡。
  **驗證方式**：直接寫一段 Python 建立 `FastAPI(ROOT_PATH=...)` 物件，印出 `app.root_path`，實測確實是空字串 `''`；改成小寫 `root_path=os.getenv(...)` 後再測一次，設了環境變數就能正確讀到值。
  **決定**：採納，改用 `os.getenv("ROOT_PATH", "")`。理由：這樣本機測試不用特別設環境變數也能跑，正式部署時再用環境變數覆蓋，也避免以後手滑同時設了 `--root-path` CLI 參數造成衝突。

- **問題**：`sites/index.html` 用相對路徑引用 `css/style.css`、`js/app.js`，為什麼實際載入會 404？
  **AI 建議**：檢查 `StaticFiles` 掛載的實際目錄（`sites/`），確認 `css/`、`js/` 資料夾是否真的在這個目錄底下。
  **驗證方式**：實際啟動 uvicorn，用 `curl` 打 `/css/style.css`、`/js/app.js`，確認回應狀態碼不是 200。
  **決定**：採納，把 `css/`、`js/` 整個搬進 `sites/` 底下，重測後兩個檔案都回 200。

- **問題**：為什麼改了 `ROOT_PATH` 環境變數、重新整理瀏覽器後，`/api/docs` 頁面的 Servers 下拉選單還是沒有出現？
  **AI 建議**：這是 FastAPI 把 OpenAPI schema 快取在 process 第一次生成時的行為，不是程式碼寫錯；只要同一個 process 內第一次請求時 `root_path` 是空的，之後都會回傳同一份沒有 servers 的快取，必須整個重啟 uvicorn process 才會重新產生 schema。
  **驗證方式**：請 AI 找出 FastAPI 原始碼中 `openapi()`／`setup()` 的邏輯來源，確認 `self.openapi_schema` 只在第一次呼叫時建立。
  **決定**：採納這個解釋，之後只要變更 `ROOT_PATH` 就整個重開一次 PowerShell 視窗、重啟 uvicorn，而不是只重新整理頁面。

## W04

- **問題**：期末專案題目「Python 程式碼學習網」被教授否決，沒有方向，AI能提供什麼具體建議？
  **AI 建議**：不要急著換一個完全不同的類別，而是找「有具體真實使用者」的場景；逐步訪談後聚焦到我自己在Mac mini上已經在維運的Minecraft伺服器——這是別人不可能複製的素材，而且剛好能對應課程剩下幾週的主題（fetch/表單/JWT）。
  **驗證方式**：SSH連進Mac mini實際檢視現有的`panel/`（776行、有auth、有自動化測試），確認這套基礎設施是真實存在、可以當作素材的。
  **決定**：採納，確定新主題為「Minecraft伺服器玩家入口網站」。

- **問題**：要做的公開網站要不要直接擴充/連結既有的私人管理後台（`panel/`，含RCON console等高危操作）？
  **AI 建議**：不要。管理後台本身就不該公開在網路上；應該做一個全新、刻意簡化、唯讀為主的公開網站，查詢伺服器狀態直接走Minecraft本來就公開不需認證的Server List Ping協定，跟管理後台完全不互通。
  **驗證方式**：實際查了`panel/panel.py`的ROUTES，確認裡面有RCON、世界刪除、備份還原這類危險操作，證實不該對外暴露。
  **決定**：採納，公開網站跟Mac mini的admin panel完全分離，只用`mcstatus`查公開的伺服器狀態。

- **問題**：查詢Minecraft伺服器即時狀態，要自己寫Server List Ping協定的socket/varint解析，還是用現成套件？
  **AI 建議**：用`mcstatus`套件。自己刻意把精力放在Web概念（fetch/API設計）而不是遊戲網路協定的二進位格式，比較符合這門課的重點。
  **驗證方式**：實際`pip install mcstatus`後在本機對真實的`schmidt-lawsuits.tun.ply.gg`查詢，確實能拿到正確的在線人數跟MOTD。
  **決定**：採納，使用`mcstatus`。

## W05

_待填：這週登入/註冊頁面的 CSS 是用 Copilot 設計的，向它下了什麼指令、它給了什麼建議、怎麼驗證/取捨，由你自己填寫。_
