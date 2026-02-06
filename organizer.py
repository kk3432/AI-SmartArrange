import shutil
from pathlib import Path
from datetime import datetime
from config import Config
from typing import Dict
import re

class FileOrganizer:
    def __init__(self, target_dir: Path = None):
        self.target_dir = target_dir or Config.TARGET_DIR
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
    def sanitize_filename(self, filename: str) -> str:
        """清理文件名，移除非法字符"""
        # 移除或替换Windows文件名中的非法字符
        illegal_chars = r'[<>:"/\\|?*\x00-\x1f]'
        filename = re.sub(illegal_chars, '_', filename)
        
        # 限制文件名长度
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:200-len(ext)] + ext
            
        return filename
    
    def organize_files(self, files_info: Dict[Path, str], category_mapping: Dict[str, str] = None):
        """整理文件到目标目录"""
        if category_mapping is None:
            category_mapping = {}
        
        moved_files = []
        skipped_files = []
        
        for file_path, category in files_info.items():
            try:
                # 使用映射表或原始分类
                final_category = category_mapping.get(category, category)
                
                # 创建分类目录
                category_dir = self.target_dir / final_category
                category_dir.mkdir(exist_ok=True)
                
                # 生成新文件名（添加时间戳避免重复）
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"{timestamp}_{file_path.name}"
                new_filename = self.sanitize_filename(new_filename)
                
                # 目标路径
                target_path = category_dir / new_filename
                
                # 移动文件
                shutil.move(str(file_path), str(target_path))
                moved_files.append((file_path, target_path))
                
                print(f"已移动: {file_path.name} -> {final_category}/{new_filename}")
                
            except Exception as e:
                print(f"移动文件 {file_path.name} 时出错: {e}")
                skipped_files.append(file_path)
        
        return moved_files, skipped_files
    
    def create_subdirectories(self, categories: list):
        """创建分类子目录"""
        for category in categories:
            category_dir = self.target_dir / category
            category_dir.mkdir(exist_ok=True)
    
    def generate_report(self, moved_files: list, skipped_files: list):
        """生成整理报告"""
        report = {
            "total_moved": len(moved_files),
            "total_skipped": len(skipped_files),
            "moved_files": [(str(src), str(dst)) for src, dst in moved_files],
            "skipped_files": [str(f) for f in skipped_files],
            "timestamp": datetime.now().isoformat(),
            "target_directory": str(self.target_dir)
        }
        
        # 保存报告
        report_path = self.target_dir / "organization_report.json"
        import json
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
