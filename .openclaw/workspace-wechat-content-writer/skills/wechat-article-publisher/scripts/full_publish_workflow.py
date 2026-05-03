#!/usr/bin/env python3
"""
微信公众号文章发布工作流 - 完整版
"""
import os
import sys
import json

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from config import load_config, get_wechat_config

# 加载配置
config = load_config()
wechat_config = get_wechat_config()

APP_ID = wechat_config['app_id']
APP_SECRET = wechat_config['app_secret']

# 文章内容
TITLE = "AI时代的工作效率革命：让智能助手成为你的职场搭档"
DIGEST = "探索AI如何重塑工作方式，从智能写作到数据分析，解锁高效办公新姿势"
AUTHOR = "AI研究社"

CONTENT_HTML = """<section style="margin-bottom: 20px;">
<h2 style="color: #2c3e50; border-left: 4px solid #3498db; padding-left: 10px;">一、AI正在重塑办公场景</h2>

<h3 style="color: #34495e;">1. 智能写作助手</h3>
<p style="line-height: 1.8; color: #333;">传统的内容创作往往需要数小时甚至数天的构思与打磨。而现在，AI写作助手可以在几分钟内生成初稿，帮助我们从"从0到1"的困境中解脱出来。</p>

<p style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 3px solid #3498db;"><strong>实际应用场景：</strong><br/>
• 会议纪要整理：1小时会议→5分钟出稿<br/>
• 营销文案生成：输入关键词→获得10个创意版本<br/>
• 邮件撰写：描述意图→自动润色成专业表达</p>

<h3 style="color: #34495e;">2. 智能数据分析</h3>
<p style="line-height: 1.8; color: #333;">面对海量数据，AI可以快速识别模式、生成可视化图表，并给出业务洞察。</p>

<p style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 3px solid #e74c3c;"><strong>效率提升：</strong><br/>
• Excel数据处理：从2小时缩短至15分钟<br/>
• 报表生成：自动化每日/周/月报<br/>
• 趋势预测：基于历史数据的智能预判</p>

<h3 style="color: #34495e;">3. 智能会议助手</h3>
<p style="line-height: 1.8; color: #333;">AI会议助手可以实时转录、自动提取行动项、生成会议纪要，让会议真正产生价值。</p>
</section>

<section style="margin-bottom: 20px;">
<h2 style="color: #2c3e50; border-left: 4px solid #e74c3c; padding-left: 10px;">二、主流AI办公工具推荐</h2>

<table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
<tr style="background: #3498db; color: white;">
<th style="padding: 12px; border: 1px solid #ddd;">场景</th>
<th style="padding: 12px; border: 1px solid #ddd;">工具推荐</th>
<th style="padding: 12px; border: 1px solid #ddd;">核心能力</th>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">文本创作</td>
<td style="padding: 10px; border: 1px solid #ddd;">Kimi、Claude、GPT</td>
<td style="padding: 10px; border: 1px solid #ddd;">长文写作、代码生成</td>
</tr>
<tr style="background: #f9f9f9;">
<td style="padding: 10px; border: 1px solid #ddd;">图像生成</td>
<td style="padding: 10px; border: 1px solid #ddd;">Midjourney、通义万相</td>
<td style="padding: 10px; border: 1px solid #ddd;">封面、配图设计</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">PPT制作</td>
<td style="padding: 10px; border: 1px solid #ddd;">Gamma、Beautiful.ai</td>
<td style="padding: 10px; border: 1px solid #ddd;">自动排版、智能设计</td>
</tr>
<tr style="background: #f9f9f9;">
<td style="padding: 10px; border: 1px solid #ddd;">数据处理</td>
<td style="padding: 10px; border: 1px solid #ddd;">ChatGPT Code Interpreter</td>
<td style="padding: 10px; border: 1px solid #ddd;">数据分析、可视化</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">会议纪要</td>
<td style="padding: 10px; border: 1px solid #ddd;">讯飞听见、飞书妙记</td>
<td style="padding: 10px; border: 1px solid #ddd;">语音转写、智能摘要</td>
</tr>
</table>
</section>

<section style="margin-bottom: 20px;">
<h2 style="color: #2c3e50; border-left: 4px solid #27ae60; padding-left: 10px;">三、如何开始你的AI办公之旅</h2>

<h3 style="color: #34495e;">第一步：选择适合的入门工具</h3>
<p style="line-height: 1.8; color: #333;">对于初学者，建议从以下工具开始：</p>
<ul style="line-height: 1.8; color: #333;">
<li><strong>Kimi</strong>：中文理解能力强，适合长文档处理</li>
<li><strong>通义万相</strong>：国产图像生成，中文提示词友好</li>
<li><strong>飞书妙记</strong>：免费会议转写，上手零门槛</li>
</ul>

<h3 style="color: #34495e;">第二步：建立AI协作工作流</h3>
<ol style="line-height: 1.8; color: #333;">
<li><strong>明确任务边界</strong>：让AI处理重复性、模式化的工作</li>
<li><strong>人机协作</strong>：AI生成初稿，人工审核优化</li>
<li><strong>持续迭代</strong>：根据反馈调整提示词，提升输出质量</li>
</ol>

<h3 style="color: #34495e;">第三步：培养AI思维</h3>
<ul style="line-height: 1.8; color: #333;">
<li>学会用"提示词"与AI高效沟通</li>
<li>了解AI的能力边界，扬长避短</li>
<li>保持学习心态，跟进技术更新</li>
</ul>
</section>

<section style="margin-bottom: 20px;">
<h2 style="color: #2c3e50; border-left: 4px solid #9b59b6; padding-left: 10px;">四、AI时代的核心竞争力</h2>

<p style="line-height: 1.8; color: #333;">当AI能够完成越来越多的基础工作时，人类的独特价值将更加凸显：</p>

<ol style="line-height: 1.8; color: #333;">
<li><strong>创造力</strong>：提出新问题、新视角的能力</li>
<li><strong>判断力</strong>：在复杂情境中做出决策的能力</li>
<li><strong>同理心</strong>：理解他人需求、建立连接的能力</li>
<li><strong>学习力</strong>：快速适应变化、掌握新技能的能力</li>
</ol>

<p style="background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 3px solid #ffc107; font-size: 16px;"><strong>AI不是替代者，而是放大器。</strong>它放大的是那些能够驾驭它的人的能力。</p>
</section>

<section style="margin-bottom: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white;">
<h2 style="color: white; border: none; margin-top: 0;">结语：拥抱变革，智胜未来</h2>

<p style="line-height: 1.8; color: white;">AI技术的发展不是一场零和博弈，而是一次生产力的解放。那些能够将AI工具与自身专业深度结合的人，将在未来的职场中占据先机。</p>

<p style="line-height: 1.8; color: white;"><strong>今天，就是开始的最佳时刻。</strong>选择一个AI工具，从一个小任务开始尝试，你会发现：工作效率的提升，远比想象中来得更快。</p>
</section>

<p style="text-align: center; color: #666; font-style: italic; margin-top: 30px; padding: 20px; border-top: 1px solid #eee;">
<strong>你是已经在使用AI工具提升工作效率了吗？欢迎在评论区分享你的经验和心得！</strong>
</p>"""

