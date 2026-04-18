"""
AI Image & Video Generator - Vercel Serverless Function
"""

import json
import urllib.request
import urllib.error
import os

# 從環境變數讀取配置
DEFAULT_API_BASE = os.environ.get("API_BASE", "https://api.openai.com/v1")
DEFAULT_API_KEY = os.environ.get("API_KEY", "")
DEFAULT_IMAGE_MODEL = os.environ.get("IMAGE_MODEL", "dall-e-3")
DEFAULT_VIDEO_MODEL = os.environ.get("VIDEO_MODEL", "")

def handler(request):
    """Vercel serverless handler"""
    
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json"
    }
    
    # Handle OPTIONS preflight
    if request.method == "OPTIONS":
        return {
            "statusCode": 204,
            "headers": headers,
            "body": ""
        }
    
    # Handle GET requests
    if request.method == "GET":
        path = request.path
        
        # API config endpoint
        if path == "/api/config":
            config = {
                "api_base": DEFAULT_API_BASE,
                "image_model": DEFAULT_IMAGE_MODEL,
                "video_model": DEFAULT_VIDEO_MODEL,
                "has_api_key": bool(DEFAULT_API_KEY)
            }
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(config)
            }
        
        return {
            "statusCode": 404,
            "headers": headers,
            "body": json.dumps({"error": "Not found"})
        }
    
    # Handle POST requests
    if request.method == "POST":
        path = request.path
        
        if path == "/api/generate":
            try:
                body = request.body
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                
                result, status_code = handle_generate(body)
                return {
                    "statusCode": status_code,
                    "headers": headers,
                    "body": json.dumps(result)
                }
            except Exception as e:
                return {
                    "statusCode": 500,
                    "headers": headers,
                    "body": json.dumps({"error": str(e)})
                }
        
        return {
            "statusCode": 404,
            "headers": headers,
            "body": json.dumps({"error": "Not found"})
        }
    
    return {
        "statusCode": 405,
        "headers": headers,
        "body": json.dumps({"error": "Method not allowed"})
    }


def handle_generate(body):
    """Handle image/video generation requests"""
    try:
        data = json.loads(body)
        prompt = data.get("prompt")
        gen_type = data.get("type", "text-to-image")

        if not prompt:
            return {"error": "Missing prompt parameter"}, 400

        # 支援前端傳入的 API 配置
        api_key = data.get("api_key") or DEFAULT_API_KEY
        api_base = data.get("api_base") or DEFAULT_API_BASE
        image_model = data.get("image_model") or DEFAULT_IMAGE_MODEL
        video_model = data.get("video_model") or DEFAULT_VIDEO_MODEL

        if not api_key:
            return {"error": "API Key not configured"}, 500

        # 根據生成類型選擇端點
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
