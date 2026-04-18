# AI Image & Video Generator

一個支援四種生成類型的 AI 圖片/影片生成器。

## 功能

- **文字生圖** (Text → Image): 從文字描述生成圖片
- **圖片編輯** (Image → Image Edit): 編輯/轉換現有圖片
- **文字生影片** (Text → Video): 從文字生成影片
- **圖片生影片** (Image → Video): 將靜態圖片動畫化

## 部署到 Vercel

### 方法 1: 透過 Vercel CLI

1. 安裝 Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. 登入 Vercel:
   ```bash
   vercel login
   ```

3. 部署:
   ```bash
   vercel
   ```

### 方法 2: 透過 GitHub 整合

1. 將此專案推送到 GitHub
2. 在 [Vercel Dashboard](https://vercel.com) 匯入專案
3. 設定環境變數

## 環境變數

在 Vercel Dashboard 設定以下環境變數：

| 變數名稱 | 說明 | 範例 |
|---------|------|------|
| `API_KEY` | API 金鑰 | `gk-xxx...` |
| `API_BASE` | API 端點 | `https://xxx.trycloudflare.com/v1` |
| `IMAGE_MODEL` | 圖片模型 | `grok-imagine-image` |
| `VIDEO_MODEL` | 影片模型 | `grok-imagine-video` |

## 本地開發

```bash
# 安裝 Vercel CLI
npm install -g vercel

# 本地執行
vercel dev
```

或使用 Python 直接執行：

```bash
python app.py
```

## 專案結構

```
├── api/
│   └── index.py        # Vercel serverless function
├── static/
│   ├── index.html      # 前端頁面
│   ├── script.js       # 前端邏輯
│   └── style.css       # 樣式
├── app.py              # 本地 Python 伺服器
├── vercel.json         # Vercel 配置
├── wasmer.toml         # Wasmer 配置（已棄用）
└── .env                # 環境變數（本地）
```

## 授權

MIT
