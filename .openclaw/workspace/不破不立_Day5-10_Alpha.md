# 《不破不立》Day 5-10 - Alpha 版本

版本：v1.0
日期：2026-03-26
状态：待完成

---

## 目标

在 Day 2-4 核心 Demo 基础上，完成：
1. 完整 UI 框架（主界面 + 关卡选择 + 游戏 HUD）
2. 存档系统（与真实数据绑定）
3. 第1章 10 关完整内容
4. 第2章 + 第3章 各 1 个母版关卡（共 3 个母版，为 Day 11-16 做准备）

**最终产出**：功能完整的游戏骨架，可完成第1章10关。

---

## 前置依赖

| 依赖项 | 对应 | 负责方 | 状态 |
|--------|------|--------|------|
| Day 2-4 Demo 验收通过 | Day 2-4 | 你审核 | 待完成 |
| Day 0 美术素材（部分） | Day 0 事项4 | 我生成 | 待完成 |

---

## Day 5：UI 框架 - 主界面

### Day 5-1：创建主界面场景 MainScene

**Claude Code 指令**：
```
在 Cocos Creator 项目中：

1. 创建场景 assets/scenes/MainScene.fire

2. 场景结构：
   - 背景：全屏暖黄色（#F5A623）
   - 游戏标题："不破不立"（大字体，居中，白色，顶部1/3处）
   - 副标题："建造 · 投掷 · 破坏"（小字体，灰色，居中）
   - 开始按钮：
     * 矩形按钮（宽200px，高60px，圆角16px）
     * 背景深灰（#4A4A4A），文字白色"开始游戏"
     * 点击 → 切换到 LevelSelect 场景
   - 设置按钮（右上角小图标）
     * 点击 → 弹出设置面板（音效开关/音乐开关）

3. 创建 Prefab：
   - assets/prefabs/ui/ButtonLarge.prefab（开始按钮预制体）
   - assets/prefabs/ui/ButtonSmall.prefab（小按钮预制体）

完成后报告场景结构。
```

### Day 5-2：创建关卡选择场景 LevelSelect

**Claude Code 指令**：
```
在 Cocos Creator 项目中：

1. 创建场景 assets/scenes/LevelSelect.fire

2. 场景结构：
   - 顶部导航栏：
     * 返回按钮（左上角，← 图标）
       点击 → 返回 MainScene
     * 标题："选择关卡"（居中）
   - 章节标签：
     * Tab1：第1章"物理启蒙"
     * Tab2：第2章"结构秘密"（灰色锁定状态，点击弹出"第1章通关后解锁"）
     * Tab3：第3章"破坏艺术"（灰色锁定状态）
   - 关卡网格：
     * 第1章显示10个关卡按钮（3列网格）
     * 每个关卡按钮：圆形（宽高60px），显示关卡编号（1-10）
     * 已通关：显示星级（1-3个★）
     * 未通关：显示灰色锁定
     * 当前可玩：正常颜色，点击进入游戏
   - 底部：章节进度（1/10 10关）显示

3. 创建 Prefab：
   - assets/prefabs/ui/LevelButton.prefab（关卡按钮预制体）

完成后报告场景结构。
```

### Day 5-3：保存系统与真实数据绑定

**Claude Code 指令**：
```
在 SaveManager.ts 中实现完整存档逻辑：

1. 存储数据结构（SaveData）：
   {
     currentLevel: number,       // 已解锁的最高关卡
     stars: number[],           // 每关星级 [levelId]: stars
     coins: number,             // 当前金币
     upgrades: {               // 升级数据
       throwPower: number,     // 投掷力等级 (0-20)
       accuracy: number,        // 精准度等级 (0-20)
       coinBonus: number,       // 金币加成等级 (0-20)
       undoCount: number,      // 撤销次数 (0-3)
     },
     unlockedProjectiles: string[], // 已解锁投掷物
     lastDailyChallenge: string,    // 上次每日挑战日期
     dailyBestScores: {},          // 每日挑战最高分
   }

2. 实现方法：
   - save()：序列化写入 localStorage
   - load()：从 localStorage 读取，反序列化
   - reset()：重置所有存档（用于测试）

3. 在 GameManager.ts 中：
   - onLoad()：调用 SaveManager.load()
   - 每关结算后：调用 SaveManager.save()

完成后报告存档数据结构。
```

