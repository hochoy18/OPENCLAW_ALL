#!/usr/bin/env python3
"""生成发酵工程知识网络图Word文档"""

import os
import zipfile
from pathlib import Path

OUTPUT_PATH = "/home/hochoy/.openclaw/workspace-biology/output/发酵工程知识网络图.docx"

def create_minimal_docx(output_path: str):
    """创建一个简单的Word文档"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Word document namespaces
    namespaces = {
        'wpc': 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas',
        'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
        'o': 'urn:schemas-microsoft-com:office:office',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
        'v': 'urn:schemas-microsoft-com:vml',
        'wp14': 'http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'w10': 'urn:schemas-microsoft-com:office:word',
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
        'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
        'wpg': 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup',
        'wpi': 'http://schemas.microsoft.com/office/word/2010/wordprocessingInk',
        'wne': 'http://schemas.microsoft.com/office/word/2006/wordml',
        'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
    }

    def make_element(tag, text='', attrs=None):
        """Create an XML element with text content"""
        attr_str = ''
        if attrs:
            attr_str = ' ' + ' '.join(f'{k}="{v}"' for k, v in attrs.items())
        return f'<w:{tag}{attr_str}><w:t>{text}</w:t></w:{tag}>'

    def make_para(content, style=None, center=False, spacing_before=0, spacing_after=200):
        """Create a paragraph element"""
        jc = '<w:jc w:val="center"/>' if center else ''
        return f'''<w:p>
  <w:pPr>
    <w:pStyle w:val="{style}"/>
    <w:spacing w:before="{spacing_before}" w:after="{spacing_after}"/>
    {jc}
  </w:pPr>
  {content}
</w:p>'''

    def make_run(text, bold=False, size=24, color='000000'):
        """Create a run element"""
        b_str = '<w:b/>' if bold else ''
        return f'''<w:r>
  <w:rPr>
    <w:sz w:val="{size}"/>
    <w:szCs w:val="{size}"/>
    <w:color w:val="{color}"/>
    {b_str}
  </w:rPr>
  <w:t>{text}</w:t>
</w:r>'''

    def make_heading_run(text, size=44, color='1F4E79'):
        return make_run(text, bold=True, size=size, color=color)

    def make_accent_run(text, size=24, color='2E75B6'):
        return make_run(text, bold=True, size=size, color=color)

    # Build document content
    body_content = []

    # === 封面 ===
    body_content.append(make_para('', spacing_before=2400, spacing_after=0))  # 空白
    body_content.append(make_para(make_heading_run('发酵工程及其应用', size=56), center=True, spacing_after=400))
    body_content.append(make_para(make_run('知识网络图', size=32, color='2E75B6'), center=True, spacing_after=800))
    body_content.append(make_para(make_run('━━━━━━━━━━━━━━━━━━━━', size=24, color='808080'), center=True, spacing_after=400))
    body_content.append(make_para(make_run('一、发酵工程的基本环节', size=24), center=True, spacing_after=200))
    body_content.append(make_para(make_run('二、发酵工程的特点', size=24), center=True, spacing_after=200))
    body_content.append(make_para(make_run('三、发酵工程的应用', size=24), center=True, spacing_after=600))
    body_content.append(make_para(make_run('高中生物 · 选择性必修三 · 生物技术与工程', size=22, color='808080'), center=True, spacing_after=0))

    # Page break
    body_content.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # === 一、发酵工程的基本环节 ===
    body_content.append(make_para(make_heading_run('一、发酵工程的基本环节', size=44), spacing_before=0, spacing_after=300))
    body_content.append(make_para(make_accent_run('中心环节：发酵罐内发酵', size=22), spacing_after=200))

    # 流程步骤
    steps = [
        ('1', '选育菌种', '目的：获得性状优良的菌种\n来源：自然筛选、诱变育种、基因工程育种'),
        ('2', '扩大培养', '将菌种数量扩增至一定规模，以满足发酵罐接种需求'),
        ('3', '培养基的配制与灭菌', '配制适合菌种生长的培养基，并进行严格灭菌防止杂菌污染'),
        ('4', '接种', '将菌种接入无菌培养基'),
        ('5', '发酵罐内发酵', '严格控制温度、pH、溶解氧等发酵条件（中心环节）'),
        ('6', '分离、提纯产物', '若产物是代谢物：提取、分离、纯化\n若产物是菌体本身：过滤、沉淀、干燥'),
        ('7', '获得产品', '得到最终发酵产品'),
    ]

    for num, title, desc in steps:
        body_content.append(make_para(
            make_accent_run(f'【{num}】', size=24) + make_heading_run(title, size=24),
            spacing_before=160, spacing_after=80
        ))
        body_content.append(make_para(make_run(desc, size=20), spacing_before=0, spacing_after=160))

    # Page break
    body_content.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # === 二、发酵工程的特点 ===
    body_content.append(make_para(make_heading_run('二、发酵工程的特点', size=44), spacing_before=0, spacing_after=300))

    chars = [
        ('产物专一', '发酵工程生产的产物具有高度特异性，即特定的微生物产生特定的代谢产物。'),
        ('生产条件温和', '一般在常温常压下进行，不需要高温高压等苛刻条件。'),
        ('原料丰富廉价', '可以利用农副产品、工业废水、废弃农作物等作为发酵原料。'),
        ('废弃物污染小', '发酵工程的废弃物多为天然物质，可被生物降解，对环境友好。'),
    ]

    for title, desc in chars:
        body_content.append(make_para(
            make_run('◆ ', size=28, color='2E75B6') + make_heading_run(title, size=28),
            spacing_before=200, spacing_after=100
        ))
        body_content.append(make_para(make_run(desc, size=22), spacing_before=0, spacing_after=300))

    # Page break
    body_content.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # === 三、发酵工程的应用 ===
    body_content.append(make_para(make_heading_run('三、发酵工程的应用', size=44), spacing_before=0, spacing_after=300))

    apps = [
        ('食品工业', [
            '酱油生产：利用米曲霉发酵大豆制成',
            '柠檬酸：黑曲霉发酵淀粉类物质',
            '味精（谷氨酸）：谷氨酸棒状杆菌发酵',
            '酶制剂：淀粉酶、果胶酶、蛋白酶等'
        ]),
        ('医药工业', [
            '基因工程药物：胰岛素、干扰素、疫苗等',
            '抗生素：青霉素、链霉素等',
            '维生素：维生素C、维生素B12等'
        ]),
        ('农牧业', [
            '微生物肥料：根瘤菌肥、固氮菌肥',
            '微生物农药：苏云金杆菌（Bt）',
            '微生物饲料：单细胞蛋白（SCP）'
        ]),
        ('其他方面', [
            '能源生产：利用废料发酵产生酒精、乙烯',
            '洗涤剂：含酶洗衣粉',
            '环保：生物降解塑料、污水处理'
        ]),
    ]

    for category, items in apps:
        body_content.append(make_para(
            make_accent_run(f'【{category}】', size=28),
            spacing_before=300, spacing_after=150
        ))
        for item in items:
            body_content.append(make_para(
                make_run(f'• {item}', size=22),
                spacing_before=80, spacing_after=80
            ))

    # Build complete document.xml
    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
            xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
            xmlns:o="urn:schemas-microsoft-com:office:office"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
            xmlns:v="urn:schemas-microsoft-com:vml"
            xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:w10="urn:schemas-microsoft-com:office:word"
            xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
            xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
            xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
            xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
            xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
            xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
            mc:Ignorable="w14 w15 wp14">
  <w:body>
    {''.join(body_content)}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="720" w:footer="720"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    # [Content_Types].xml
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>'''

    # _rels/.rels
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    # word/_rels/document.xml.rels
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>'''

    # Create the docx file (which is a zip file)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/_rels/document.xml.rels', doc_rels)

    print(f"Document created: {output_path}")

if __name__ == '__main__':
    create_minimal_docx(OUTPUT_PATH)