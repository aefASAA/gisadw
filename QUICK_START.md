# 🚀 快速启动指南

## 📋 文件说明

本程序包含以下核心文件：

- **`smart_launcher.py`** - 🎯 智能启动器（推荐使用）
- **`dependency_checker.py`** - 🔍 依赖检查器
- **`simple_crawler.py`** - 🕷️ 简化版爬虫
- **`web_crawler.py`** - 🕷️ 完整版爬虫
- **`run_crawler.bat`** - 🪟 Windows启动脚本
- **`run_crawler.sh`** - 🐧 Linux/Mac启动脚本

## 🎯 推荐启动方式

### 方法1: 使用智能启动器（强烈推荐）

```bash
python smart_launcher.py
```

**优势：**
- ✅ 自动检测依赖
- ✅ 智能程序选择
- ✅ 错误自动修复
- ✅ 用户友好界面

### 方法2: 使用启动脚本

**Windows用户：**
```bash
# 双击运行
run_crawler.bat

# 或命令行运行
.\run_crawler.bat
```

**Linux/Mac用户：**
```bash
# 添加执行权限
chmod +x run_crawler.sh

# 运行脚本
./run_crawler.sh

# 或使用bash运行
bash run_crawler.sh
```

### 方法3: 直接运行程序

```bash
# 检查依赖
python dependency_checker.py

# 运行简化版爬虫
python simple_crawler.py

# 运行完整版爬虫
python web_crawler.py
```

## 🔍 首次使用建议

1. **运行依赖检查器**
   ```bash
   python dependency_checker.py
   ```
   - 自动检测Python环境
   - 检查并安装缺失的包
   - 确保程序可以正常运行

2. **使用智能启动器**
   ```bash
   python smart_launcher.py
   ```
   - 选择要运行的程序
   - 自动处理依赖问题
   - 提供友好的用户界面

## 🛠️ 依赖包说明

### 必需包（程序运行必需）
- `requests` - HTTP请求库
- `beautifulsoup4` - HTML解析库
- `lxml` - XML/HTML解析器
- `pandas` - 数据处理库
- `openpyxl` - Excel文件处理

### 可选包（增强功能）
- `fake-useragent` - 随机User-Agent
- `selenium` - 浏览器自动化
- `webdriver-manager` - 浏览器驱动管理
- `tqdm` - 进度条显示
- `colorama` - 彩色输出

## 🚨 常见问题解决

### 问题1: Python未安装
```bash
# Windows: 访问 https://www.python.org/downloads/
# Linux: sudo apt-get install python3 python3-pip
# macOS: brew install python3
```

### 问题2: 依赖包缺失
```bash
# 自动安装
python dependency_checker.py

# 手动安装
pip install -r requirements.txt
```

### 问题3: 权限问题
```bash
# Linux/Mac添加执行权限
chmod +x run_crawler.sh

# 或使用bash运行
bash run_crawler.sh
```

### 问题4: 编码问题
```bash
# 设置环境变量
set PYTHONIOENCODING=utf-8  # Windows
export PYTHONIOENCODING=utf-8  # Linux/Mac
```

## 💡 使用技巧

### 快速启动特定程序
```bash
# 直接启动简化版爬虫
python smart_launcher.py simple_crawler.py

# 直接启动完整版爬虫
python smart_launcher.py web_crawler.py
```

### 批量安装依赖
```bash
# 安装所有依赖
pip install -r requirements.txt

# 升级pip
python -m pip install --upgrade pip
```

### 检查程序状态
```bash
# 运行智能启动器，选择"显示状态"
python smart_launcher.py
```

## 📱 跨平台支持

| 平台 | 启动方式 | 推荐方法 |
|------|----------|----------|
| Windows | `run_crawler.bat` | 双击运行 |
| Linux | `run_crawler.sh` | `./run_crawler.sh` |
| macOS | `run_crawler.sh` | `./run_crawler.sh` |
| 所有平台 | `smart_launcher.py` | `python smart_launcher.py` |

## 🎉 开始使用

1. **确保Python 3.7+已安装**
2. **运行依赖检查器**
3. **使用智能启动器选择程序**
4. **开始您的爬虫之旅！**

---

**💡 提示：首次使用建议先运行依赖检查器，确保所有必需的包都已正确安装。**