---

## Day 6-8：第1章 10 关完整内容

### Day 6-1：创建关卡配置数据

**Claude Code 指令**：
```
创建关卡配置文件：

1. assets/levels/Chapter1.json
   内容：10个关卡的配置数组

   每关数据结构：
   {
     id: 1,                    // 关卡编号
     chapter: 1,               // 章节
     name: "第一关",
     budget: 100,             // 材料预算（金币）
     availableMaterials: ["wood"],  // 可用材料
     availableProjectiles: ["stone"], // 可用投掷物
     targets: [               // 目标列表
       { type: "box", x: 400, y: 300, w: 60, h: 60 }
     ],
     obstacles: [              // 障碍物
       { type: "ground", x: 0, y: 0, w: 800, h: 50 }
     ],
     starThresholds: [50, 80, 100],  // 1/2/3星分数阈值
     hint: "按住屏幕拖动瞄准，松开发射！"
   }

2. 10关难度参数（参考GDD）：
   - Level 1:  budget=150, targets=1, materials=["wood"], projectiles=["stone"]
   - Level 2:  budget=120, targets=1, materials=["wood"], projectiles=["stone"]
   - Level 3:  budget=100, targets=1, materials=["wood"], projectiles=["stone"]
   - Level 4:  budget=100, targets=2, materials=["wood"], projectiles=["stone"]
   - Level 5:  budget=80,  targets=2, materials=["wood"], projectiles=["stone","dumbbell"]
   - Level 6:  budget=80,  targets=2, materials=["wood","steel"], projectiles=["stone"]
   - Level 7:  budget=60,  targets=2, materials=["wood","steel"], projectiles=["stone"]
   - Level 8:  budget=60,  targets=2, materials=["wood","steel"], projectiles=["stone"]
   - Level 9:  budget=50,  targets=2, materials=["wood","steel"], projectiles=["stone"]
   - Level 10: budget=40,  targets=3, materials=["wood","steel"], projectiles=["stone","dumbbell"]

完成后报告 Chapter1.json 结构。
```

### Day 6-2：加载关卡数据到场景

**Claude Code 指令**：
```
在 LevelManager.ts 中实现关卡加载：

1. loadLevel(levelId):
   - 从 Chapter1.json（1-10关）或 Chapter2/3.json（11-30关）加载数据
   - 解析 targets → 创建目标节点
   - 解析 obstacles → 创建障碍物节点
   - 设置 availableMaterials → 更新 Builder UI
   - 设置 budget → 初始化预算显示

2. evaluateResult():
   - 统计：破坏目标数 / 投掷次数 / 剩余预算
   - 计算分数 = 目标分(60) + 精准分(20) + 预算分(20)
   - 判断星级（参考 starThresholds）
   - 触发结算 UI

3. GameManager.ts 中实现关卡切换：
   - onLevelComplete() → 显示结算界面 → 存储进度 → 返回 LevelSelect
   - onLevelFailed() → 显示失败界面 → 提供重新开始

完成后报告关卡加载流程。
```

### Day 7-8：第1章 10 关逐关验证

**你的审核任务**：
1. 逐关测试（Level 1 → Level 10）
2. 每关记录：
   - 能否正常进入
   - 材料放置是否正常
   - 投掷是否正常
   - 目标检测是否正常
   - 结算是否正常
3. 把有问题的关卡编号发我

---

## Day 9：第2章 + 第3章 母版

### Day 9-1：创建第2章母版关卡

**Claude Code 指令**：
```
创建第2章（结构秘密）关卡配置：

assets/levels/Chapter2.json（10关）

难度参考（从第1章结尾递增）：
- Level 11: budget=100, targets=2, materials=["wood","steel","rope"], projectiles=["stone","dumbbell"]
- Level 12-19: 逐步增加绳索(rope)的使用需求
- Level 20（章节Boss）: budget=60, targets=3, materials全部, projectiles全部

关键教学点：
- 绳索只受拉不受压，需要配合钢梁使用
- 斜拉结构可以增加稳定性

完成后报告 Chapter2.json 结构。
```

