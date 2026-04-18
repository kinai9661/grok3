// 語言切換
let currentLang = 'zh';

// API 設定管理
const SETTINGS_KEY = 'ai_generator_settings';

// 預設設定（從後端載入）
let defaultSettings = {
    api_base: '',
    image_model: '',
    video_model: '',
    has_api_key: false
};

// 載入後端預設配置
async function loadDefaultSettings() {
    try {
        const response = await fetch('/api/config');
        if (response.ok) {
            defaultSettings = await response.json();
        }
    } catch (e) {
        console.log('Using local settings only');
    }
}

// 取得用戶設定
function getSettings() {
    try {
        const saved = localStorage.getItem(SETTINGS_KEY);
        return saved ? JSON.parse(saved) : {};
    } catch {
        return {};
    }
}

// 儲存用戶設定
function saveSettings(settings) {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

// 取得有效的 API 配置（優先使用用戶設定）
function getEffectiveConfig() {
    const userSettings = getSettings();
    return {
        api_base: userSettings.api_base || defaultSettings.api_base,
        api_key: userSettings.api_key || '',
        image_model: userSettings.image_model || defaultSettings.image_model,
        video_model: userSettings.video_model || defaultSettings.video_model
    };
}

const translations = {
zh: {
    title: 'AI 圖片 & 影片 生成',
    labelPrompt: '描述文字 (Prompt)：',
    labelType: '生成類型：',
    image: '圖片',
    video: '影片',
    videoOptionsTitle: '影片進階選項',
    labelVideoDuration: '影片長度：',
    labelVideoResolution: '解析度：',
    labelVideoStyle: '影片風格：',
    default: '預設',
    cinematic: '電影感',
    vlog: 'Vlog',
    animation: '動畫',
    imageOptionsTitle: '圖片進階選項',
    labelImageSize: '圖片尺寸：',
    labelImageCount: '生成數量：',
    i2iTitle: '圖片生圖 (Image-to-Image)',
    i2iHint: '上傳一張參考圖片，AI 將基於該圖片進行風格轉換或修改',
    uploadText: '📁 選擇參考圖片',
    clearImage: '清除圖片',
    submitBtn: '產生',
    historyTitle: '生成記錄',
    clearHistory: '清除記錄',
    loadingImage: '正在生成圖片，請稍候',
    loadingVideo: '正在生成影片，請稍候',
    successImage: '圖片生成成功！',
    successVideo: '影片生成成功！',
    errorNoPrompt: '請輸入描述文字',
    errorGenerate: '生成失敗',
    errorNoResult: '無法取得生成結果',
    historyEmpty: '尚無生成記錄',
    sec: '秒',
    images: '張',
    textToImage: '文字生圖',
    imageEdit: '圖片編輯',
    textToVideo: '文字生影片',
    imageToVideo: '圖片生影片',
    uploadTitle: '上傳參考圖片',
    uploadHint: '請上傳一張圖片作為參考',
    labelVideoAspectRatio: '比例：',
    labelImageResolution: '解析度：',
    settingsTitle: 'API 設定',
    labelApiBase: 'API Base URL：',
    labelApiKey: 'API Key：',
    labelImageModel: '圖片模型：',
    labelVideoModel: '影片模型：',
    saveSettings: '儲存設定',
    resetSettings: '重置',
    settingsHint: '提示：設定會儲存在瀏覽器本地，重新載入頁面後仍會保留。',
    settingsSaved: '設定已儲存！',
    settingsReset: '設定已重置！'
},
en: {
    title: 'AI Image & Video Generator',
    labelPrompt: 'Prompt:',
    labelType: 'Type:',
    image: 'Image',
    video: 'Video',
    videoOptionsTitle: 'Video Options',
    labelVideoDuration: 'Duration:',
    labelVideoResolution: 'Resolution:',
    labelVideoStyle: 'Style:',
    default: 'Default',
    cinematic: 'Cinematic',
    vlog: 'Vlog',
    animation: 'Animation',
    imageOptionsTitle: 'Image Options',
    labelImageSize: 'Size:',
    labelImageCount: 'Count:',
    i2iTitle: 'Image-to-Image',
    i2iHint: 'Upload a reference image for style transfer or modification',
    uploadText: '📁 Select Reference Image',
    clearImage: 'Clear',
    submitBtn: 'Generate',
    historyTitle: 'History',
    clearHistory: 'Clear History',
    loadingImage: 'Generating image, please wait',
    loadingVideo: 'Generating video, please wait',
    successImage: 'Image generated successfully!',
    successVideo: 'Video generated successfully!',
    errorNoPrompt: 'Please enter a prompt',
    errorGenerate: 'Generation failed',
    errorNoResult: 'Unable to get result',
    historyEmpty: 'No history yet',
    sec: 'sec',
    images: 'images',
    textToImage: 'Text → Image',
    imageEdit: 'Image → Image (Edit)',
    textToVideo: 'Text → Video',
    imageToVideo: 'Image → Video',
    uploadTitle: 'Upload Reference Image',
    uploadHint: 'Please upload an image as reference',
    labelVideoAspectRatio: 'Aspect Ratio:',
    labelImageResolution: 'Resolution:',
    settingsTitle: 'API Settings',
    labelApiBase: 'API Base URL:',
    labelApiKey: 'API Key:',
    labelImageModel: 'Image Model:',
    labelVideoModel: 'Video Model:',
    saveSettings: 'Save',
    resetSettings: 'Reset',
    settingsHint: 'Settings are saved locally in your browser.',
    settingsSaved: 'Settings saved!',
    settingsReset: 'Settings reset!'
}
};

function updateLanguage(lang) {
    currentLang = lang;
    const t = translations[lang];

    // 更新標題和標籤
    document.getElementById('title').textContent = t.title;
    document.getElementById('labelPrompt').textContent = t.labelPrompt;
    document.getElementById('labelType').textContent = t.labelType;
    document.getElementById('videoOptionsTitle').textContent = t.videoOptionsTitle;
    document.getElementById('labelVideoDuration').textContent = t.labelVideoDuration;
    document.getElementById('labelVideoResolution').textContent = t.labelVideoResolution;
    document.getElementById('labelVideoStyle').textContent = t.labelVideoStyle;
    document.getElementById('imageOptionsTitle').textContent = t.imageOptionsTitle;
    document.getElementById('labelImageSize').textContent = t.labelImageSize;
    document.getElementById('labelImageCount').textContent = t.labelImageCount;
    document.getElementById('uploadText').textContent = t.uploadText;
    document.getElementById('clearImage').textContent = t.clearImage;
    document.getElementById('submitBtn').textContent = t.submitBtn;
    document.getElementById('historyTitle').textContent = t.historyTitle;
    document.getElementById('clearHistory').textContent = t.clearHistory;

    // 更新設定面板
    document.getElementById('settingsTitle').textContent = t.settingsTitle;
    document.getElementById('labelApiBase').textContent = t.labelApiBase;
    document.getElementById('labelApiKey').textContent = t.labelApiKey;
    document.getElementById('labelImageModel').textContent = t.labelImageModel;
    document.getElementById('labelVideoModel').textContent = t.labelVideoModel;
    document.getElementById('saveSettings').textContent = t.saveSettings;
    document.getElementById('resetSettings').textContent = t.resetSettings;
    document.getElementById('settingsHint').textContent = t.settingsHint;
    
    // 更新下拉選單選項
    const typeSelect = document.getElementById('type');
    typeSelect.options[0].text = t.textToImage;
    typeSelect.options[1].text = t.imageEdit;
    typeSelect.options[2].text = t.textToVideo;
    typeSelect.options[3].text = t.imageToVideo;
    
    const videoStyleSelect = document.getElementById('videoStyle');
    videoStyleSelect.options[0].text = t.default;
    videoStyleSelect.options[1].text = t.cinematic;
    videoStyleSelect.options[2].text = t.vlog;
    videoStyleSelect.options[3].text = t.animation;
    
    const imageCountSelect = document.getElementById('imageCount');
    for (let i = 0; i < 4; i++) {
        imageCountSelect.options[i].text = `${i + 1} ${t.images}`;
    }
    
    // 更新上傳區域文字
    const uploadTitle = document.getElementById('uploadTitle');
    const uploadHint = document.getElementById('uploadHint');
    if (uploadTitle) uploadTitle.textContent = t.uploadTitle;
    if (uploadHint) uploadHint.textContent = t.uploadHint;
    const labelVideoAspectRatio = document.getElementById('labelVideoAspectRatio');
    const labelImageResolution = document.getElementById('labelImageResolution');
    if (labelVideoAspectRatio) labelVideoAspectRatio.textContent = t.labelVideoAspectRatio;
    if (labelImageResolution) labelImageResolution.textContent = t.labelImageResolution;
    
    // 更新按鈕狀態
    document.getElementById('langZh').classList.toggle('active', lang === 'zh');
    document.getElementById('langEn').classList.toggle('active', lang === 'en');
    
    // 重新渲染歷史記錄
    renderHistory();
}

// 語言切換按鈕事件
document.getElementById('langZh').addEventListener('click', () => updateLanguage('zh'));
document.getElementById('langEn').addEventListener('click', () => updateLanguage('en'));

// 類型切換邏輯
function updateTypeUI(type) {
    const videoOpts = document.getElementById('videoOptions');
    const imageOpts = document.getElementById('imageOptions');
    const uploadSection = document.getElementById('imageUploadSection');
    
    // 是否為影片類型
    const isVideo = (type === 'text-to-video' || type === 'image-to-video');
    // 是否需要上傳圖片
    const needsImage = (type === 'image-edit' || type === 'image-to-video');
    
    videoOpts.style.display = isVideo ? 'block' : 'none';
    imageOpts.style.display = isVideo ? 'none' : 'block';
    uploadSection.style.display = needsImage ? 'block' : 'none';
}

document.getElementById('type').addEventListener('change', function () {
    updateTypeUI(this.value);
});

// 初始顯示根據預設類型
updateTypeUI(document.getElementById('type').value);

// 圖片預覽與清除
const referenceInput = document.getElementById('referenceImage');
const previewDiv = document.getElementById('imagePreview');
const clearBtn = document.getElementById('clearImage');
const uploadText = document.getElementById('uploadText');

referenceInput.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function (e) {
        previewDiv.innerHTML = '<img src="' + e.target.result + '" alt="Reference" class="preview-img" />';
        clearBtn.style.display = 'inline-block';
        uploadText.textContent = currentLang === 'zh' ? '已選擇圖片' : 'Image selected';
    };
    reader.readAsDataURL(file);
});

