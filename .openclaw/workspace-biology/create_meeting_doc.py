#!/usr/bin/env python3
"""Create meeting minutes Word document using only stdlib"""

import zipfile
import os

OUTPUT_PATH = "/home/hochoy/.openclaw/workspace-biology/output/高中生物教学分析会议记录.docx"

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

def xml_escape(text):
    return (text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;'))

def make_paragraph(text, bold=False, font_size=None, align=None, space_before=None, space_after=None):
    rPr_children = ""
    if bold:
        rPr_children += "<w:b/>"
    if font_size:
        rPr_children += f"<w:sz w:val='{font_size}'/><w:szCs w:val='{font_size}'/>"
    
    rPr = f"<w:rPr>{rPr_children}</w:rPr>" if rPr_children else ""
    
    pPr_children = ""
    if align:
        pPr_children += f"<w:jc w:val='{align}'/>"
    if space_before is not None:
        pPr_children += f"<w:spacing w:before='{space_before}'/>"
    if space_after is not None:
        pPr_children += f"<w:spacing w:after='{space_after}'/>"
    
    pPr = f"<w:pPr>{pPr_children}</w:pPr>" if pPr_children else ""
    
    return f"<w:p>{pPr}<w:r>{rPr}<w:t xml:space='preserve'>{xml_escape(text)}</w:t></w:r></w:p>"

def make_table_row(cells, is_header=False):
    row_xml = "<w:tr>"
    for cell in cells:
        shading = "<w:shd w:val='clear' w:color='auto' w:fill='D9E2F3'/>" if is_header else ""
        row_xml += f"<w:tc><w:tcPr><w:tcW w:w='0' w:type='auto'/>{shading}</w:tcPr><w:p><w:r><w:rPr><w:b/></w:rPr><w:t xml:space='preserve'>{xml_escape(cell)}</w:t></w:r></w:p></w:tc>"
    row_xml += "</w:tr>"
    return row_xml

def build_document():
    title = make_paragraph("高中生物教学分析会议记录", bold=True, font_size='36', align='center', space_after='400')
    date_para = make_paragraph("日期：2026年4月10日", align='center', space_after='400')
    section1 = make_paragraph("一、各年级学习建议", bold=True, font_size='28', space_before='240', space_after='200')
    
    table_header = make_table_row(["年级", "建议"], is_header=True)
    table_row1 = make_table_row(["高一", "扎实必修一、二的基础，多练各种习题，不要追速度"])
    table_row2 = make_table_row(["高二", "开始必修一、必修二的加强，提升能力"])
    table_row3 = make_table_row(["高三", "多练选择题，多考、多测"])
    
    table = f"<w:tbl><w:tblPr><w:tblStyle w:val='TableGrid'/><w:tblW w:w='0' w:type='auto'/><w:tblBorders><w:top w:val='single' w:sz='4' w:space='0' w:color='auto'/><w:left w:val='single' w:sz='4' w:space='0' w:color='auto'/><w:bottom w:val='single' w:sz='4' w:space='0' w:color='auto'/><w:right w:val='single' w:sz='4' w:space='0' w:color='auto'/><w:insideH w:val='single' w:sz='4' w:space='0' w:color='auto'/><w:insideV w:val='single' w:sz='4' w:space='0' w:color='auto'/></w:tblBorders></w:tblPr><w:tr>{table_header}</w:tr><w:tr>{table_row1}</w:tr><w:tr>{table_row2}</w:tr><w:tr>{table_row3}</w:tr></w:tbl>"
    
    section2 = make_paragraph("二、客观原因分析", bold=True, font_size='28', space_before='360', space_after='200')
    intro = make_paragraph("经分析，当前教学存在以下客观问题：", space_after='120')
    
    reasons = [
        ("1. 阅卷标准变化", "主观题得分下降"),
        ("2. 课时不足", "高一、高二课时不够，周测频率低或缺失"),
        ("3. 师资不稳定", "频繁换老师"),
        ("4. 训练时间不足", "主观题书写量大，需更多训练时间才能达到拿分标准"),
        ("5. 学生水平差异", "物化生两极分化明显，同班学生水平相差明显"),
        ("6. 学生态度问题", "平时考试存在\"做假\"现象，对生物学科的重视程度需转变"),
    ]
    
    reason_paras = []
    for title, desc in reasons:
        reason_paras.append(make_paragraph(f"• {title}：{desc}", space_after='80'))
    
    section3 = make_paragraph("三、改进方向", bold=True, font_size='28', space_before='360', space_after='200')
    
    improvements = [
        "高一、高二：夯实基础，增加练习量，建立稳定周测机制",
        "高三：强化选择题训练，增加考试频次",
        "整体：稳定师资队伍，统一阅卷标准，加强学风建设",
    ]
    
    improvement_paras = []
    for imp in improvements:
        improvement_paras.append(make_paragraph(f"• {imp}", space_after='80'))
    
    content = title + date_para + section1 + table + section2 + intro + "".join(reason_paras) + section3 + "".join(improvement_paras)
    
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

def build_styles():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:rPr>
      <w:rFonts w:ascii="宋体" w:hAnsi="宋体" w:eastAsia="宋体"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
</w:styles>"""

def build_rels():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

def build_content_types():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

def build_root_rels():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

def create_docx():
    with zipfile.ZipFile(OUTPUT_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", build_content_types())
        zf.writestr("_rels/.rels", build_root_rels())
        zf.writestr("word/document.xml", build_document())
        zf.writestr("word/styles.xml", build_styles())
        zf.writestr("word/_rels/document.xml.rels", build_rels())
    print(f"Document created: {OUTPUT_PATH}")

if __name__ == "__main__":
    create_docx()