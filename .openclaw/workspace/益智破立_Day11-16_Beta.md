# 《益智破立》Day 11-16 - Beta 版本

版本：v1.0
日期：2026-03-26
状态：待完成

---

## 目标

在 Day 5-10 Alpha 基础上，完成全部 30 关的验证和所有系统接入。

**最终产出**：
1. 全部 30 关（3章×10关）验证通过
2. 升级系统（4条升级路线，永久成长）
3. 每日挑战（每天1个高难度关卡）
4. 社交系统（微信分享 + 好友排行）
5. 完整的游戏可玩版本

---

## 前置依赖

| 依赖项 | 对应 | 负责方 | 状态 |
|--------|------|--------|------|
| Day 5-10 Alpha 验收通过 | Day 5-10 | 你审核 | 待完成 |
| Day 0 美术素材（完整） | Day 0 事项3 | 我生成 | 待完成 |

---

## Day 11-13：全部 30 关参数化生成 + 验证

### Day 11：第1章参数化变体（5-10关难度提升）

**Claude Code 指令**：
```
在 LevelManager.ts 中实现关卡参数化变体：

1. 在 Chapter1.json 中补充 Level 5-10 的详细障碍物和目标配置：

Level 5: budget=80, targets=2(圆形木箱×2), structures=[桥形木板], projectiles=["stone","dumbbell"]
- 场景：两侧桥墩，中间悬空木板，木板上是2个目标

Level 6: budget=80, targets=2(1木箱+1铁箱), structures=[单柱支撑], projectiles=["stone","dumbbell"]
- 场景：单根钢柱支撑一块石板，石板两端各1个目标

Level 7: budget=60, targets=2(1木箱+1铁箱), structures=[三角结构], projectiles=["stone"]
- 场景：3根木板组成三角结构，顶上2个目标

Level 8: budget=60, targets=2(铁箱×2), structures=[双柱支撑], projectiles=["stone"]
- 场景：2根钢柱支撑石板，铁箱在石板上

Level 9: budget=50, targets=2(铁箱+木箱), structures=[叠叠乐], projectiles=["stone","dumbbell"]
- 场景：木箱铁箱交替堆叠，需要精准打击底部

Level 10 (Boss): budget=40, targets=3(铁箱×3), structures=[复杂塔形], projectiles=["stone","dumbbell"]
- 场景：3根钢柱+多层木板+3个目标，高塔结构，需要策略

完成后报告 10关完整配置。
```

### Day 12：第2章 10 关详细配置

**Claude Code 指令**：
```
在 Chapter2.json 中实现 Level 11-20 详细配置：

Level 11: budget=100, targets=2, materials=["wood","steel","rope"], projectiles=["stone","dumbbell"]
- 教学：绳索斜拉。两侧钢柱，中间搭绳索，绳索上放木板，木板上有目标

Level 12: budget=90, targets=2, materials=["wood","steel","rope"], projectiles=["stone","dumbbell"]
- 在Level 11基础上增加高度

Level 13: budget=80, targets=2, materials=["steel","rope"], projectiles=["stone","dumbbell"]
- 教学：只用绳索和钢。钢柱斜拉，考验绳索角度

Level 14: budget=80, targets=3, materials=["wood","steel","rope"], projectiles=["stone"]
- 教学：3个目标分布在不同高度

Level 15: budget=70, targets=3, materials=["wood","steel","rope"], projectiles=["stone","dumbbell"]
- 教学：哑铃可以压断木板，制造连锁反应

Level 16: budget=60, targets=3, materials=["steel","rope"], projectiles=["stone","dumbbell"]
- 教学：高难度纯绳索结构

Level 17: budget=60, targets=3, materials=["wood","steel","rope"], projectiles=["stone"]
- 综合复习

Level 18: budget=50, targets=3, materials=["steel","rope"], projectiles=["dumbbell"]
- 高难度：只用哑铃+绳索钢

Level 19: budget=40, targets=3, materials=["steel","rope"], projectiles=["stone","dumbbell"]
- 极高难度：极低预算

Level 20 (Boss): budget=50, targets=3, materials=["wood","steel","rope"], projectiles=["stone","dumbbell"]
- 章节Boss：高塔+斜拉综合

完成后报告 Chapter2 配置。
```

