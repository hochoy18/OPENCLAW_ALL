# 《不破不立》Day 2-4 - 核心玩法 Demo

版本：v1.0
日期：2026-03-26
状态：待完成

---

## 目标

在 Day 1 创建的 Cocos Creator 项目基础上，用 Claude Code 生成代码，完成核心物理玩法的 Demo。

**最终产出**：一个**可玩的单关 Demo**，包含：
- 物理引擎正常工作（重力 + 碰撞）
- 建造系统可用（放置材料 + 关节连接）
- 投掷系统可用（瞄准 + 轨迹预测 + 发射）
- 破坏检测正常（碰撞触发破坏 + 目标检测）
- 结算界面（过关条件：摧毁目标 → 显示星级）

---

## 前置依赖

| 依赖项 | 对应 | 负责方 | 状态 |
|--------|------|--------|------|
| Cocos Creator 项目（已配置 AppID） | Day 1 步骤3-4 | 你本地 | 待完成 |
| Day 1 步骤6 构建成功 | Day 1 步骤6 | 你本地 | 待完成 |

---

## 代码生成方式

以下所有代码由 **Claude Code** 执行。

**执行方式**：
1. 你打开终端，进入项目目录
2. 运行：`claude --permission-mode bypassPermissions --print '指令'`
3. Claude Code 执行后，把输出发我验证

或者：
1. 你把指令内容直接发给 OpenClaw（我）执行

---

## Day 2：物理引擎 + 场景搭建

### Day 2-1：创建核心文件夹结构

**Claude Code 指令**：
```
请在 Cocos Creator 项目中创建以下 TypeScript 文件：

1. assets/scripts/core/PhysicsManager.ts - 物理引擎管理器
   - 配置 Chipmunk 物理引擎参数
   - 重力设置为 y=-2000
   - 开启物体休眠（sleep: true）
   - 固定步长 1/60s
   
2. assets/scripts/core/GameManager.ts - 游戏总管理器
   - 游戏状态机（IDLE / BUILDING / THROWING / RESULT）
   - 当前关卡数据引用
   - 评分和星级计算逻辑

3. assets/scripts/core/LevelManager.ts - 关卡管理器
   - 关卡配置数据结构（LevelData 接口）
   - 从 JSON 加载关卡数据
   - 难度参数计算

4. assets/scripts/core/SaveManager.ts - 存档管理器
   - 使用 localStorage 存储进度
   - 存储内容：当前关卡 / 金币 / 升级数据 / 已解锁投掷物

5. assets/scripts/core/Constants.ts - 常量定义
   - 材料物理属性（density/friction/restitution）
   - 投掷物物理参数
   - 星级阈值

完成后报告创建了哪些文件。
```

### Day 2-2：创建测试场景

**Claude Code 指令**：
```
在 Cocos Creator 项目中：

1. 创建场景 assets/scenes/DemoLevel.fire
   - 添加 Canvas（Canvas组件）
   - 添加 Camera（Camera组件，正交投影）
   - 添加一个背景节点（纯色矩形，暖黄色 #F5A623）
   - 添加地面节点（灰色矩形，深灰 #4A4A4A，高度100px，底部对齐）

2. 在该场景中：
   - 创建一个名为 PhysicsTest 的 TypeScript 组件
   - 挂在 Canvas 节点上
   - 实现 onLoad()：初始化 PhysicsManager，设置物理世界
   - 实现 start()：添加一个测试刚体（红色圆形，半径30px）

3. 将该场景设为默认启动场景（通过 GameManager.ts 控制）

完成后报告场景结构。
```

### Day 2-3：验证物理引擎

**验证标准**：
- 运行游戏时，红色圆形刚体应在 1 秒内落到地面
- 落到地面后应停止（休眠）
- Cocos 模拟器控制台无报错

**你的审核任务**：
1. 运行项目，观察红色刚体是否下落
2. 截图发我
3. 如有报错，把报错信息发我

---

## Day 3：建造系统 Demo

### Day 3-1：创建建造系统核心文件

