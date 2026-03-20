# OpenClaw 手动命令清单

由于当前 agent 没有 exec 权限，以下命令需要在终端手动执行：

## ClawHub 技能管理

```bash
# 搜索技能
openclaw clawhub search <关键词>

# 安装技能
openclaw clawhub install <技能名>

# 查看已安装技能
openclaw clawhub list

# 更新技能
openclaw clawhub update <技能名>

# 更新所有技能
openclaw clawhub update --all

# 查看技能详情
openclaw clawhub info <技能名>
```

## 常用示例

```bash
# 搜索搜索相关的技能
openclaw clawhub search search

# 搜索社交媒体相关技能
openclaw clawhub search social

# 搜索开发工具
openclaw clawhub search dev

# 安装 agent-reach（如果还没有）
openclaw clawhub install agent-reach
```

## 查看当前配置

```bash
# OpenClaw 状态
openclaw status

# 查看配置
openclaw config get

# 查看当前 agent 配置
cat ~/.openclaw/openclaw.json | grep -A 5 "wechat-assistant"
```

## 技能开发（如需在 workspace 创建技能）

```bash
# 创建技能目录
mkdir -p ~/.openclaw/workspace-wechat-assistant/skills/my-skill

# 或者安装到用户目录
mkdir -p ~/.openclaw/skills/my-skill
```

---
*此清单由 wechat-assistant agent 生成*