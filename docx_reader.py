import zipfile
import os
import xml.etree.ElementTree as ET

def extract_docx_xml(docx_path, output_dir):
    """从docx文件中提取XML文件"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    
    return output_dir

def read_docx_content(docx_path, extract_dir=None):
    """读取docx文件内容"""
    temp_dir = extract_dir or os.path.join(os.path.dirname(docx_path), "temp_extract")
    
    try:
        extract_docx_xml(docx_path, temp_dir)
        
        # 读取document.xml文件
        doc_path = os.path.join(temp_dir, "word", "document.xml")
        
        if not os.path.exists(doc_path):
            return "文档格式错误或无法读取内容"
        
        # 解析XML
        tree = ET.parse(doc_path)
        root = tree.getroot()
        
        # 定义命名空间
        namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        }
        
        # 提取文本内容
        paragraphs = []
        for para in root.findall('.//w:p', namespaces):
            texts = []
            for text in para.findall('.//w:t', namespaces):
                if text.text:
                    texts.append(text.text)
            if texts:
                paragraphs.append(''.join(texts))
        
        return '\n'.join(paragraphs)
    
    except Exception as e:
        return f"读取文档时出错: {str(e)}"
    
    finally:
        # 如果没有提供extract_dir，清理临时目录
        if not extract_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    # 示例调用
    docx_path = "example.docx"
    content = read_docx_content(docx_path)
    print(content) 