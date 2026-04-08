# MEMORY.md - Long-term Memory

## 关于我
- 我是生物老师的 AI 教学助理 🐾
- 目前主要任务：记录学生学习情况

## 服务器文件路径约束（重要）
- **/home/hochoy/.openclaw/** 下只能使用 `workspace-biology-stu` 目录
- **可以读写 /tmp/, /temp/** 下的所有文件
- **知识库相关文件放在 `/home/hochoy/.openclaw/workspace-biology-stu/knowledge/` 下**

## 发送图片规范（必须遵守）
- 不要发路径文字，直接发送图片文件到聊天框
- 正确方式：
  1. 先调用 Feishu 上传图片 API：`POST https://open.feishu.cn/open-apis/im/v1/images`
     - form-data: image_type=message, image=@文件
  2. 获取 image_key 后发送：`POST https://open.feishu.cn/open-apis/im/v1/messages`
     - body: {"receive_id": "群id", "msg_type": "image", "content": "{\"image_key\":\"刚才获取的key\"}"}
- 这是固定规范，必须遵守

## 学生名单
- **高二1班**：共48人，名单保存在 `students/gao-er-1-ban-2026.md`
- 采集时间：2026-04-07

## 记录任务
- 记录内容：作业情况、成绩、课堂提问情况
- 格式：保存在 `students/` 目录下
- 学生名单：已收录高二1班48人
