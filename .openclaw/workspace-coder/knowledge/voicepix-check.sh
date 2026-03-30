#!/bin/bash
# voicepix.html 自检脚本 - 每次提交前必须执行

FILE="/home/hochoy/.openclaw/workspace-coder/voicepix.html"

echo "=== VoicePix 代码自检 ==="

# 1. HTML 结构完整性
echo -n "[1/4] HTML 结构 (</script></body></html>): "
if grep -q '</script>' "$FILE" && grep -q '</body>' "$FILE" && grep -q '</html>' "$FILE"; then
  echo "✅"
else
  echo "❌ 缺失 HTML 闭合标签"
  exit 1
fi

# 2. JS 语法检查 (提取 <script> 内容用 node --check)
echo -n "[2/4] JS 语法 (node --check): "
python3 -c "
import re
with open('$FILE') as f:
    content = f.read()
m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if m:
    with open('/tmp/vp_check.js', 'w') as f:
        f.write(m.group(1))
    print('ok', end='')
" 2>/dev/null
RESULT=$(node --check /tmp/vp_check.js 2>&1)
if [ $? -eq 0 ]; then
  echo "✅"
else
  echo "❌ $RESULT"
  exit 1
fi

# 3. 关键元素存在性
echo -n "[3/4] 关键 DOM 元素: "
python3 -c "
import re
with open('$FILE') as f:
    c = f.read()
checks = ['id=\"genBtn\"', 'id=\"cloneBtn\"', 'id=\"preset\"', 'data-sec=\"t2a\"', 'data-sec=\"clone\"', 'data-f=\"mp3\"', 'id=\"akBtn\"']
ok = all(x in c for x in checks)
print('✅' if ok else '❌')
if not ok: exit(1)
" 2>/dev/null

# 4. API 调用参数正确性 (GID/KEY 不再用 AK)
echo -n "[4/4] API Key 变量 (无遗留 AK): "
if ! grep -q '\bAK\b' "$FILE"; then
  echo "✅"
else
  echo "❌ 发现遗留 AK 变量"
  exit 1
fi

echo ""
echo "=== 全部检查通过 ✅ ==="
