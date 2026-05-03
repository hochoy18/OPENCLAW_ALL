#!/usr/bin/env python3
"""
v3推送：使用 wechat-article-publisher skill 的正确编码方式推送v2草稿
"""

import sys
import os
import re
import json
import requests
import tempfile
from pathlib import Path

# Load .env directly from wechat-article-publisher skill
env_file = Path('/home/hochoy/.openclaw/workspace-wechat-assistant/skills/wechat-article-publisher/.env')
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

APP_ID = os.environ.get('WECHAT_APP_ID', '')
APP_SECRET = os.environ.get('WECHAT_APP_SECRET', '')
print(f"[DEBUG] APP_ID={APP_ID}, APP_SECRET={APP_SECRET[:8]}...", file=sys.stderr)

HTML_FILE = '/opt/wechat/ai/workspace-wechat-shared/2026-04-02/article/2026-04-02-article-v2.html'
COVER_PATH = '/opt/wechat/ai/workspace-wechat-shared/2026-04-02/images/2026-04-02-img-1.png'
IMG_PATHS = [
    '/opt/wechat/ai/workspace-wechat-shared/2026-04-02/images/2026-04-02-img-1.png',
    '/opt/wechat/ai/workspace-wechat-shared/2026-04-02/images/2026-04-02-img-2.png',
    '/opt/wechat/ai/workspace-wechat-shared/2026-04-02/images/2026-04-02-img-3.png',
]

def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    r = requests.get(url).json()
    if 'access_token' not in r:
        raise Exception(f"Token failed: {r}")
    return r['access_token']

def upload_image(token, path):
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    with open(path, 'rb') as f:
        r = requests.post(url, files={'media': f}).json()
    url_val = r.get('url', '')
    print(f"[IMG] {path.split('/')[-1]} -> {url_val[:60]}...", file=sys.stderr)
    return url_val

def upload_thumb(token, path):
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=thumb"
    from PIL import Image
    img = Image.open(path).convert('RGB')
    tmp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    img.save(tmp.name, 'JPEG', quality=85)
    tmp.close()
    with open(tmp.name, 'rb') as f:
        r = requests.post(url, files={'media': f}).json()
    os.unlink(tmp.name)
    mid = r.get('media_id', '')
    print(f"[THUMB] {mid}", file=sys.stderr)
    return mid

def make_safe_title(title, max_units=20):
    total = 0
    for i, c in enumerate(title):
        total += 2 if ord(c) > 127 else 1
        if total > max_units:
            return title[:i]
    return title

def extract_digest(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:80].strip()

# --- Main ---
token = get_token()
print(f"[OK] Token: {token[:20]}...", file=sys.stderr)

# Read HTML
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract title
m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
title = m.group(1).strip() if m else '无标题'
print(f"[OK] Title: {title}", file=sys.stderr)

# Extract digest
body_start = html.find('<body>')
body_end = html.find('</body>')
body = html[body_start:body_end] if body_start != -1 else html
digest = extract_digest(body)
print(f"[OK] Digest ({len(digest)} chars): {digest[:50]}...", file=sys.stderr)

# Upload 3 images
cdn_map = {}
for local_path in IMG_PATHS:
    cdn_url = upload_image(token, local_path)
    if cdn_url:
        cdn_map[local_path] = cdn_url

# Replace local paths in HTML
for lp, cu in cdn_map.items():
    html = html.replace(f'src="{lp}"', f'src="{cu}"')

# Upload cover
thumb_id = upload_thumb(token, COVER_PATH)

# Create draft - correct UTF-8 encoding
safe_title_str = make_safe_title(title)
article = {
    "title": safe_title_str,
    "content": html,
    "thumb_media_id": thumb_id,
    "show_cover_pic": 1
}
if digest:
    article["digest"] = digest

request_data = {"articles": [article]}
json_data = json.dumps(request_data, ensure_ascii=False)
url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
r = requests.post(url, data=json_data.encode('utf-8'), headers={"Content-Type": "application/json; charset=utf-8"}).json()

print(f"[RESULT] {json.dumps(r, ensure_ascii=False)}", file=sys.stderr)
media_id = r.get('media_id', '')
print(json.dumps({
    "success": bool(media_id),
    "media_id": media_id,
    "errcode": r.get('errcode'),
    "errmsg": r.get('errmsg'),
    "title": title,
    "img_count": len(cdn_map)
}, ensure_ascii=False))
