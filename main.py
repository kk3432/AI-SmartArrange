#!/usr/bin/env python3
import argparse
from pathlib import Path
from dotenv import load_dotenv
import os

from config import Config
from file_scanner import FileScanner
from deepseek_client import DeepSeekClient
from organizer import FileOrganizer

def main():
    # 加载环境变量
    load_dotenv()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='使用DeepSeek API自动整理文件')
    parser.add_argument('--source', type=str, help='源目录路径')
    parser.add_argument('--target', type=str, help='目标目录路径')
    parser.add_argument('--api-key', type=str, help='DeepSeek API密钥')
    parser.add_argument('--dry-run', action='store_true', help='只分析不移动文件')
    parser.add_argument('--category-map', type=str, help='分类映射JSON文件')
    
    args = parser.parse_args()
    
    # 更新配置
    if args.source:
        Config.SOURCE_DIR = Path(args.source)
    if args.target:
        Config.TARGET_DIR = Path(args.target)
    if args.api_key:
        Config.DEEPSEEK_API_KEY = args.api_key
    
    # 检查API密钥
    if Config.DEEPSEEK_API_KEY == "your-api-key-here":
        print("请设置DeepSeek API密钥:")
        print("1. 在.env文件中设置 DEEPSEEK_API_KEY")
        print("2. 或使用 --api-key 参数")
        print("3. 或在config.py中直接设置")
        return
    
    print(f"扫描目录: {Config.SOURCE_DIR}")
    print(f"目标目录: {Config.TARGET_DIR}")
    
    # 初始化组件
    scanner = FileScanner(Config.SOURCE_DIR)
    deepseek = DeepSeekClient()
    organizer = FileOrganizer(Config.TARGET_DIR)
    
    try:
        # 步骤1: 扫描文件
        print("\n正在扫描文件...")
        files_with_content = scanner.get_files_with_content()
        
        if not files_with_content:
            print("未找到可处理的文件")
            return
        
        # 步骤2: 使用DeepSeek分析文件
        print("\n正在使用DeepSeek分析文件内容...")
        files_info = []
        for file_path, content in files_with_content:
            # 为每个文件创建简短描述
            file_description = f"文件名: {file_path.name}\n内容摘要:\n{content[:1000]}"
            files_info.append((str(file_path), file_description))
        
        # 批量分析
        categories = deepseek.batch_analyze(files_info)
        
        # 步骤3: 整理文件
        print("\n正在整理文件...")
        
        # 加载分类映射（如果有）
        category_mapping = {}
        if args.category_map:
            import json
            with open(args.category_map, 'r') as f:
                category_mapping = json.load(f)
        
        if args.dry_run:
            print("\n【DRY RUN模式 - 不实际移动文件】")
            print("分类结果:")
            for file_path_str, category in categories.items():
                file_path = Path(file_path_str)
                print(f"  {file_path.name} -> {category}")
        else:
            # 实际移动文件
            moved_files, skipped_files = organizer.organize_files(categories, category_mapping)
            
            # 生成报告
            report = organizer.generate_report(moved_files, skipped_files)
            
            print(f"\n整理完成！")
            print(f"移动了 {report['total_moved']} 个文件")
            print(f"跳过了 {report['total_skipped']} 个文件")
            print(f"报告已保存至: {report['target_directory']}/organization_report.json")
    
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()