### Day 9-2：创建第3章母版关卡

**Claude Code 指令**：
```
创建第3章（破坏艺术）关卡配置：

assets/levels/Chapter3.json（10关）

难度参考（从第2章结尾继续递增）：
- Level 21: budget=120, targets=2, 需要先搭后拆
- Level 22-28: 目标分散在复杂结构内部
- Level 30（最终Boss）: budget=50, targets=3, 综合考验建造+投掷+精准

关键教学点：
- 支撑点概念：打掉某个部件，整栋结构连锁倒塌
- 优先目标：先摧毁支撑点比直接打目标更高效

完成后报告 Chapter3.json 结构。
```

---

## Day 10：UI 优化 + 整体修复

### Day 10-1：完善游戏内 HUD

**Claude Code 指令**：
```
在游戏场景（DemoLevel.fire）中完善 HUD：

1. 顶部 HUD 条：
   - 左侧：当前关卡名称（例："第1关"）
   - 中间：星级预览（当前获得 / 目标）
   - 右侧：剩余投掷次数

2. 建造阶段 UI：
   - 顶部：预算显示（已用 / 总预算）
   - 底部：4个材料按钮（对应木板/钢梁/绳索/炸药）
   - 每个按钮：图标 + 剩余数量
   - 未解锁材料显示锁定状态

3. 投掷阶段 UI：
   - 顶部：目标列表（已摧毁 / 总数）
   - 底部：当前投掷物 + 蓄力条
   - 蓄力条：按住时显示，颜色从绿→黄→红

4. 结算界面：
   - 遮罩层（半透明黑色）
   - 中央卡片：星级动画（星星从0到获得数）
   - 金币获得动画
   - "下一关" / "重玩" / "返回" 按钮

完成后报告 HUD 结构。
```

### Day 10-2：美术素材替换

**我执行（美术素材）**：
- 将在 Day 0 事项4 中生成的测试图确认后，替换到对应预制体中
- 如果测试图未通过，继续调整 Prompt 重生成

**你的审核任务**：
1. 确认美术素材是否替换成功
2. 风格是否一致（温暖工业风）

---

## Day 5-10 产出清单

| 阶段 | 产出 | 状态 |
|------|------|------|
| Day 5 | MainScene.fire / LevelSelect.fire / Prefabs / SaveManager完善 | 待完成 |
| Day 6 | Chapter1.json（10关完整配置） | 待完成 |
| Day 7-8 | 第1章10关逐关验证 + 修复 | 待完成 |
| Day 9 | Chapter2.json + Chapter3.json（母版） | 待完成 |
| Day 10 | 游戏HUD完善 + 美术素材替换 | 待完成 |

---

## 用户审核任务

Q5：Day 5 UI框架完成后，主界面和关卡选择界面是否正常显示？

Q6-8：第1章10关逐关验证，每关是否有问题？哪些关卡有问题？

Q9：第2/3章母版关卡是否能正常加载？

Q10：美术素材是否替换成功？

---

## 执行日志

（此栏由我填写，完成后更新状态）

| 日期 | Day | 步骤 | 内容 | 状态 | 完成日期 |
|------|-----|------|------|------|---------|
| - | Day 5 | 5-1 | 主界面场景 | 待完成 | - |
| - | Day 5 | 5-2 | 关卡选择场景 | 待完成 | - |
| - | Day 5 | 5-3 | 存档系统绑定 | 待完成 | - |
| - | Day 6 | 6-1 | Chapter1.json | 待完成 | - |
| - | Day 6 | 6-2 | 关卡加载逻辑 | 待完成 | - |
| - | Day 7-8 | 7-8 | 10关验证+修复 | 待完成 | - |
| - | Day 9 | 9-1 | Chapter2.json | 待完成 | - |
| - | Day 9 | 9-2 | Chapter3.json | 待完成 | - |
| - | Day 10 | 10-1 | HUD完善 | 待完成 | - |
| - | Day 10 | 10-2 | 美术替换 | 待完成 | - |
