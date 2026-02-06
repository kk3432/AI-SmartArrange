import os
from pathlib import Path

class Config:
    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key-here")
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    DEEPSEEK_MODEL = "deepseek-chat"
    
    # 文件路径配置
    SOURCE_DIR = Path.home() / "Downloads"  # 默认扫描下载文件夹
    TARGET_DIR = Path.home() / "Documents" / "OrganizedFiles"
    
    # 文件类型配置
    SUPPORTED_EXTENSIONS = {
        '.txt', '.md', '.pdf', '.doc', '.docx', '.xls', '.xlsx',
        '.ppt', '.pptx', '.jpg', '.jpeg', '.png', '.gif'
    }
    
    # 分类配置
    CATEGORIES = {
        '文档': ['.txt', '.md', '.doc', '.docx', '.pdf'],
        '表格': ['.xls', '.xlsx', '.csv'],
        '演示文稿': ['.ppt', '.pptx'],
        '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        '代码': ['.py', '.js', '.java', '.cpp', '.html', '.css'],
        '压缩包': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        '音频': ['.mp3', '.wav', '.flac'],
        '视频': ['.mp4', '.avi', '.mov', '.mkv']
    }
    
    # API提示词模板
    CATEGORY_PROMPT = """请根据以下文件内容分析文件类型和用途，返回最合适的分类标签。
    只返回一个分类标签，不要有其他内容。

    可选的分类标签：
    - 工作文档
    - 学习资料
    - 个人文件
    - 财务记录
    - 家庭照片
    - 项目文件
    - 临时文件
    - 重要备份
    - 娱乐媒体
    - 其他

    文件内容摘要：
    {content}

    请返回最合适的分类标签："""
