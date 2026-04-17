# AI Image & Video Generator - Wasmer Edge 部署說明

## 專案結構

```
├── wasmer.toml          # Wasmer 配置
├── app.py               # Python 後端入口
├── requirements.txt     # Python 依賴
├── static/
│   ├── index.html       # 前端頁面
│   ├── style.css        # 樣式表
│   └── script.js        # 前端邏輯
└── README-WASMER.md     # 本說明文件
```

## 部署步驟

### 1. 安裝 Wasmer CLI

```bash
# macOS/Linux
curl https://get.wasmer.io -sSf | sh

# Windows (PowerShell)
iwr https://win.wasmer.io -useb | iex
```

### 2. 登入 Wasmer

```bash
wasmer login
```

### 3. 設定環境變數

在 Wasmer Dashboard 或 CLI 設定 API Key：

```bash
wasmer app config set API_KEY "gk-3c25e655bf951d96aca89b240bfdf9515987416c6591319a"
```

### 4. 部署

```bash
wasmer deploy
```

### 5. 查看部署狀態

```bash
wasmer app logs
```

## 本地測試

```bash
# 設定環境變數
export API_KEY="gk-3c25e655bf951d96aca89b240bfdf9515987416c6591319a"

# 執行 Python 伺服器
python app.py
```

開啟瀏覽器訪問 `http://localhost:8080`

## Wasmer vs Cloudflare Workers

| 功能 | Wasmer Edge | Cloudflare Workers |
|------|-------------|-------------------|
| 語言 | Python/Rust/Wasm | JavaScript |
| 免費額度 | 有限制 | 100K req/日 |
| 部署難度 | 中等 | 簡單 |
| 全球 CDN | ✅ | ✅ |
| 環境變數 | Dashboard/CLI | Dashboard |

## 注意事項

1. **API Key 安全**：請勿將 API Key 直接寫入程式碼，務必使用環境變數
2. **靜態資源**：已複製到 `static/` 目錄，修改後需重新複製
3. **Python 版本**：需要 Python 3.11+

## 疑難排解

### 部署失敗
```bash
# 檢查配置
wasmer app validate

# 查看日誌
wasmer app logs --tail
```

### 本地無法啟動
```bash
# 確認 Python 版本
python --version

# 確認靜態檔案存在
dir static
```

## 授權

MIT License