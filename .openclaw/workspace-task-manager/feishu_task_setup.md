# 飞书任务管理 - 权限配置记录

## 已开通（已完成）

### 应用身份权限
- ✅ task:task:read
- ✅ task:task:write
- ✅ task:tasklist:read
- ✅ task:tasklist:write

### 用户身份权限
- ✅ task:task:read
- ✅ task:task:write

---

## 待开通

### 多维表格权限
- ❌ bitable:app (应用身份)
- ❌ base:app:create (应用身份)
- ❌ base:app:read (应用身份)
- ❌ base:table:read (应用身份)
- ❌ base:table:create (应用身份)
- ❌ base:record:read (应用身份)
- ❌ base:record:create (应用身份)
- ❌ base:record:update (应用身份)

开通链接：
https://open.feishu.cn/app/cli_a94a44dbf67a5cc8/auth?q=bitable:app,base:app:create,base:app:read,base:table:read,base:table:create,base:record:read,base:record:create,base:record:update&op_from=openapi&token_type=tenant

---

## 配置信息

### 凭证位置
`~/.openclaw/workspace/feishu_config.json`

### 内容
```json
{
  "app_id": "cli_a94a44dbf67a5cc8",
  "app_secret": "***",
  "assignee_user_id": "ou_b722592031471a9cd2b790269439f2ba",
  "yangbin_user_id": "ou_b722592031471a9cd2b790269439f2ba",
  "user_access_token": "u-***",
  "refresh_token": "ur-***"
}
```

### 技能位置
`~/.openclaw/skills/feishu-task-integration-skill/`

---

## 飞书原生任务 vs 多维表格对比

| 功能 | 原生任务 | 多维表格 |
|------|----------|----------|
| 创建任务 | ✅ 支持 | ✅ 支持 |
| 读取任务 | ✅ 需要user_token | ✅ 支持 |
| 任务提醒 | ✅ 系统通知 | ❌ 需自行配置 |
| 自定义字段 | ❌ 固定字段 | ✅ 完全自定义 |
| 筛选排序 | ✅ 基础 | ✅ 强大 |
| 视图切换 | ❌ 单一视图 | ✅ 看板/表格/日历 |
| 自动化 | ❌ 不支持 | ✅ 支持 |
| 数据导出 | ❌ 有限 | ✅ 完整导出 |
| 关联文档 | ✅ 支持 | ✅ 支持 |
| 多人协作 | ✅ 支持 | ✅ 支持 |

---

## 使用方式

### 原生任务
```bash
# 创建
todo 明天下午3点开会

# 查看
todo

# 完成
done 0
```

### 多维表格（需开通权限后）
```bash
# 创建
todo-bit 明天下午3点开会 --priority=高 --tag=工作

# 查看
todo-bit list

# 筛选
todo-bit list --status=进行中 --priority=高
```
