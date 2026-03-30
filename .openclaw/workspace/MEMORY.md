# MEMORY.md - 长期记忆

## 身份与权限

- 我是 **Hochoy**，OpenClaw 主 Agent（飞书渠道）
- 拥有最高权限，其他 agent 有各自的权限限制
- 可在用户授权下读写其他 agent workspace 内容
- 用户主要做探索性工作，因此我的权限较高

## 环境信息

- OpenClaw 版本：2026.3.13（61d171a）
- Node：v24.2.0
- OS：Linux 6.6.117-45.oc9.x86_64
- 工作目录：/home/hochoy/.openclaw/workspace
- Skills 安装目录：/home/hochoy/.openclaw/skills/

## MiniMax Image Generation Skill

- Skill 名：minimax-image-generation（从 clawhub 安装）
- 安装路径：~/.openclaw/skills/minimax-image-generation/
- Base URL 已修改为：api.minimax.io（国际版）
- 支持模型：image-01（图生图+文生图）/ image-01-live（不支持，API Key 套餐限制）
- API Key：`sk-cp-dEJDwSZI46V_ys9hSxmyH3MT3kjnYJAkMGQK6fz38Imta8l5FmHU9stkSc8lqrT_xpeglsSQypkntDpu0xuJAYVxmkx_cpo3wEHseh_5pCi_HX_qX9X66-Y`

## 用户项目：益智破立

- 游戏类型：物理建造+投掷破坏融合休闲游戏（Cocos Creator 3.8）
- 广告变现方案已取消（穿山甲需企业资质）
- 待确认：微信 AppID、通义万相 API Key
- 详细计划见 workspace 文档

## 安全边界

- 敏感/外部操作先问
- destructive 命令先确认
- 不泄露用户隐私数据

## 飞书账号对应关系（open_id 映射）

| Agent | 飞书 App/账号 | 目标用户 open_id |
|-------|--------------|-----------------|
| main | main | `ou_a40d252df8eedac11a6ca82ca1b65352`（何才本人） |
| wechat-assistant | wechat-assistant | `ou_7f442bef1a102e6c203ad4e2d1a86e69` |
| coder | coder | `ou_930ed7a70e55cdc26722683f4d7d00bd` |
| demo | demo | `ou_0bc2f0bdf4be8039599fe8c4967425a8` |
| task-manager | task-manager | `ou_b722592031471a9cd2b790269439f2ba` |
| cron | cron | `ou_a46824a36fa8086e31b863b652ce8d57` |
| comedy | comedy | `ou_85dd739a4dc546bdd0342b2ddaaa25b1` |

> open_id `ou_a40d252df8eedac11a6ca82ca1b65352` = 何才（用户本人）
