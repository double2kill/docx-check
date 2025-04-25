from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import tempfile
from app.scripts.doc_parser import DocxStructParser

router = APIRouter()

@router.post("/upload-docx")
async def upload_docx(file: UploadFile = File(...)):
    # 检查文件类型
    if not file.filename.endswith(('.docx', '.doc')):
        raise HTTPException(status_code=400, detail="只支持.docx或.doc格式文件")
    
    try:
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp:
            temp_path = temp.name
            content = await file.read()
            temp.write(content)
        
        # 解析文档
        parser = DocxStructParser()
        result = parser.parse(temp_path)
        
        # 清理临时文件
        os.unlink(temp_path)
        
        return result
    except Exception as e:
        # 确保清理临时文件
        if 'temp_path' in locals():
            try:
                os.unlink(temp_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"文档解析失败: {str(e)}") 