clearBtn.addEventListener('click', function () {
    referenceInput.value = '';
    previewDiv.innerHTML = '';
    this.style.display = 'none';
    uploadText.textContent = translations[currentLang].uploadText;
});

// 歷史記錄管理
const HISTORY_KEY = 'ai_generator_history';
const EXPIRE_DAYS = 15; // 保留 15 天

function getHistory() {
    try {
        return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
    } catch {
        return [];
    }
}

function saveHistory(history) {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}

// 清除過期記錄（超過 15 天）
function cleanExpiredHistory() {
    const history = getHistory();
    const now = Date.now();
    const expireTime = EXPIRE_DAYS * 24 * 60 * 60 * 1000; // 15 天的毫秒數
    const filtered = history.filter(item => (now - item.timestamp) < expireTime);
    if (filtered.length !== history.length) {
        saveHistory(filtered);
    }
    return filtered;
}

function addToHistory(item) {
    let history = getHistory();
    // 清除過期記錄
    history = cleanExpiredHistory();
    history.unshift(item);
    // 最多保留 50 筆
    if (history.length > 50) history.pop();
    saveHistory(history);
    renderHistory();
}

function clearAllHistory() {
    localStorage.removeItem(HISTORY_KEY);
    renderHistory();
}

// 刪除單筆記錄
function deleteHistoryItem(index) {
    const history = getHistory();
    history.splice(index, 1);
    saveHistory(history);
    renderHistory();
}

