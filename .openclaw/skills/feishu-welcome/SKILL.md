---
name: feishu-welcome
description: Automatically send welcome messages when new members join Feishu group chats. Use when the user wants to set up automatic welcome messages for group chat members joining events. Triggers on phrases like "set up welcome message", "group chat welcome", "welcome new members", "入群欢迎", "欢迎语".
---

# Feishu Group Welcome Skill

Automatically send welcome messages when new members (users or bots) join a Feishu group chat.

## How It Works

This skill listens to Feishu events:
- `im.chat.member.user.added_v1` - When a user joins the group
- `im.chat.member.bot.added_v1` - When a bot joins the group

When triggered, it sends a customizable welcome message mentioning the new member.

## Configuration

The welcome message is defined by the user. Default format:
```
欢迎 @新成员 加入群聊！🎉
```

## Usage

When setting up welcome messages:
1. Confirm the welcome message content with the user
2. Confirm whether to @mention the new member
3. Store the configuration for the specific chat

## Implementation

Use the `message` tool to send welcome messages:
- `channel`: "feishu"
- `target`: The chat ID where the member joined
- `message`: The welcome text with proper mention tags

Mention format for Feishu:
```
<at user_id="{user_id}">{display_name}</at>
```

Example welcome message:
```
欢迎 <at user_id="ou_xxxxx">新成员</at> 加入群聊！🎉
```
