# VoicePix MiniMax Speech API 测试套件

## 测试目标

本测试套件为 VoicePix 项目提供 MiniMax Speech API 的自动化测试覆盖：

- **T2A API** (`voicepix-t2a-tests.yaml`)：文本转语音，测试正常场景、错误处理、多种音色和格式
- **Voice Clone API** (`voicepix-clone-tests.yaml`)：声音克隆，测试鉴权与参数校验

## 文件结构

```
api-tests/
├── voicepix-t2a-tests.yaml    # T2A API 测试用例
├── voicepix-clone-tests.yaml  # Voice Clone API 测试用例
└── README.md                   # 本文档
```

## 运行测试

### 前置要求

```bash
# 安装 openclaw-api-tester（如果尚未安装）
npm install -g openclaw-api-tester

# 或使用 npx
npx openclaw-api-tester --help
```

### 运行全部测试

```bash
openclaw-api-tester run api-tests/
```

### 运行指定环境

```bash
# 使用 dev 环境
openclaw-api-tester run api-tests/voicepix-t2a-tests.yaml --env dev

# 使用 prod 环境
openclaw-api-tester run api-tests/voicepix-t2a-tests.yaml --env prod
```

### 运行指定用例

```bash
openclaw-api-tester run api-tests/voicepix-t2a-tests.yaml --test "T2A - 中文语音生成（正常）"
```

## 配置 API Key

### 方式一：直接编辑 YAML 文件

编辑 `voicepix-t2a-tests.yaml` 和 `voicepix-clone-tests.yaml` 中的 `environment` 配置：

```yaml
environment:
  dev:
    api_key: "YOUR_ACTUAL_GROUP_ID_HERE"  # 替换为你的 Group ID
  prod:
    api_key: "YOUR_ACTUAL_GROUP_ID_HERE"
```

### 方式二：环境变量覆盖

```bash
export MINIMAX_API_KEY="YOUR_ACTUAL_GROUP_ID_HERE"
openclaw-api-tester run api-tests/voicepix-t2a-tests.yaml
```

### 方式三：命令行参数

```bash
openclaw-api-tester run api-tests/voicepix-t2a-tests.yaml \
  --var "api_key=YOUR_GROUP_ID_HERE"
```

## 测试用例说明

### T2A API 测试用例

| 用例名称 | 描述 |
|---------|------|
| T2A - 中文语音生成（正常） | 使用中文音色生成语音，验证 200 响应和 audio header |
| T2A - 英文语音生成（正常） | 使用英文音色生成语音 |
| T2A - 空 text 字段返回错误 | 验证空文本返回 400 错误 |
| T2A - 无效 voice_id 返回错误 | 验证无效音色 ID 返回 400 错误 |
| T2A - speech-02-hd 模型（高清音色） | 测试高清语音模型 |
| T2A - PCM 格式输出 | 测试非 MP3 格式输出 |
| T2A - 无 Authorization header | 验证缺少鉴权返回 401 |
| T2A - 超长文本（接近限制） | 测试长文本处理 |

### Voice Clone API 测试用例

| 用例名称 | 描述 |
|---------|------|
| Voice Clone - 缺少 voice_id 参数 | 验证缺少必填参数返回 400 |
| Voice Clone - 无 Authorization header | 验证缺少鉴权返回 401 |

## 测试结果解读

### 成功输出示例

```
✅ T2A - 中文语音生成（正常）
   Status: 200 | Time: 1243ms
   ✓ Response contains audio data
```

### 失败输出示例

```
❌ T2A - 空 text 字段返回错误
   Expected: 400 | Actual: 200
   ✗ body_contains check failed
```

### 退出码

- `0`：所有测试通过
- `1`：存在测试失败
- `2`：配置错误或无法运行

## CI/CD 集成示例

### GitHub Actions

```yaml
name: API Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install API Tester
        run: npm install -g openclaw-api-tester

      - name: Run T2A Tests
        env:
          MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}
        run: |
          openclaw-api-tester run api-tests/voicepix-t2a-tests.yaml \
            --env prod \
            --format json > t2a-results.json

      - name: Run Clone Tests
        env:
          MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}
        run: |
          openclaw-api-tester run api-tests/voicepix-clone-tests.yaml \
            --env prod

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: api-test-results
          path: t2a-results.json
```

### GitLab CI

```yaml
stages:
  - test

api-tests:
  stage: test
  image: node:20
  script:
    - npm install -g openclaw-api-tester
    - openclaw-api-tester run api-tests/ --env prod
  variables:
    MINIMAX_API_KEY: $MINIMAX_API_KEY
  artifacts:
    reports:
      junit: results.xml
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any

    environment {
        MINIMAX_API_KEY = credentials('minimax-api-key')
    }

    stages {
        stage('API Tests') {
            steps {
                sh 'npm install -g openclaw-api-tester'
                sh 'openclaw-api-tester run api-tests/ --env prod'
            }
        }
    }

    post {
        always {
            junit 'results/*.xml'
        }
    }
}
```

### 本地开发工作流

```bash
# 1. 安装依赖
npm install -g openclaw-api-tester

# 2. 复制环境配置
cp api-tests/voicepix-t2a-tests.yaml api-tests/voicepix-t2a-tests.local.yaml

# 3. 编辑 local 配置填入你的 API Key
vim api-tests/voicepix-t2a-tests.local.yaml

# 4. 运行测试
openclaw-api-tester run api-tests/voicepix-t2a-tests.local.yaml --env dev

# 5. 提交前确保测试通过
openclaw-api-tester run api-tests/voicepix-t2a-tests.yaml --env prod
```
