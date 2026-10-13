# 企劃書 (Project Proposal)

> 參考格式：問題/動機 → 目的 → 需求 → 需求細節 → 需求總結 → 應用情境

## 專案名稱

Minecraft 伺服器玩家入口網站

## 1. Introduction

### 問題、動機 (Problem / Motivation)
我自己用 AI coding 在家裡的 Mac mini 上架設並維運一個 Minecraft 伺服器（Paper 26.3，已有 BlueMap 3D地圖、playit.gg 對外連線、自動備份等機制），平時給朋友一起玩。但目前朋友想加入時，只能私訊問我「伺服器有沒有開」「要怎麼連」「能不能把我加進白名單」，資訊完全沒有一個公開、固定的地方可以查，每次都要我手動回覆。

### 目的 (Purpose)
做一個對外公開的玩家入口網站，讓朋友可以自己查詢伺服器即時狀態（在不在線、幾個人在玩）、看到連線方式，並透過表單自行申請加入白名單，不用每次都私訊我詢問。

## 2. Team Members
個人專案，獨立完成開發、設計與展示。

## 3. Project Milestone（W02 學習單）

| 項目 | 內容 |
|---|---|
| 問題定義 | 朋友想加入自己架設的 Minecraft 伺服器時，連線資訊與白名單申請都要私訊詢問，沒有一個公開、固定的管道 |
| 目標使用者 | 想加入這個 Minecraft 伺服器的朋友 |
| 核心功能 | 伺服器介紹與連線資訊、即時狀態查詢（線上人數/MOTD）、白名單申請表單 |
| 資料 (Data) | 伺服器狀態透過 Minecraft 公開的 Server List Ping 協定即時查詢（不需認證）；白名單申請紀錄存成本機 JSON 檔案，供管理員（我自己）事後審核 |
| 外部依賴 | `mcstatus` 套件（查詢 Minecraft 伺服器狀態）；伺服器對外位址由現有的 playit.gg 隧道提供（`schmidt-lawsuits.tun.ply.gg`） |
| 資安/隱私 | 刻意不對外公開/連結既有的私人管理後台（RCON console、世界管理等高危操作）；白名單申請只送進「待審清單」，不會自動對伺服器執行任何指令；申請者的 Minecraft ID 需經格式驗證 |
| MVP（若僅剩4週） | 伺服器介紹頁 + 即時狀態查詢 + 白名單申請表單（待審清單）；管理員登入介面與自動化審核列為後續擴充項目 |

## 4. Service Design

### 架構
- **前端**：HTML/CSS/JS 靜態頁面（`sites/`），mobile-first 版面。
- **後端**：FastAPI（`server.py`），新增 `/api/status`、`/api/whitelist-apply` 兩個 API，其餘仍是純靜態檔案服務。
- **Minecraft 伺服器**：既有的 Mac mini 上的 Paper 伺服器，完全不需改動；後端透過 `mcstatus` 對其公開位址做 Server List Ping 查詢，跟 Minecraft 用戶端在多人列表顯示伺服器資訊用的是同一個機制，不需要任何認證或額外開洞。
- **私人管理後台**：既有的 `panel/`（Mac mini 上，port 8209），跟這個公開網站完全不互通，刻意保持分離。

### 流程圖
```
朋友開啟網站
 ├─ 查看連線資訊與即時狀態（在線人數/MOTD）
 │   └─ 前端 fetch /api/status → 後端用 mcstatus 查詢 Minecraft 伺服器 → 回傳JSON
 └─ 填寫白名單申請表單
     └─ 前端 fetch POST /api/whitelist-apply → 後端驗證格式 → 寫入 data/whitelist_requests.json
         └─ 管理員（我）事後查看清單，手動用既有的 ./ops/console.sh "whitelist add" 加入白名單
```

### 心智圖
```
                 Minecraft 玩家入口網站
                          |
   ┌──────────┬──────────┼──────────┬──────────┐
伺服器資訊    即時狀態      白名單申請    資安邊界
（連線位址/   （Server List  （表單+       （不連私人
版本說明）    Ping查詢）     待審清單）    管理後台）
```

## 5. 應用情境 (Application Scenarios)
1. **查詢在不在線**：朋友想玩之前，先打開網站看看伺服器現在是不是開著、有幾個人在線上。
2. **申請加入**：還沒被加入白名單的朋友，透過表單送出自己的 Minecraft ID，等待審核。
3. **管理員審核**：我（管理員）定期查看待審清單，確認後用既有的 `ops/console.sh` 手動加入白名單，不透過網站自動執行。

## 6. UI Design and Demo

預計展示頁面：
1. **首頁**——伺服器介紹、連線資訊、即時狀態 widget、白名單申請表單（目前規劃為單頁）。
2. **（未來擴充）管理員登入後台**——取代目前「手動看 JSON 檔案」的審核方式，對應課程後段 JWT/Session 主題。