function renderHistory() {
    const historyList = document.getElementById('historyList');
    // 清除過期記錄
    const history = cleanExpiredHistory();
    const t = translations[currentLang];

    if (history.length === 0) {
        historyList.innerHTML = '<div class="history-empty">' + t.historyEmpty + '</div>';
        return;
    }

    const deleteLabel = currentLang === 'zh' ? '刪除' : 'Delete';
    
    historyList.innerHTML = history.map((item, index) => {
        const typeLabel = item.type === 'video' ? t.video : t.image;
        const typeClass = item.type === 'video' ? 'video' : 'image';
        const timeStr = new Date(item.timestamp).toLocaleString(currentLang === 'zh' ? 'zh-TW' : 'en-US');

        let contentHtml = '';
        if (item.type === 'video') {
            contentHtml = '<video controls muted style="max-width:100%;max-height:200px;border-radius:8px;"><source src="' + item.url + '" type="video/mp4"></video>';
        } else {
            contentHtml = '<img src="' + item.url + '" alt="Generated" style="max-width:100%;max-height:200px;border-radius:8px;cursor:pointer;" onclick="window.open(\'' + item.url + '\', \'_blank\')" />';
        }

        return '<div class="history-item">' +
            '<div class="history-item-header">' +
            '<span class="history-item-type ' + typeClass + '">' + typeLabel + '</span>' +
            '<span class="history-item-time">' + timeStr + '</span>' +
            '<button class="history-item-delete" onclick="deleteHistoryItem(' + index + ')" title="' + deleteLabel + '">×</button>' +
            '</div>' +
            '<div class="history-item-prompt">' + item.prompt + '</div>' +
            '<div class="history-item-content">' + contentHtml + '</div>' +
            '</div>';
    }).join('');
}

