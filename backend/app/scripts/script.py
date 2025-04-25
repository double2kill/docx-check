from docx import Document
from docx.shared import Pt
import re
import json
from typing import Dict, List

class DocxParserPro:
    def __init__(self):
        self.global_index = 0
        self.elements = []
        self.heading_patterns = [
            (r'^第[一二三四五六七八九十]+章\s', 1),
            (r'^第[1234567890]+章\s', 1),
            (r'^\d+\.\d+(\.\d+)*\s', lambda m: m.group().count('.')),
            (r'^[（$][一二三四五六七八九十][）$]', 2),
            (r'^[①②③④⑤⑥⑦⑧⑨⑩]', 3)
        ]
        self.content_patterns = {
            "摘要": r'^摘要[：\s]',
            "关键词": r'^关键[词字][：\s]',
            "图注": r'^图\s*\d+[.．、]\s*',
            "表注": r'^表\s*\d+[.．、]\s*',
            "参考文献": r'^参考文献|^\[\d+\]',
            "level_1": r'^[一二三四五六七八九十]、',
            "level_2": r'^（[一二三四五六七八九十]）',
            "level_3": r'^\d+、',
            "level_4": r'^\(\d+\)',
            "level_5": r'^[①②③④⑤⑥⑦⑧⑨⑩]'
        }

    def _truncate_text(self, text: str) -> str:
        return text if len(text) <= 20 else f"{text[:10]}...{text[-10:]}"

    def _get_line_spacing(self, fmt) -> Dict:
        """精确解析行间距并确保数值类型"""
        try:
            if fmt.line_spacing_rule:
                return {
                    "type": "multiple",
                    "value": round(float(fmt.line_spacing), 2)
                }
            return {
                "type": "exact",
                "value": round(float(fmt.line_spacing.pt), 1),
                "unit": "pt"
            }
        except:
            return {"type": "unknown", "value": 1.5}

    def _parse_indent(self, fmt) -> Dict:
        """解析缩进参数（数值类型）"""
        def get_pt(value):
            return round(value.pt, 1) if value else 0
            
        return {
            "first_line": get_pt(fmt.first_line_indent),
            "left": get_pt(fmt.left_indent),
            "right": get_pt(fmt.right_indent),
            "unit": "pt"
        }

    def _parse_spacing(self, fmt) -> Dict:
        """解析间距参数（数值类型）"""
        def get_pt(value):
            return round(value.pt, 1) if value else 0
            
        return {
            "before": get_pt(fmt.space_before),
            "after": get_pt(fmt.space_after),
            "unit": "pt"
        }

    def _parse_paragraph_format(self, paragraph) -> Dict:
        """综合解析段落格式"""
        fmt = paragraph.paragraph_format
        return {
            "alignment": self._parse_alignment(paragraph),
            "line_spacing": self._get_line_spacing(fmt),
            "indentation": self._parse_indent(fmt),
            "spacing": self._parse_spacing(fmt),
            "keep_lines": fmt.keep_together,
            "page_break": fmt.page_break_before
        }

    def _parse_alignment(self, paragraph):
        """安全解析对齐方式"""
        try:
            return str(paragraph.alignment).split('.')[-1] if paragraph.alignment else "LEFT"
        except:
            return "LEFT"

    def _detect_content_type(self, text: str, style: Dict) -> str:
        text = text.strip()
        
        if not text:
            return "空白段落"

        for content_type, pattern in self.content_patterns.items():
            if re.match(pattern, text):
                return content_type

        if style["bold"] and style["size_pt"] >= 16:
            return "标题"
        elif style["size_pt"] >= 14:
            return "小标题"
        elif re.match(r'^\d+\s*[\.、]', text):
            return "编号列表"
        
        return "正文"

    def _parse_style_features(self, paragraph) -> Dict:
        style = {
            "font": "宋体",
            "size_pt": 12.0,
            "bold": False,
            "italic": False,
            "color": "#000000"
        }

        if paragraph.runs:
            run = paragraph.runs[0]
            try:
                style.update({
                    "font": run.font.name or "宋体",
                    "size_pt": float(run.font.size.pt) if run.font.size else 12.0,
                    "bold": run.font.bold,
                    "italic": run.font.italic,
                    "color": self._get_font_color(run)
                })
            except:
                pass
        return style

    def _get_font_color(self, run):
        """解析字体颜色"""
        try:
            if run.font.color.rgb:
                return f"#{run.font.color.rgb:06X}"
        except:
            return "#000000"

    def process_document(self, file_path: str) -> List[Dict]:
        doc = Document(file_path)
        
        for para in doc.paragraphs:
            if not para.text.strip():
                continue
            
            style = self._parse_style_features(para)
            content_type = self._detect_content_type(para.text, style)
            
            element = {
                "content": para.text,
                "position": {
                    "start": self.global_index,
                    "end": self.global_index + len(para.text)
                },
                "formatting": self._parse_paragraph_format(para),
                "style": style,
                "heading_info": self._detect_heading(para),
                "content_type": content_type
            }
            
            self.elements.append(element)
            self.global_index += len(para.text) + 1
        
        return self.elements

    def _detect_heading(self, paragraph) -> Dict:
        """改进的标题检测逻辑"""
        fmt = self._parse_paragraph_format(paragraph)
        style = self._parse_style_features(paragraph)
        text = paragraph.text.strip()

        heading_features = {
            "is_heading": False,
            "level": 0,
            "evidence": []
        }

        # 规则1：内置标题样式
        if "Heading" in paragraph.style.name:
            try:
                level = int(paragraph.style.name.split()[-1])
                heading_features.update({
                    "is_heading": True,
                    "level": level,
                    "evidence": ["内置标题样式"]
                })
                return heading_features
            except:
                pass

        # 规则2：行间距特征（使用数值类型比较）
        line_spacing = fmt["line_spacing"]["value"]
        if isinstance(line_spacing, (int, float)) and line_spacing < 1.2:
            heading_features["evidence"].append(f"紧凑行间距({line_spacing})")

        # 规则3：格式特征判断
        if style["bold"] and style["size_pt"] >= 14:
            heading_features["evidence"].append("加粗大字号")
            if fmt["alignment"] == "CENTER":
                heading_features.update({"is_heading": True, "level": 1})
            else:
                heading_features.update({"is_heading": True, "level": 2})

        # 规则4：段前间距特征（数值类型判断）
        if fmt["spacing"]["before"] > 0:
            heading_features["evidence"].append(f"段前距 {fmt['spacing']['before']}pt")

        # 规则5：编号列表检测
        if paragraph._element.pPr.numPr is not None:
            heading_features.update({
                "is_heading": True,
                "level": 3,
                "evidence": ["编号列表"]
            })

        return heading_features

    def save_report(self, output_path: str):
        report = {
            "metadata": {
                "total_characters": self.global_index,
                "paragraphs": len(self.elements),
                "headings": sum(1 for e in self.elements if e["heading_info"]["is_heading"])
            },
            "document_structure": self.elements
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    parser = DocxParserPro()
    parser.process_document("input.docx")
    parser.save_report("advanced_report.json")
    print("文档解析完成，完整版式信息已保存至 advanced_report.json")