### Day 13：第3章 10 关详细配置

**Claude Code 指令**：
```
在 Chapter3.json 中实现 Level 21-30 详细配置：

Level 21: budget=120, targets=2, materials=["wood","steel","rope"], projectiles=["stone","dumbbell","firework"]
- 教学：先进攻支撑点。1根木柱支撑2个目标，需要先击倒木柱让目标摔落

Level 22: budget=100, targets=2, materials=["wood","steel"], projectiles=["stone","dumbbell"]
- 教学：先建后拆。先搭桥到目标附近，再投掷摧毁

Level 23: budget=90, targets=3, materials=["wood","steel","rope"], projectiles=["stone"]
- 综合：搭桥+精准打击

Level 24: budget=80, targets=3, materials=["steel"], projectiles=["dumbbell","firework"]
- 高难度：只用钢柱+重投掷物

Level 25: budget=70, targets=3, materials=["wood","steel"], projectiles=["stone","dumbbell"]
- 难度封顶

Level 26: budget=60, targets=3, materials=["wood","steel","rope"], projectiles=["stone"]
- 挑战：极低预算

Level 27: budget=60, targets=3, materials=["steel","rope"], projectiles=["dumbbell"]
- 挑战：只用绳索钢+哑铃

Level 28: budget=50, targets=3, materials=["steel","rope","explosive"], projectiles=["stone","firework"]
- 教学：炸药使用。地形障碍需要先炸开再搭桥

Level 29: budget=40, targets=3, materials=["wood","steel","rope"], projectiles=["stone","dumbbell","firework"]
- 极高难度

Level 30 (最终Boss): budget=30, targets=3, materials=["wood","steel","rope","explosive"], projectiles=["stone","dumbbell","firework"]
- 极限挑战：极低预算+4个目标+全部材料+全部投掷物

完成后报告 Chapter3 配置。
```

---

## Day 14：升级系统

### Day 14-1：升级系统 UI

**Claude Code 指令**：
```
在 MainScene 中添加"升级"按钮，进入升级界面：

1. 创建 Prefab assets/prefabs/ui/UpgradePanel.prefab
   包含：
   - 背景遮罩（半透明）
   - 升级面板（中央卡片）
   - 4个升级项：
     * 投掷力+（图标：弓，名称，等级，当前/上限，升级按钮，金币价格）
     * 精准度+（图标：准星，等级，当前/上限，升级按钮，金币价格）
     * 资源获取+（图标：金币袋，等级，当前/上限，升级按钮，金币价格）
     * 撤销次数+（图标：↩，等级，当前/上限，升级按钮，金币价格）
   - 关闭按钮（右上角X）
   - 当前金币显示

2. 升级费用计算：
   - 每级费用 = 基础费用 × (1.5 ^ 当前等级)
   - 投掷力/精准度/资源获取基础费用：100金币
   - 撤销次数基础费用：500金币

完成后报告升级面板结构。
```

### Day 14-2：升级逻辑绑定

**Claude Code 指令**：
```
在 GameManager.ts 中实现升级逻辑：

1. onUpgradeClick(type):
   - 检查当前金币是否足够
   - 检查是否已达等级上限
   - 扣除金币，应用升级效果
   - 调用 SaveManager.save()

2. 升级效果：
   - 投掷力+1：throwPower += 0.05（即每级+5%）
   - 精准度+1：trajectoryLine 点数增加
   - 资源获取+1：coinBonus += 0.1（即每关金币+10%）
   - 撤销次数+1：undoCount += 1（即每关多1次撤销）

3. UI 显示：
   - 升级按钮：达到上限时显示"已满级"
   - 金币不足时显示灰色，点击提示"金币不足"

完成后报告升级逻辑。
```