// 清除歷史記錄按鈕
document.getElementById('clearHistory').addEventListener('click', clearAllHistory);

// 初始渲染歷史記錄
renderHistory();

// 表單提交
document.getElementById('genForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const prompt = document.getElementById('prompt').value.trim();
    const type = document.getElementById('type').value;
    const resultDiv = document.getElementById('result');
    const submitBtn = document.getElementById('submitBtn');
    const t = translations[currentLang];
    
    if (!prompt) {
        resultDiv.innerHTML = '<div class="error">' + t.errorNoPrompt + '</div>';
        return;
    }
    
    // 取得進階參數和 API 配置
    const config = getEffectiveConfig();
    const payload = { prompt, type };
    
    // 加入 API 配置
    if (config.api_base) payload.api_base = config.api_base;
    if (config.api_key) payload.api_key = config.api_key;
    if (config.image_model) payload.image_model = config.image_model;
    if (config.video_model) payload.video_model = config.video_model;
    
    // 判斷是否為影片類型
    const isVideo = (type === 'text-to-video' || type === 'image-to-video');
    const needsImage = (type === 'image-edit' || type === 'image-to-video');
    
    if (isVideo) {
        payload.duration = parseInt(document.getElementById('videoDuration').value, 10);
        payload.resolution = document.getElementById('videoResolution').value;
        payload.aspect_ratio = document.getElementById('videoAspectRatio').value;
        payload.style = document.getElementById('videoStyle').value;
    } else {
        payload.size = document.getElementById('imageSize').value;
        payload.n = parseInt(document.getElementById('imageCount').value, 10);
        payload.resolution = document.getElementById('imageResolution').value;
    }
    
    // 需要圖片的類型（image-edit, image-to-video）
    if (needsImage) {
        if (!referenceInput.files[0]) {
            resultDiv.innerHTML = '<div class="error">' + (currentLang === 'zh' ? '請上傳參考圖片' : 'Please upload a reference image') + '</div>';
            return;
        }
        const file = referenceInput.files[0];
        const base64 = await new Promise((res) => {
            const r = new FileReader();
            r.onload = () => res(r.result.split(',')[1]);
            r.readAsDataURL(file);
        });
        payload.reference_image = base64;
    }
    
    // 顯示載入中
    const loadingMsg = isVideo ? t.loadingVideo : t.loadingImage;
    resultDiv.innerHTML = '<div class="loading">' + loadingMsg + '</div>';
    submitBtn.disabled = true;
    submitBtn.textContent = currentLang === 'zh' ? '生成中...' : 'Generating...';
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || t.errorGenerate);
        
        // 處理多張圖片
        const urls = (data.data || []).map(item => item.url).filter(Boolean);
        if (urls.length === 0) throw new Error(t.errorNoResult);
    
        // 加入歷史記錄（每張圖片都加入）
        // 歷史記錄中統一用 video/image 類型分類
        const historyType = isVideo ? 'video' : 'image';
        urls.forEach(url => {
            addToHistory({
                type: historyType,
                prompt: prompt,
                url: url,
                timestamp: Date.now()
            });
        });
    
        if (isVideo) {
            resultDiv.innerHTML = '<div class="success">' + t.successVideo + '</div><video controls autoplay muted loop><source src="' + urls[0] + '" type="video/mp4">' + (currentLang === 'zh' ? '您的瀏覽器不支援影片播放' : 'Your browser does not support video playback') + '</video>';
        } else {
            // 顯示多張圖片
            let imagesHtml = '<div class="success">' + t.successImage + '</div><div class="generated-images">';
            urls.forEach(url => {
                imagesHtml += '<img src="' + url + '" alt="Generated" style="cursor:pointer;max-width:100%;border-radius:8px;margin:5px;" onclick="window.open(\'' + url + '\', \'_blank\')" />';
            });
            imagesHtml += '</div>';
            resultDiv.innerHTML = imagesHtml;
        }
    } catch (err) {
        resultDiv.innerHTML = '<div class="error">' + (currentLang === 'zh' ? '錯誤：' : 'Error: ') + err.message + '</div>';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = t.submitBtn;
    }
});