**Claude Code 指令**：
```
在 Cocos Creator 项目中继续创建文件：

1. assets/scripts/building/Material.ts - 材料数据类
   - 枚举：MaterialType { WOOD, STEEL, ROPE, EXPLOSIVE }
   - 材料数据结构 { type, cost, density, friction, restitution, maxLength }
   - 材料预算配置（参考 GDD 中数值）

2. assets/scripts/building/Builder.ts - 建造阶段控制器
   - 当前材料预算 / 已使用预算
   - 当前选中的材料类型
   - onClickMaterial(type)：选中材料
   - onDropMaterial(position)：在指定位置放置材料
   - onRotateMaterial(angle)：旋转当前材料
   - onConfirm()：确认建造完成，切换到投掷阶段
   - 建造阶段 UI（预算显示、确认按钮）

3. assets/scripts/building/Structure.ts - 结构管理
   - 管理所有已放置的材料节点
   - 材料之间的关节连接（使用 Cocos 内置 Joint 组件）
   - 移除材料（撤销功能，每关3次）

4. 在 DemoLevel.scene 中添加：
   - 建造 UI 节点（预算显示：100/100 金币）
   - 4个材料按钮（木板/钢梁/绳索/炸药）
   - 一个确认建造按钮
   - 取消按钮

完成后报告建造系统文件列表。
```

### Day 3-2：实现材料放置

**Claude Code 指令**：
```
在 Builder.ts 中实现以下逻辑：

1. 玩家点击材料按钮 → 选中材料类型
2. 在场景中显示材料预览（半透明，跟随鼠标）
3. 玩家点击场景 → 实例化材料预制体（Prefab）
4. 实例化时：
   - 创建物理刚体（根据材料类型设置 density/friction/restitution）
   - 如果有两个以上材料，自动用关节连接（distance joint）
5. 更新预算消耗

完成后报告材料放置流程是否走通。
```

### Day 3-3：建造系统联调

**你的审核任务**：
1. 运行 DemoLevel 场景
2. 点击木板按钮 → 点击场景放置 → 检查预算是否减少
3. 再放置2块木板 → 检查关节是否自动连接
4. 点击确认按钮 → 检查是否切换到投掷阶段
5. 如有问题，把现象发我

---

## Day 4：投掷系统 Demo + 破坏检测

### Day 4-1：创建投掷系统核心文件

**Claude Code 指令**：
```
在 Cocos Creator 项目中创建文件：

1. assets/scripts/throwing/Projectile.ts - 投掷物数据类
   - 枚举：ProjectileType { STONE, DUMBBELL, BARBEL, FIREWORK }
   - 投掷物数据结构 { type, mass, restitution, unlockLevel }
   - 初始投掷物：只有 STONE 可用

2. assets/scripts/throwing/Trajectory.ts - 轨迹预测
   - predictTrajectory(startPos, velocity, steps) 函数
   - 原理：每帧前向模拟物理步长，输出路径点数组
   - 在场景中绘制虚线（使用 Graphics 组件）

3. assets/scripts/throwing/ThrowController.ts - 投掷控制器
   - 当前选中的投掷物类型
   - 蓄力状态（按住时间 → 力量映射）
   - onPointerDown：开始瞄准
   - onPointerMove：更新轨迹预测线
   - onPointerUp：发射投掷物，施加 Impulse
   - 投掷物理参数：最小力 500，最大力 2000

4. assets/scripts/destruction/DestructionMgr.ts - 破坏管理器
   - 碰撞力道阈值配置
   - onContactBegin 回调：计算碰撞力道
   - 超过阈值 → 触发 node.destroy()
   - 播放粒子特效（debris）
   - 检测所有目标是否被摧毁 → 触发过关
```

### Day 4-2：实现投掷流程

