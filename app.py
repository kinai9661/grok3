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

API_BASE = "https://connector-consulting-solution-beginner.trycloudflare.com/v1"
API_KEY = os.environ.get("API_KEY", "")

# CORS headers
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

# Read static files
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

# API handler
def handle_generate(body):
    try:
        data = json.loads(body)
        prompt = data.get("prompt")
        gen_type = data.get("type", "image")
        
        if not prompt:
            return {"error": "Missing prompt parameter"}, 400
        
        if not API_KEY:
            return {"error": "API Key not configured"}, 500
        
        # Build payload
        if gen_type == "video":
            endpoint = f"{API_BASE}/videos/generations"
            duration = data.get("duration", 5)
            resolution = data.get("resolution", "480p")
            style = data.get("style", "")
            
            payload = {
                "prompt": prompt,
                "model": "grok-imagine-video",
                "duration": duration
            }
            
            # Style mapping
            style_map = {
                "cinematic": "cinematic style, film look, dramatic lighting",
                "vlog": "vlog style, casual, handheld camera feel",
                "animation": "animated style, cartoon, vibrant colors"
            }
            if style and style in style_map:
                payload["prompt"] = f"{prompt}, {style_map[style]}"
        else:
            endpoint = f"{API_BASE}/images/generations"
            size = data.get("size", "1024x1024")
            n = data.get("n", 1)
            
            payload = {
                "prompt": prompt,
                "n": n,
                "model": "grok-imagine-image"
            }
            if size:
                payload["size"] = size
        
        # Make request to external API
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {API_KEY}",
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