// 設定面板切換
document.getElementById('settingsBtn').addEventListener('click', function() {
    const panel = document.getElementById('settingsPanel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    
    // 載入目前設定到表單
    if (panel.style.display === 'block') {
        const settings = getSettings();
        document.getElementById('apiBase').value = settings.api_base || defaultSettings.api_base || '';
        document.getElementById('apiKey').value = settings.api_key || '';
        document.getElementById('imageModel').value = settings.image_model || defaultSettings.image_model || '';
        document.getElementById('videoModel').value = settings.video_model || defaultSettings.video_model || '';
    }
});

// 儲存設定
document.getElementById('saveSettings').addEventListener('click', function() {
    const settings = {
        api_base: document.getElementById('apiBase').value.trim(),
        api_key: document.getElementById('apiKey').value.trim(),
        image_model: document.getElementById('imageModel').value.trim(),
        video_model: document.getElementById('videoModel').value.trim()
    };
    saveSettings(settings);
    alert(translations[currentLang].settingsSaved);
});

// 重置設定
document.getElementById('resetSettings').addEventListener('click', function() {
    localStorage.removeItem(SETTINGS_KEY);
    document.getElementById('apiBase').value = defaultSettings.api_base || '';
    document.getElementById('apiKey').value = '';
    document.getElementById('imageModel').value = defaultSettings.image_model || '';
    document.getElementById('videoModel').value = defaultSettings.video_model || '';
    alert(translations[currentLang].settingsReset);
});

// 初始化：載入預設設定
loadDefaultSettings();