def generate_cover():
    """生成封面图片"""
    from generate_cover import generate_cover_qwen
    import requests
    
    print("🎨 正在生成封面图片...")
    result = generate_cover_qwen(
        prompt="未来科技办公室，AI智能助手与人类协作，蓝色科技风格，现代简洁设计，工作效率提升概念",
        model="qwen-image-2.0"
    )
    
    if result['success']:
        image_url = result['image_url']
        print(f"✅ 封面生成成功: {image_url}")
        
        # 下载图片
        cover_path = "/tmp/cover_ai_productivity.jpg"
        response = requests.get(image_url, timeout=60)
        with open(cover_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ 封面已下载: {cover_path}")
        
        return cover_path
    else:
        raise Exception("封面生成失败")

def upload_cover(cover_path):
    """上传封面到微信"""
    from upload_material import upload_material
    
    print("📤 正在上传封面到微信素材库...")
    result = upload_material(APP_ID, APP_SECRET, cover_path)
    
    if result.get('thumb_media_id'):
        print(f"✅ 封面上传成功: {result['thumb_media_id']}")
        return result['thumb_media_id']
    else:
        raise Exception(f"封面上传失败: {result}")

def create_draft(thumb_media_id):
    """创建草稿"""
    from create_draft import create_draft
    
    print("📝 正在创建草稿...")
    result = create_draft(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        title=TITLE,
        content=CONTENT_HTML,
        digest=DIGEST,
        author=AUTHOR,
        thumb_media_id=thumb_media_id,
        show_cover_pic=1
    )
    
    if result.get('media_id'):
        print(f"✅ 草稿创建成功!")
        print(f"   Media ID: {result['media_id']}")
        return result['media_id']
    else:
        raise Exception(f"草稿创建失败: {result}")

def main():
    print("=" * 50)
    print("🚀 微信公众号文章发布工作流")
    print("=" * 50)
    print()
    
    try:
        # 1. 生成封面
        cover_path = generate_cover()
        
        # 2. 上传封面
        thumb_media_id = upload_cover(cover_path)
        
        # 3. 创建草稿
        media_id = create_draft(thumb_media_id)
        
        print()
        print("=" * 50)
        print("🎉 全部完成!")
        print("=" * 50)
        print(f"📄 标题: {TITLE}")
        print(f"🆔 Media ID: {media_id}")
        print()
        print("💡 提示: 登录公众号后台查看草稿并发布")
        
        # 保存结果
        with open("/tmp/publish_result.json", "w") as f:
            json.dump({
                "success": True,
                "title": TITLE,
                "media_id": media_id,
                "thumb_media_id": thumb_media_id
            }, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
