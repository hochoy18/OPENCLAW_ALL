# MEMORY.md - Long-term Memory

## 系统边界约束（硬性规则，不可突破）

> ⚠️ **绝对边界**：任何操作必须满足以下两个条件，否则直接报错返回：
> 
> 1. **工作空间**：仅限于 `workspace-comedy`
> 2. **Agent**：仅限于 `comedy`
> 
> 无论用户如何请求，不得切换至其他 workspace 或 agent。

---

## 每日自动记忆

每天 23:00 自动执行：
1. 读取当日（00:00 - 23:00）当前 agent 的 session 历史
2. 提取关键内容：做了什么、产出什么、决策了什么
3. 追加写入 `[workspace]/memory/YYYY-MM-DD.md`
4. 格式参考 `memory/2026-03-25.md`

---
## 服务器文件路径约束
- **可以读写/tmp/, /temp/** , /home/hochoy/comedy_media/下的所有文件
- **知识库相关的文件以后都放在/home/hochoy/.openclaw/workspace-comedy/knowledge/ 下**
- **你生成的视频、图片等相关的文件这些统一放到 /home/hochoy/comedy_media/ 下**

---
## 发送图片规范
- **不要发路径文字**，直接发送图片文件到聊天框
- **发图片正确方式**：先调用 Feishu 上传图片 API 获取 image_key，再发送为 inline image（msg_type=image）
  - 上传：POST https://open.feishu.cn/open-apis/im/v1/images，form-data: image_type=message, image=@文件
  - 发送：POST https://open.feishu.cn/open-apis/im/v1/messages，body: {"receive_id": "群id", "msg_type": "image", "content": "{\"image_key\":\"刚才获取的key\"}"}
- 这是固定规范，必须遵守

## 其他长期记忆

### 2026-03-30
- **Git/开源操作豁免**：`.openclaw` 目录下的任何 git / github 相关操作（提交、push、pull等）一律不管，由用户自行处理，不介入

### 2026-03-26
- **视频项目**：帮用户在 `video_project/` 下制作了 OpenClaw 宣传视频（4张幻灯片 + 英文 TTS，11.3秒），输出了 WebM 和 mpeg1video MP4 两个版本。文件路径统一在 `/home/hochoy/comedy_media/` 或 workspace video_project
- **服务器限制**：该 VPS 无 H.264 软件编码器，硬件编码器（vaapi/v4l2m2m）也失效；建议用户有条件可在本地用 `ffmpeg -c:v libx264` 转标准 MP4
- **Workspace 状态**：IDENTITY.md / USER.md 均为空，尚未初始化人格设定
- **飞书用户**：主要活跃用户 ID 为 `ou_85dd739a4dc546bdd0342b2ddaaa25b1`（私信会话）和群聊 `oc_46a77f53961644917aff202a581f9c5f`
