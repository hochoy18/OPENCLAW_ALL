#!/usr/bin/env python3
"""Generate slides for OpenClaw video"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
OUT = "/home/hochoy/.openclaw/workspace-comedy/video_project"

# Try to load a decent font, fallback to default
def get_font(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

def create_gradient(img, color1, color2, direction='horizontal'):
    """Draw a gradient on image"""
    draw = ImageDraw.Draw(img)
    for i in range(H):
        ratio = i / H
        r = int(color1[0] * (1-ratio) + color2[0] * ratio)
        g = int(color1[1] * (1-ratio) + color2[1] * ratio)
        b = int(color1[2] * (1-ratio) + color2[2] * ratio)
        draw.line([(0, i), (W, i)], fill=(r, g, b))
    return img

def draw_centered_text(draw, text, y, font, color, max_width=W-100):
    """Draw centered text with word wrap"""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0,0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    
    line_h = draw.textbbox((0,0), "ABC", font=font)[3] - draw.textbbox((0,0), "A", font=font)[3]
    total_h = len(lines) * line_h
    start_y = y - total_h // 2
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        lw = bbox[2] - bbox[0]
        draw.text(((W - lw)//2, start_y), line, font=font, fill=color)
        start_y += line_h
    return start_y

slides = [
    {
        "bg": (10, 10, 30),
        "bg2": (30, 30, 90),
        "title": "How to Learn OpenClaw",
        "subtitle": "Your Personal AI Agent",
        "accent": (100, 150, 255),
        "duration": 3.0,
    },
    {
        "bg": (15, 25, 45),
        "bg2": (20, 50, 80),
        "title": "What is OpenClaw?",
        "subtitle": "OpenClaw is a local autonomous AI agent framework.\nSupports Telegram, Discord, WhatsApp, Feishu & more.\nFeatures: Skills system, memory, web search, automation.",
        "accent": (80, 200, 150),
        "duration": 3.5,
    },
    {
        "bg": (25, 15, 40),
        "bg2": (50, 20, 70),
        "title": "How to Get Started",
        "subtitle": "1. Install: curl -fsSL https://openclaw.ai/install.sh | bash\n2. Run: openclaw onboard\n3. Requires: Node.js 24+ & an API key",
        "accent": (200, 120, 255),
        "duration": 3.5,
    },
    {
        "bg": (10, 30, 30),
        "bg2": (10, 60, 50),
        "title": "Core Features",
        "subtitle": "Skills system — extendable AI capabilities\nMulti-channel — one agent, many platforms\nMemory — persistent context\nWeb automation — search, browse, act",
        "accent": (255, 200, 80),
        "duration": 3.5,
    },
]

for i, slide in enumerate(slides):
    img = Image.new('RGB', (W, H), slide["bg"])
    img = create_gradient(img, slide["bg"], slide["bg2"], 'vertical')
    draw = ImageDraw.Draw(img)
    
    # Top accent bar
    draw.rectangle([0, 0, W, 8], fill=slide["accent"])
    # Bottom accent bar
    draw.rectangle([0, H-8, W, H], fill=slide["accent"])
    
    # Title
    font_title = get_font(110)
    bbox = draw.textbbox((0,0), slide["title"], font=font_title)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((W-tw)//2, 300), slide["title"], font=font_title, fill=(255,255,255))
    
    # Divider line
    line_y = 300 + th + 40
    draw.line([(200, line_y), (W-200, line_y)], fill=slide["accent"], width=3)
    
    # Subtitle
    font_sub = get_font(52)
    sub_lines = slide["subtitle"].split('\n')
    y_pos = line_y + 60
    for line in sub_lines:
        bbox = draw.textbbox((0,0), line, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text(((W-tw)//2, y_pos), line, font=font_sub, fill=(220,220,240))
        y_pos += (bbox[3] - bbox[1]) + 30
    
    # Bottom branding
    font_small = get_font(36)
    brand = "openclaw.ai"
    bbox = draw.textbbox((0,0), brand, font=font_small)
    bw = bbox[2] - bbox[0]
    draw.text(((W-bw)//2, H-130), brand, font=font_small, fill=(150,150,180))
    
    out_path = f"{OUT}/slide_{i+1:02d}.jpg"
    img.save(out_path, "JPEG", quality=92)
    print(f"Slide {i+1}: {out_path}")

print("All slides created!")
