# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## 飞书发图规范

发送图片到飞书时，**禁止发送路径文字**，直接发送图片文件。

### 正确流程
1. **上传图片** → 获取 image_key  
   `POST https://open.feishu.cn/open-apis/im/v1/images`  
   form-data: `image_type=message`, `image=@文件路径`

2. **发送图片消息**  
   `POST https://open.feishu.cn/open-apis/im/v1/messages`  
   body: `{"receive_id": "目标ID", "msg_type": "image", "content": "{\"image_key\":\"<key>\"}"}`

### 优先使用
优先用 `message` 工具自带的 media 参数；不支持时再走上述 API。

---

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

---

Add whatever helps you do your job. This is your cheat sheet.
