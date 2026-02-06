import requests
import json
from config import Config
from typing import Optional, Dict, Any
import time

class DeepSeekClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.DEEPSEEK_API_KEY
        self.api_url = Config.DEEPSEEK_API_URL
        self.model = Config.DEEPSEEK_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze_file_content(self, content: str, filename: str) -> Optional[str]:
        """使用DeepSeek API分析文件内容并返回分类"""
        try:
            # 限制内容长度，避免token超限
            max_length = 4000
            if len(content) > max_length:
                content = content[:max_length] + "..."
            
            prompt = Config.CATEGORY_PROMPT.format(content=content)
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "你是一个专业的文件分类助手。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 100,
                "temperature": 0.3
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                category = result['choices'][0]['message']['content'].strip()
                return category
            else:
                print(f"API请求失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"分析文件时出错: {e}")
            return None
    
    def batch_analyze(self, files_info: list, delay: float = 1.0) -> Dict[str, str]:
        """批量分析多个文件"""
        results = {}
        for filename, content in files_info:
            category = self.analyze_file_content(content, filename)
            if category:
                results[filename] = category
            time.sleep(delay)  # 避免API限制
        return results
