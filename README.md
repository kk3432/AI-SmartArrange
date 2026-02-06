# AI-SmartArrange
使用DeepSeek API的智能文件整理工具，自动分析、分类和组织您的本地文件。  ## 特性 - 🤖 AI驱动的内容分析 - 📁 智能自动分类   - 🔄 安全文件整理 - 📊 详细整理报告
# 智能文件整理工具 📂🤖

使用DeepSeek API自动分析和整理本地文件，让杂乱的文件变得井井有条。

## ✨ 功能特性

- **智能分析**：利用DeepSeek AI分析文件内容，理解文件用途
- **自动分类**：根据分析结果将文件移动到相应分类文件夹
- **多格式支持**：支持文本、文档、表格、图片等多种文件格式
- **安全可靠**：可预览分类结果后再执行，避免误操作
- **详细报告**：生成完整的整理报告，记录所有操作
- **灵活配置**：支持自定义分类规则和文件类型

## 📦 安装步骤

### 1. 获取项目
```bash
# 克隆项目
git clone <repository-url>
cd file-organizer

# 或者直接下载项目文件
```

### 2. 安装依赖
```bash
# 使用pip安装所需包
pip install -r requirements.txt
```

### 3. 配置API密钥

**方法1：使用环境变量（推荐）**
创建 `.env` 文件：
```bash
DEEPSEEK_API_KEY=你的API密钥
```

**方法2：直接修改配置文件**
编辑 `config.py`：
```python
DEEPSEEK_API_KEY = "你的实际API密钥"
```

**方法3：命令行参数传递**
```bash
python main.py --api-key sk-xxxxxxx
```

### 4. 获取DeepSeek API密钥
1. 访问 [DeepSeek官网](https://www.deepseek.com/)
2. 注册/登录账户
3. 进入API管理页面
4. 创建新的API密钥并复制

## 🚀 快速开始

### 基本用法
```bash
# 整理下载文件夹（默认配置）
python main.py
```

### 指定目录
```bash
# 整理指定文件夹到目标位置
python main.py --source ~/Downloads --target ~/Documents/SortedFiles
```

### 预览模式
```bash
# 只分析不移动文件，查看分类结果
python main.py --dry-run
```

## 📁 项目结构

```
file-organizer/
├── main.py              # 主程序入口
├── config.py           # 配置文件
├── file_scanner.py     # 文件扫描和内容提取
├── deepseek_client.py  # DeepSeek API交互
├── organizer.py        # 文件整理逻辑
├── requirements.txt    # Python依赖包
├── .env.example       # 环境变量示例
└── README.md          # 本文件
```

## 🔧 配置说明

### 修改默认目录
编辑 `config.py`：
```python
# 修改默认源目录
SOURCE_DIR = Path.home() / "Downloads"  # 改为你的目录

# 修改默认目标目录
TARGET_DIR = Path.home() / "Documents" / "OrganizedFiles"
```

### 扩展支持的文件类型
```python
SUPPORTED_EXTENSIONS = {
    '.txt', '.md', '.pdf', '.doc', '.docx',
    '.xls', '.xlsx', '.ppt', '.pptx',
    '.jpg', '.jpeg', '.png', '.gif',
    # 添加更多扩展名...
}
```

### 自定义分类
```python
CATEGORIES = {
    '文档': ['.txt', '.md', '.doc', '.docx', '.pdf'],
    '表格': ['.xls', '.xlsx', '.csv'],
    '图片': ['.jpg', '.jpeg', '.png', '.gif'],
    # 添加更多分类...
}
```

## 📄 支持的文件格式

| 文件类型 | 扩展名 | 备注 |
|---------|--------|------|
| 文本文件 | .txt, .md | 完整内容分析 |
| PDF文档 | .pdf | 提取前3页文本 |
| Word文档 | .doc, .docx | 提取前50段 |
| Excel表格 | .xls, .xlsx | 提取前100行 |
| 演示文稿 | .ppt, .pptx | 支持基础分析 |
| 图片文件 | .jpg, .png等 | 基于文件名分析 |
| 压缩文件 | .zip, .rar等 | 分类但不分析内容 |

## 🧠 分类逻辑

### AI分析分类
DeepSeek会根据文件内容分析出最合适的分类：

- **工作文档** - 工作报告、会议记录等
- **学习资料** - 课程材料、学习笔记
- **个人文件** - 个人文档、日记等
- **财务记录** - 账单、发票、财务报表
- **家庭照片** - 照片、家庭影像
- **项目文件** - 项目文档、代码文件
- **临时文件** - 临时下载、缓存文件
- **重要备份** - 备份文件、重要文档
- **娱乐媒体** - 音乐、视频、游戏
- **其他** - 无法明确分类的文件

### 优先级规则
1. AI分析结果优先
2. 文件扩展名作为辅助参考
3. 可配置自定义分类映射

## ⚙️ 高级用法

### 使用分类映射文件
```bash
# 创建category_map.json
{
    "工作文档": "办公文件",
    "学习资料": "教育资料",
    "临时文件": "待处理"
}

# 运行程序
python main.py --category-map category_map.json
```

### 定时自动整理（Linux/macOS）
```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点自动整理
0 2 * * * cd /path/to/file-organizer && python main.py
```

### 只处理特定类型文件
修改 `config.py` 中的 `SUPPORTED_EXTENSIONS`，只保留需要的扩展名。

## ⚠️ 注意事项

1. **首次使用前请备份重要文件**
2. **API调用有额度限制**，大量文件可能需要分批处理
3. **大文件处理较慢**，建议先测试少量文件
4. **加密或损坏的文件可能无法读取**
5. **建议先使用 `--dry-run` 预览分类结果**

## 🔍 故障排除

### 常见问题

**Q: API密钥无效**
```
错误：API请求失败: 401
```
解决方案：检查API密钥是否正确，是否已激活

**Q: 文件无法读取**
```
错误：读取文件xxx时出错: [错误信息]
```
解决方案：检查文件权限和格式是否支持

**Q: 分类结果不准确**
解决方案：可以创建自定义分类映射表调整

**Q: 处理速度太慢**
解决方案：减少一次处理的文件数量，或调整API调用间隔

### 调试模式
```bash
# 查看详细错误信息
python main.py 2> error.log
```

## 📊 整理报告示例

整理完成后会生成 `organization_report.json`：
```json
{
    "total_moved": 42,
    "total_skipped": 3,
    "timestamp": "2024-01-15T14:30:00",
    "target_directory": "/Users/name/Documents/OrganizedFiles",
    "moved_files": [
        ["report.pdf", "工作文档/20240115_143000_report.pdf"],
        ...
    ]
}
```

## 🔄 恢复文件

如果整理后需要恢复：
1. 查看整理报告找到原位置
2. 手动将文件移回原目录
3. 或使用备份文件

## 🤝 贡献指南

欢迎提交Issue和Pull Request：
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。
5. **建立工作流**：配合其他工具自动化整个流程

**让AI成为你的数字管家，告别杂乱的文件世界！**
