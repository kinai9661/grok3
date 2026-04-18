"""
AI Image & Video Generator - Wasmer Edge Backend
Python HTTP server for handling API requests
"""

import json
import urllib.request
import urllib.error
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Load .env file if exists
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env()

# 預設配置（從環境變數讀取）
DEFAULT_API_BASE = os.environ.get("API_BASE", "https://api.openai.com/v1")
DEFAULT_API_KEY = os.environ.get("API_KEY", "")
DEFAULT_IMAGE_MODEL = os.environ.get("IMAGE_MODEL", "dall-e-3")
DEFAULT_VIDEO_MODEL = os.environ.get("VIDEO_MODEL", "")

# CORS headers
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-API-Key, X-API-Base",
}

# Read static files
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

# API handler
def handle_generate(body, headers=None):
    try:
        data = json.loads(body)
        prompt = data.get("prompt")
        gen_type = data.get("type", "text-to-image")  # 新增四種類型

        if not prompt:
            return {"error": "Missing prompt parameter"}, 400

        # 支援前端傳入的 API 配置，若無則使用預設值
        api_key = data.get("api_key") or DEFAULT_API_KEY
        api_base = data.get("api_base") or DEFAULT_API_BASE
        image_model = data.get("image_model") or DEFAULT_IMAGE_MODEL
        video_model = data.get("video_model") or DEFAULT_VIDEO_MODEL

        if not api_key:
            return {"error": "API Key not configured"}, 500

        # 根據生成類型選擇端點和建構 payload
        # 四種類型: text-to-image, image-edit, text-to-video, image-to-video
        
        if gen_type == "text-to-video":
            # Text → Video
            endpoint = f"{api_base}/videos/generations"
            duration = data.get("duration", 5)
            resolution = data.get("resolution", "480p")
            aspect_ratio = data.get("aspect_ratio", "16:9")
            style = data.get("style", "")

            payload = {
                "prompt": prompt,
                "model": video_model or "grok-imagine-video",
                "duration": duration,
                "resolution": resolution,
                "aspect_ratio": aspect_ratio
            }

            # Style mapping
            style_map = {
                "cinematic": "cinematic style, film look, dramatic lighting",
                "vlog": "vlog style, casual, handheld camera feel",
                "animation": "animated style, cartoon, vibrant colors"
            }
            if style and style in style_map:
                payload["prompt"] = f"{prompt}, {style_map[style]}"

        elif gen_type == "image-to-video":
            # Image → Video
            endpoint = f"{api_base}/videos/generations"
            duration = data.get("duration", 5)
            resolution = data.get("resolution", "480p")
            aspect_ratio = data.get("aspect_ratio", "16:9")
            reference_image = data.get("reference_image")

            if not reference_image:
                return {"error": "Reference image required for image-to-video"}, 400

            payload = {
                "prompt": prompt,
                "model": video_model or "grok-imagine-video",
                "duration": duration,
                "resolution": resolution,
                "aspect_ratio": aspect_ratio,
                "image": {
                    "url": f"data:image/jpeg;base64,{reference_image}"
                }
            }

        elif gen_type == "image-edit":
            # Image → Image (Edit)
            endpoint = f"{api_base}/images/edits"
            size = data.get("size", "1024x1024")
            n = data.get("n", 1)
            resolution = data.get("resolution", "1k")
            reference_image = data.get("reference_image")

            if not reference_image:
                return {"error": "Reference image required for image-edit"}, 400

            payload = {
                "prompt": prompt,
                "n": n,
                "model": image_model,
                "resolution": resolution,
                "image": {
                    "url": f"data:image/jpeg;base64,{reference_image}"
                }
            }

        else:
            # Text → Image (預設)
            endpoint = f"{api_base}/images/generations"
            size = data.get("size", "1024x1024")
            n = data.get("n", 1)

            payload = {
                "prompt": prompt,
                "n": n,
                "model": image_model
            }
            if size:
                payload["size"] = size

        # Make request to external API
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result, 200

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_data = json.loads(error_body)
            return {"error": error_data.get("error", {}).get("message", "API request failed")}, e.code
        except:
            return {"error": "API request failed"}, e.code
    except Exception as e:
        return {"error": str(e)}, 500


class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logging
    
    def send_cors_headers(self):
        for key, value in CORS_HEADERS.items():
            self.send_header(key, value)
    
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Serve static files
        if path == "/" or path == "/index.html":
            content = read_file("static/index.html")
            if content:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        
        elif path == "/style.css":
            content = read_file("static/style.css")
            if content:
                self.send_response(200)
                self.send_header("Content-Type", "text/css; charset=utf-8")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        
        elif path == "/script.js":
            content = read_file("static/script.js")
            if content:
                self.send_response(200)
                self.send_header("Content-Type", "application/javascript; charset=utf-8")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

        # API 配置端點 - 返回預設配置（不包含 API Key）
        elif path == "/api/config":
            config = {
                "api_base": DEFAULT_API_BASE,
                "image_model": DEFAULT_IMAGE_MODEL,
                "video_model": DEFAULT_VIDEO_MODEL,
                "has_api_key": bool(DEFAULT_API_KEY)  # 只告知是否有設定，不暴露實際值
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(config).encode('utf-8'))

        else:
            self.send_response(404)
            self.send_cors_headers()
            self.end_headers()
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == "/api/generate":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            result, status_code = handle_generate(body)
            
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_cors_headers()
            self.end_headers()


def main():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print(f"Server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()