**Claude Code 指令**：
```
在 ThrowController.ts 中实现投掷流程：

1. 玩家按住发射区域 → 开始蓄力（按住的时长，0-2秒映射到力量）
2. 移动鼠标 → 调用 Trajectory.predictTrajectory() → 更新轨迹线
3. 玩家松开鼠标 → 
   - 创建投掷物刚体节点
   - 施加 Impulse（方向为当前鼠标朝向）
   - 进入物理模拟阶段
4. 物理模拟 → DestructionMgr 监听碰撞事件
5. 所有目标被摧毁 → 切换到 RESULT 状态

在 DemoLevel.scene 中添加：
- 发射区域 UI（底部，灰色矩形，高100px）
- 投掷物选择按钮（当前只用石块）
- 力量条 UI（显示当前蓄力状态）
- 目标物体（3个红色矩形，添加 Target 标签）

完成后报告投掷流程。
```

### Day 4-3：完整 Demo 联调（最终验证）

**最终 Demo 验收标准**（Day 4 结束前必须完成）：

| 测试项 | 验收标准 | 状态 |
|--------|---------|------|
| 物理引擎 | 刚体下落、碰撞、静止正常 | - |
| 材料放置 | 木板放置成功，关节连接正常 | - |
| 预算系统 | 放置木板后预算减少，重置后恢复 | - |
| 投掷瞄准 | 轨迹预测线正常显示 | - |
| 投掷发射 | 按住蓄力，松开发射，投掷物飞行 | - |
| 破坏检测 | 投掷物碰撞目标 → 目标消失 + 粒子特效 | - |
| 过关判定 | 3个目标全摧毁 → 弹出"过关"提示 | - |
| 重新开始 | 点击重新开始 → 重置所有状态 | - |

**你的审核任务**：
1. 逐项测试以上验收标准
2. 如有不通过的，把现象发我（截图 + 描述）
3. 全部通过后，Day 2-4 结束

---

## Day 2-4 产出清单

完成后应有以下文件：

```
assets/
├── scripts/
│   ├── core/
│   │   ├── PhysicsManager.ts    ✅
│   │   ├── GameManager.ts       ✅
│   │   ├── LevelManager.ts      ✅
│   │   ├── SaveManager.ts        ✅
│   │   └── Constants.ts         ✅
│   ├── building/
│   │   ├── Material.ts          ✅
│   │   ├── Builder.ts            ✅
│   │   └── Structure.ts         ✅
│   ├── throwing/
│   │   ├── Projectile.ts         ✅
│   │   ├── Trajectory.ts         ✅
│   │   └── ThrowController.ts    ✅
│   └── destruction/
│       ├── DestructionMgr.ts      ✅
│       └── ParticleFX.ts         ✅
└── scenes/
    └── DemoLevel.fire            ✅
```

---

## 用户审核任务（Day 2-4 完成后）

1. **Day 2 审核**：截图发我，红色刚体是否正常下落
2. **Day 3 审核**：建造系统操作是否正常，材料放置和预算减少是否正常
3. **Day 4 审核**：完成上表9项验收标准，逐项报告

---

## 需要你确认（Q2-4）

Q2-1：Day 2 运行后，红色刚体是否正常落到地面？

Q2-2：Day 3 建造系统操作是否正常？

Q2-3：Day 4 投掷系统操作是否正常？

Q2-4：9项验收标准全部通过了吗？哪项有问题？

---

## 执行日志

（此栏由我填写，完成后更新状态）

| 日期 | Day | 步骤 | 内容 | 状态 | 完成日期 |
|------|-----|------|------|------|---------|
| - | Day 2 | 2-1 | 核心文件夹结构 | 待完成 | - |
| - | Day 2 | 2-2 | 测试场景 | 待完成 | - |
| - | Day 2 | 2-3 | 物理验证 | 待完成 | - |
| - | Day 3 | 3-1 | 建造系统文件 | 待完成 | - |
| - | Day 3 | 3-2 | 材料放置逻辑 | 待完成 | - |
| - | Day 3 | 3-3 | 建造系统联调 | 待完成 | - |
| - | Day 4 | 4-1 | 投掷系统文件 | 待完成 | - |
| - | Day 4 | 4-2 | 投掷流程实现 | 待完成 | - |
| - | Day 4 | 4-3 | 完整Demo联调 | 待完成 | - |
