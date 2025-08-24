# 网络关键词爬虫程序

这是一个功能强大的网络关键词爬虫程序，支持多种搜索引擎，可以爬取用户设定的关键词搜索结果。

## 功能特性

- 🔍 **多搜索引擎支持**: 支持百度、必应、搜狗、Google等主流搜索引擎
- 📊 **灵活的输出格式**: 支持Excel、CSV、JSON等多种输出格式
- ⚡ **双模式运行**: 支持requests模式和Selenium模式
- 🎯 **智能过滤**: 内置结果过滤和去重功能
- 📝 **详细日志**: 完整的搜索过程记录
- 🛡️ **反爬虫**: 内置请求头伪装和延迟机制

## 文件说明

### 🕷️ 核心爬虫程序
- `web_crawler.py` - 完整版爬虫程序（功能最全）
- `simple_crawler.py` - 简化版爬虫程序（易于使用）

### 🎯 启动和管理工具
- `smart_launcher.py` - 智能启动器，集成依赖检查和程序选择
- `gui_launcher.py` - 图形化启动器，提供友好的GUI界面
- `gui_crawler.py` - 图形化爬虫界面，直接在GUI中执行爬虫任务

### ⚙️ 配置和依赖管理
- `config.py` - 配置文件（可自定义参数）
- `dependency_checker.py` - 依赖包检测和自动安装脚本
- `install.py` - 一键安装脚本
- `requirements.txt` - Python依赖包列表

### 🚀 启动脚本
- `run_crawler.bat` - Windows命令行启动脚本
- `run_crawler.sh` - Linux/Mac命令行启动脚本
- `run_gui.bat` - Windows图形化启动脚本
- `run_gui.sh` - Linux/Mac图形化启动脚本

### 📚 文档
- `README.md` - 使用说明文档
- `QUICK_START.md` - 快速启动指南

## 安装依赖

在运行程序之前，请先安装所需的Python包：

```bash
pip install -r requirements.txt
```

## 快速开始

### 🎯 方法1: 使用图形化界面（强烈推荐）

**Windows用户：**
```bash
# 双击运行
run_gui.bat

# 或命令行运行
python gui_launcher.py
```

**Linux/Mac用户：**
```bash
# 添加执行权限
chmod +x run_gui.sh

# 运行脚本
./run_gui.sh

# 或直接运行
python gui_launcher.py
```

### 🖥️ 方法2: 使用智能启动器

```bash
python smart_launcher.py
```

### 🕷️ 方法3: 直接运行爬虫程序

```bash
# 简化版爬虫（推荐新手）
python simple_crawler.py

# 完整版爬虫
python web_crawler.py
```

## 使用步骤

1. **运行程序**: 选择上述任一命令运行
2. **输入关键词**: 输入您要搜索的关键词
3. **设置页数**: 设置要搜索的页数（建议2-5页）
4. **选择搜索引擎**: 选择要使用的搜索引擎
5. **等待搜索**: 程序会自动爬取搜索结果
6. **查看结果**: 程序会显示结果摘要
7. **保存结果**: 选择是否保存结果及保存格式

## 配置说明

您可以通过修改 `config.py` 文件来自定义爬虫行为：

### 搜索引擎配置
```python
SEARCH_ENGINES = {
    'baidu': {
        'enabled': True,        # 是否启用
        'max_pages': 5,         # 最大页数
        'delay_range': (1, 3),  # 请求延迟范围
    }
}
```

### 输出配置
```python
OUTPUT_CONFIG = {
    'default_format': 'excel',  # 默认输出格式
    'encoding': 'utf-8-sig',   # 文件编码
}
```

### 爬虫行为配置
```python
CRAWLER_CONFIG = {
    'use_selenium': False,      # 是否使用Selenium
    'retry_times': 3,           # 重试次数
    'random_delay': True,       # 随机延迟
}
```

## 输出格式

程序支持三种输出格式：

- **Excel (.xlsx)**: 适合数据分析，支持中文
- **CSV (.csv)**: 通用格式，可用Excel打开
- **JSON (.json)**: 结构化数据，适合程序处理

## 搜索结果字段

每个搜索结果包含以下信息：

- `title`: 网页标题
- `link`: 网页链接
- `abstract`: 网页摘要
- `source`: 来源网站
- `search_engine`: 搜索引擎名称
- `keyword`: 搜索关键词
- `page`: 搜索结果页码

## 注意事项

1. **遵守网站规则**: 请遵守目标网站的robots.txt和使用条款
2. **控制请求频率**: 程序已内置延迟机制，避免请求过于频繁
3. **网络环境**: Google搜索可能需要代理才能正常访问
4. **反爬虫**: 如遇到反爬虫机制，可尝试启用Selenium模式

## 故障排除

### 常见问题

1. **安装依赖失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Chrome驱动问题**
   - 程序会自动下载Chrome驱动
   - 如失败，请手动安装Chrome浏览器

3. **搜索结果为空**
   - 检查网络连接
   - 尝试减少搜索页数
   - 检查关键词是否有效

4. **保存文件失败**
   - 确保有写入权限
   - 检查磁盘空间
   - 尝试不同的输出格式

### 调试模式

如需调试，可修改配置文件中的日志级别：

```python
LOG_CONFIG = {
    'log_level': 'DEBUG',  # 改为DEBUG级别
}
```

## 高级用法

### 批量搜索

您可以修改程序来支持批量关键词搜索：

```python
keywords = ['关键词1', '关键词2', '关键词3']
for keyword in keywords:
    results = crawler.search_all(keyword, max_pages=2)
    # 处理结果...
```

### 自定义过滤

在配置文件中添加自定义过滤规则：

```python
FILTER_CONFIG = {
    'exclude_domains': ['spam.com', 'ads.com'],
    'include_domains': ['news.com', 'blog.com'],
}
```

## 技术支持

如果您在使用过程中遇到问题，请：

1. 检查错误日志
2. 确认网络连接正常
3. 验证依赖包版本
4. 尝试不同的配置参数

## 免责声明

本程序仅供学习和研究使用，请：

- 遵守相关法律法规
- 尊重网站的使用条款
- 不要用于商业用途
- 不要进行恶意爬取

## 更新日志

- v1.0.0: 初始版本，支持基本搜索功能
- v1.1.0: 添加多搜索引擎支持
- v1.2.0: 增加结果过滤和导出功能
- v1.3.0: 优化性能和稳定性

---

**祝您使用愉快！** 🚀
