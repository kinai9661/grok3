"""
AI Image & Video Generator - Vercel Serverless Function
"""

import json
import urllib.request
import urllib.error
import os
from http.server import BaseHTTPRequestHandler

# 從環境變數讀取配置
DEFAULT_API_BASE = os.environ.get("API_BASE", "https://api.openai.com/v1")
DEFAULT_API_KEY = os.environ.get("API_KEY", "")
DEFAULT_IMAGE_MODEL = os.environ.get("IMAGE_MODEL", "dall-e-3")
DEFAULT_VIDEO_MODEL = os.environ.get("VIDEO_MODEL", "")


def handle_generate(body):
    """Handle image/video generation requests"""
    try:
        data = json.loads(body)
        prompt = data.get("prompt")
        gen_type = data.get("type", "text-to-image")

        if not prompt:
            return {"error": "Missing prompt parameter"}, 400

        api_key = data.get("api_key") or DEFAULT_API_KEY
        api_base = data.get("api_base") or DEFAULT_API_BASE
        image_model = data.get("image_model") or DEFAULT_IMAGE_MODEL
        video_model = data.get("video_model") or DEFAULT_VIDEO_MODEL

        if not api_key:
            return {"error": "API Key not configured"}, 500

        if gen_type == "text-to-video":
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

            style_map = {
                "cinematic": "cinematic style, film look, dramatic lighting",
                "vlog": "vlog style, casual, handheld camera feel",
                "animation": "animated style, cartoon, vibrant colors"
            }
            if style and style in style_map:
                payload["prompt"] = f"{prompt}, {style_map[style]}"

        elif gen_type == "image-to-video":
            endpoint = f"{api_base}/videos/generations"
            duration = data.get("duration", 5)
            resolution = data.get("resolution", "480p")
            aspect_ratio = data.get("aspect_ratio", "16:9")
            reference_image = data.get("reference_image")
            image_mime = data.get("image_mime", "jpeg")

            if not reference_image:
                return {"error": "Reference image required for image-to-video"}, 400

            payload = {
                "prompt": prompt,
                "model": video_model or "grok-imagine-video",
                "duration": duration,
                "resolution": resolution,
                "aspect_ratio": aspect_ratio,
                "image": {
                    "url": f"data:image/{image_mime};base64,{reference_image}"
                }
            }

        elif gen_type == "image-edit":
            endpoint = f"{api_base}/images/edits"
            n = data.get("n", 1)
            resolution = data.get("resolution", "1k")
            reference_image = data.get("reference_image")
            image_mime = data.get("image_mime", "jpeg")

            if not reference_image:
                return {"error": "Reference image required for image-edit"}, 400

            payload = {
                "prompt": prompt,
                "n": n,
                "model": image_model,
                "resolution": resolution,
                "image": {
                    "url": f"data:image/{image_mime};base64,{reference_image}"
                }
            }

        else:
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


class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        if self.path.endswith("/api/config") or "/config" in self.path:
            config = {
                "api_base": DEFAULT_API_BASE,
                "image_model": DEFAULT_IMAGE_MODEL,
                "video_model": DEFAULT_VIDEO_MODEL,
                "has_api_key": bool(DEFAULT_API_KEY)
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(config).encode('utf-8'))
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ''

        if self.path.endswith("/api/generate") or "/generate" in self.path:
            try:
                result, status_code = handle_generate(body)
                self._set_headers(status_code)
                self.wfile.write(json.dumps(result).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8'))