---

## Day 15：每日挑战系统

### Day 15-1：每日挑战逻辑

**Claude Code 指令**：
```
在 DailyChallengeManager.ts 中实现每日挑战：

1. 每日挑战配置：
   - 每天00:00自动重置（检查 localStorage 中的 lastDailyChallenge 日期）
   - 当天使用固定seed生成的关卡（基于日期字符串做随机种子）
   - 关卡内容：从30关中随机选1关，随机调整难度参数（±20%）

2. 分数计算：
   - 使用标准关卡分数计算，但加入时间惩罚
   - 时间越短，分数越高

3. 排行榜（本地）：
   - 保存每天的最高分
   - 显示最近7天的记录

4. UI 入口：
   - MainScene 增加"每日挑战"按钮
   - LevelSelect 增加每日挑战Tab

完成后报告每日挑战逻辑。
```

### Day 15-2：分享功能

**Claude Code 指令**：
```
在 ShareManager.ts 中实现微信分享：

1. 生成分享图片：
   - 在结算界面，点击"炫耀一下"按钮
   - 使用 Cocos Creator 的 RenderToTex 截图
   - 截图中包含：关卡名 + 星级 + 分数 + "益智破立"水印
   - 保存为 PNG，通过 wx.shareMessage 分享

2. 分享回调：
   - 分享成功后，奖励玩家 50 金币
   - ⚠️ 注：无广告版暂无奖励来源，v1先做功能，奖励机制在广告接入后补充
   - 使用 wx.showShareMenu 配置分享菜单

3. 好友排行（轻量版）：
   - 使用 wx.getUserCloudStorage 获取当前玩家最高关卡
   - 使用 wx.getGroupCloudStorage 获取群内好友数据
   - 在每日挑战 Tab 中显示排行榜

完成后报告分享功能。
```

---

## Day 16：整体测试 + 修复

### Day 16-1：全部 30 关完整验证

**你的审核任务**：
1. 从 Level 1 到 Level 30 逐关验证
2. 记录每关是否正常通过
3. 有问题的关卡发我截图 + 现象描述

### Day 16-2：全部系统联调

**你的审核任务**：
1. 升级系统：升级后效果是否生效
2. 每日挑战：当天关卡是否随机生成
3. 分享：截图分享是否成功
4. 存档：关掉游戏重开后进度是否保留

---

## Day 11-16 产出清单

| 阶段 | 产出 | 状态 |
|------|------|------|
| Day 11 | Level 5-10 详细配置 | 待完成 |
| Day 12 | Chapter2（10关完整） | 待完成 |
| Day 13 | Chapter3（10关完整） | 待完成 |
| Day 14 | 升级系统（UI+逻辑） | 待完成 |
| Day 15 | 每日挑战 + 分享系统 | 待完成 |
| Day 16 | 30关完整验证 + 修复 | 待完成 |

---

## 用户审核任务

Q11：Level 5-10 配置是否合理？

Q12：Chapter2 是否能正常加载？

Q13：Chapter3 是否能正常加载？

Q14：升级系统效果是否生效？

Q15：每日挑战和分享功能是否正常？

Q16：30关全部通过了吗？哪些有问题？

---

## 执行日志

（此栏由我填写，完成后更新状态）

| 日期 | Day | 步骤 | 内容 | 状态 | 完成日期 |
|------|-----|------|------|------|---------|
| - | Day 11 | 11 | Level 5-10配置 | 待完成 | - |
| - | Day 12 | 12 | Chapter2 10关 | 待完成 | - |
| - | Day 13 | 13 | Chapter3 10关 | 待完成 | - |
| - | Day 14 | 14 | 升级系统 | 待完成 | - |
| - | Day 15 | 15 | 每日挑战+分享 | 待完成 | - |
| - | Day 16 | 16 | 完整验证+修复 | 待完成 | - |
