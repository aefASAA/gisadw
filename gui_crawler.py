 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图形化爬虫界面
提供友好的GUI界面来执行爬虫任务
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import os
import sys
import subprocess
from datetime import datetime
import json
import logging
import traceback

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('crawler_gui.log', encoding='utf-8')
    ]
)

class CrawlerGUI:
    """图形化爬虫界面"""
    
    def __init__(self):
        """初始化GUI"""
        self.root = tk.Tk()
        self.root.title("🕷️ 网站内容爬虫 - 图形化界面")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)  # 设置最小窗口大小
        self.root.resizable(True, True)
        
        # 设置应用图标（如果有）
        try:
            if os.path.exists("assets/icon.ico"):
                self.root.iconbitmap("assets/icon.ico")
        except Exception:
            pass
            
        # 网站配置
        self.websites = {
            'people': {'name': '人民网（人民日报社）', 'url': 'http://www.people.com.cn'},
            'xinhua': {'name': '新华网（新华社）', 'url': 'http://www.news.cn'},
            'cctv': {'name': '央视网（中央广播电视总台）', 'url': 'https://news.cctv.com'},
            'chinanews': {'name': '中国新闻网（中新社）', 'url': 'https://www.chinanews.com.cn'},
            'gmw': {'name': '光明网（光明日报社）', 'url': 'http://www.gmw.cn'},
            'huanqiu': {'name': '环球网（人民日报社/环球时报）', 'url': 'http://www.huanqiu.com'},
            'ce': {'name': '中国经济网（经济日报社）', 'url': 'http://www.ce.cn'},
            'chinadaily': {'name': '中国日报网（China Daily）', 'url': 'http://www.chinadaily.com.cn'},
            'china': {'name': '中国网（国新办主管）', 'url': 'http://www.china.com.cn'},
            'youth': {'name': '中国青年网（共青团中央）', 'url': 'http://www.youth.cn'},
            'sina_news': {'name': '新浪新闻', 'url': 'https://news.sina.com.cn'},
            'qq_news': {'name': '腾讯新闻', 'url': 'https://news.qq.com'},
            'netease_news': {'name': '网易新闻', 'url': 'https://news.163.com'},
            'sohu_news': {'name': '搜狐新闻', 'url': 'https://news.sohu.com'},
            'ifeng': {'name': '凤凰网', 'url': 'http://www.ifeng.com'},
            'thepaper': {'name': '澎湃新闻', 'url': 'https://www.thepaper.cn'},
            'caixin': {'name': '财新网', 'url': 'https://www.caixin.com'},
            'jiemian': {'name': '界面新闻', 'url': 'https://www.jiemian.com'},
            'yicai': {'name': '第一财经', 'url': 'https://www.yicai.com'},
            'eeo': {'name': '经济观察网', 'url': 'https://www.eeo.com.cn'},
            '36kr': {'name': '36氪', 'url': 'https://36kr.com'},
            'huxiu': {'name': '虎嗅', 'url': 'https://www.huxiu.com'},
            'tmtpost': {'name': '钛媒体', 'url': 'https://www.tmtpost.com'},
            'ifanr': {'name': '爱范儿', 'url': 'https://www.ifanr.com'},
            'sina_tech': {'name': '新浪科技', 'url': 'https://tech.sina.com.cn'},
            'readhub': {'name': 'ReadHub', 'url': 'https://readhub.cn'},
            'kepuchina': {'name': '科普中国网', 'url': 'https://www.kepuchina.cn'},
            'ithome': {'name': 'IT之家', 'url': 'https://www.ithome.com'},
            'geekpark': {'name': '极客公园', 'url': 'https://www.geekpark.net'},
            'feng': {'name': '威锋网', 'url': 'https://www.feng.com'},
            'guokr': {'name': '果壳', 'url': 'https://www.guokr.com'},
            'sspai': {'name': '少数派', 'url': 'https://sspai.com'},
            'dgtle': {'name': '数字尾巴', 'url': 'https://www.dgtle.com'},
            'autohome': {'name': '汽车之家', 'url': 'https://www.autohome.com.cn'},
            'cnbeta': {'name': 'cnBeta', 'url': 'https://www.cnbeta.com.cn'},
            'imooc': {'name': '慕课网手记', 'url': 'https://www.imooc.com/article'},
            '24hmb': {'name': '全天候科技', 'url': 'https://www.24hmb.com'},
            'techweb': {'name': 'TechWeb', 'url': 'https://www.techweb.com.cn'},
            'eastmoney': {'name': '东方财富网', 'url': 'https://www.eastmoney.com'},
            'sina_finance': {'name': '新浪财经', 'url': 'https://finance.sina.com.cn'},
            'qq_finance': {'name': '腾讯财经', 'url': 'https://finance.qq.com'},
            'netease_finance': {'name': '网易财经', 'url': 'https://money.163.com'},
            'sohu_finance': {'name': '搜狐财经', 'url': 'https://business.sohu.com'},
            'ljsw': {'name': '棱镜深网', 'url': 'https://www.ljsw.com'},
            '10jqka': {'name': '同花顺财经', 'url': 'https://www.10jqka.com.cn'},
            'xueqiu': {'name': '雪球', 'url': 'https://xueqiu.com'},
            'cninfo': {'name': '巨潮资讯网', 'url': 'https://www.cninfo.com.cn'},
            'hibor': {'name': '慧博投研', 'url': 'https://www.hibor.com.cn'},
            'wind': {'name': 'Wind金融终端', 'url': 'https://www.wind.com.cn'},
            'wallstreetcn': {'name': '华尔街见闻', 'url': 'https://wallstreetcn.com'},
            'cls': {'name': '财联社', 'url': 'https://www.cls.cn'},
            'stcn': {'name': '证券时报网', 'url': 'https://www.stcn.com'},
            'gelonghui': {'name': '格隆汇', 'url': 'https://www.gelonghui.com'},
            'pedaily': {'name': '投资界', 'url': 'https://www.pedaily.cn'},
            'wabei': {'name': '挖贝网', 'url': 'https://www.wabei.cn'},
            'bloomberg': {'name': 'Bloomberg彭博', 'url': 'https://www.bloomberg.com'},
            'reuters': {'name': 'Reuters路透', 'url': 'https://www.reuters.com'},
            'cnbc': {'name': 'CNBC', 'url': 'https://www.cnbc.com'},
            'ft': {'name': 'Financial Times金融时报', 'url': 'https://www.ft.com'},
            'wsj': {'name': 'Wall Street Journal华尔街日报', 'url': 'https://www.wsj.com'},
            'marketwatch': {'name': 'MarketWatch', 'url': 'https://www.marketwatch.com'},
            'yahoo_finance': {'name': 'Yahoo Finance', 'url': 'https://finance.yahoo.com'},
            'seeking_alpha': {'name': 'Seeking Alpha', 'url': 'https://seekingalpha.com'},
            'investing': {'name': 'Investing.com', 'url': 'https://cn.investing.com'},
            'forbes': {'name': 'Forbes福布斯', 'url': 'https://www.forbes.com'}
        }
        
        # 输出格式
        self.output_formats = {
            'excel': 'Excel文件 (.xlsx)',
            'csv': 'CSV文件 (.csv)',
            'json': 'JSON文件 (.json)'
        }
        
        # 初始化UI变量
        self.keyword_entry = None
        self.engine_var = None
        self.pages_var = None
        self.format_var = None
        self.output_dir_var = None
        self.start_btn = None
        self.stop_btn = None
        self.log_text = None
        self.progress_var = None
        self.progress_bar = None
        self.status_var = None
        
        # 当前任务状态
        self.is_running = False
        self.current_task = None
        self.should_stop = False  # 用于控制爬虫停止
        
        # 检查爬虫模块可用性
        self.check_crawler_modules()
        
        # 创建样式
        self.create_styles()
        
        # 设置UI
        self.setup_ui()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_styles(self):
        """创建自定义样式"""
        style = ttk.Style()
        
        # 检查是否支持主题
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        
        # 创建强调按钮样式
        style.configure('Accent.TButton', 
                        font=('Arial', 10, 'bold'),
                        background='#4CAF50',
                        foreground='white')
        
        # 创建警告按钮样式
        style.configure('Warning.TButton',
                        font=('Arial', 10, 'bold'),
                        background='#f44336',
                        foreground='white')
        
        # 创建小按钮样式
        style.configure('Small.TButton',
                        font=('Arial', 8),
                        padding=(5, 2))
    
    def check_crawler_modules(self):
        """检查爬虫模块是否可用"""
        self.available_modules = {
            'simple_crawler': False,
            'web_crawler': False
        }
        
        try:
            import simple_crawler
            self.available_modules['simple_crawler'] = True
            logging.info("简化爬虫模块加载成功")
        except ImportError as e:
            logging.warning(f"无法加载简化爬虫模块: {e}")
        
        try:
            import web_crawler
            self.available_modules['web_crawler'] = True
            logging.info("完整爬虫模块加载成功")
        except ImportError as e:
            logging.warning(f"无法加载完整爬虫模块: {e}")
        
        # 检查依赖库
        self.check_dependencies()
    
    def check_dependencies(self):
        """检查依赖库"""
        self.dependencies = {
            'pandas': False,
            'openpyxl': False,
            'requests': False,
            'beautifulsoup4': False
        }
        
        try:
            import pandas
            self.dependencies['pandas'] = True
        except ImportError:
            pass
            
        try:
            import openpyxl
            self.dependencies['openpyxl'] = True
        except ImportError:
            pass
            
        try:
            import requests
            self.dependencies['requests'] = True
        except ImportError:
            pass
            
        try:
            import bs4
            self.dependencies['beautifulsoup4'] = True
        except ImportError:
            pass
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="🕷️ 网站内容爬虫", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(side='left')
        
        # 版本信息
        version_label = ttk.Label(title_frame, text="v2.0.0", 
                                 font=('Arial', 10))
        version_label.pack(side='right')
        
        # 创建输入区域
        self.create_input_area(main_frame)
        
        # 创建选项区域
        self.create_options_area(main_frame)
        
        # 创建控制区域
        self.create_control_area(main_frame)
        
        # 创建日志区域
        self.create_log_area(main_frame)
        
        # 创建状态栏
        self.create_status_bar(main_frame)
        
        # 初始化状态
        self.update_ui_state()
    
    def update_ui_state(self):
        """更新UI状态"""
        # 更新状态栏信息
        status_text = "就绪"
        if self.is_running:
            status_text = "正在爬取..."
        self.status_var.set(status_text)
        
        # 更新依赖状态信息
        self.update_dependency_status()
    
    def update_dependency_status(self):
        """更新依赖状态信息"""
        module_status = []
        
        # 爬虫模块状态
        if self.available_modules['simple_crawler']:
            module_status.append("✅ 网站爬虫")
        else:
            module_status.append("❌ 网站爬虫")
            
        if self.available_modules['web_crawler']:
            module_status.append("✅ 高级爬虫")
        else:
            module_status.append("❌ 高级爬虫")
        
        # 依赖库状态
        if hasattr(self, 'dependencies'):
            if self.dependencies['pandas']:
                module_status.append("✅ pandas")
            else:
                module_status.append("❌ pandas")
                
            if self.dependencies['openpyxl']:
                module_status.append("✅ openpyxl")
            else:
                module_status.append("❌ openpyxl")
                
            if self.dependencies['requests']:
                module_status.append("✅ requests")
            else:
                module_status.append("❌ requests")
                
            if self.dependencies['beautifulsoup4']:
                module_status.append("✅ bs4")
            else:
                module_status.append("❌ bs4")
        
        return " | ".join(module_status)
        
    def check_and_install_dependencies(self):
        """检查并安装依赖"""
        missing_deps = []
        
        # 检查缺失的依赖
        if not self.dependencies['pandas']:
            missing_deps.append('pandas')
        if not self.dependencies['openpyxl']:
            missing_deps.append('openpyxl')
        if not self.dependencies['requests']:
            missing_deps.append('requests')
        if not self.dependencies['beautifulsoup4']:
            missing_deps.append('beautifulsoup4')
            
        if not missing_deps:
            messagebox.showinfo("依赖检查", "所有依赖已安装！")
            return
            
        # 询问是否安装缺失的依赖
        if messagebox.askyesno("依赖检查", 
                              f"发现缺失的依赖: {', '.join(missing_deps)}\n\n是否要安装这些依赖?"):
            self.install_dependencies(missing_deps)
    
    def install_dependencies(self, dependencies):
        """安装依赖"""
        try:
            # 创建安装进度窗口
            install_window = tk.Toplevel(self.root)
            install_window.title("安装依赖")
            install_window.geometry("400x300")
            install_window.resizable(False, False)
            install_window.transient(self.root)
            install_window.grab_set()
            
            # 安装信息
            ttk.Label(install_window, text="正在安装依赖...", 
                     font=('Arial', 12)).pack(pady=(20, 10))
            
            # 进度条
            progress = ttk.Progressbar(install_window, mode='indeterminate')
            progress.pack(fill='x', padx=20, pady=10)
            progress.start()
            
            # 日志区域
            log_area = scrolledtext.ScrolledText(install_window, height=10)
            log_area.pack(fill='both', expand=True, padx=20, pady=10)
            
            # 启动安装线程
            def install_thread():
                try:
                    import sys
                    import subprocess
                    
                    log_area.insert('end', f"Python 版本: {sys.version}\n")
                    log_area.insert('end', f"安装路径: {sys.executable}\n")
                    log_area.insert('end', f"开始安装依赖: {', '.join(dependencies)}\n")
                    log_area.see('end')
                    
                    # 使用pip安装依赖
                    for dep in dependencies:
                        log_area.insert('end', f"\n正在安装 {dep}...\n")
                        log_area.see('end')
                        
                        try:
                            # 使用当前Python解释器的pip安装
                            cmd = [sys.executable, "-m", "pip", "install", dep]
                            process = subprocess.Popen(
                                cmd, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,
                                text=True
                            )
                            
                            # 读取输出
                            for line in process.stdout:
                                log_area.insert('end', line)
                                log_area.see('end')
                                
                            # 等待进程完成
                            process.wait()
                            
                            if process.returncode == 0:
                                log_area.insert('end', f"{dep} 安装成功!\n")
                            else:
                                log_area.insert('end', f"{dep} 安装失败! 错误码: {process.returncode}\n")
                                
                                # 读取错误输出
                                for line in process.stderr:
                                    log_area.insert('end', f"错误: {line}\n")
                                    
                        except Exception as e:
                            log_area.insert('end', f"安装 {dep} 时出错: {e}\n")
                    
                    log_area.insert('end', "\n安装完成! 请重启应用以应用更改。\n")
                    log_area.see('end')
                    
                    # 更新UI
                    progress.stop()
                    progress.pack_forget()
                    
                    ttk.Button(install_window, text="关闭", 
                              command=install_window.destroy).pack(pady=10)
                    
                except Exception as e:
                    log_area.insert('end', f"安装过程中出错: {e}\n")
                    log_area.insert('end', traceback.format_exc())
                    log_area.see('end')
                    
                    # 更新UI
                    progress.stop()
                    progress.pack_forget()
                    
                    ttk.Button(install_window, text="关闭", 
                              command=install_window.destroy).pack(pady=10)
            
            # 启动线程
            threading.Thread(target=install_thread, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("错误", f"安装依赖时出错: {e}")
    
    def on_closing(self):
        """窗口关闭事件处理"""
        if self.is_running:
            if messagebox.askyesno("确认", "爬虫任务正在运行，确定要退出吗？"):
                self.should_stop = True
                self.is_running = False
                self.root.destroy()
        else:
            self.root.destroy()
        
    def create_input_area(self, parent):
        """创建输入区域"""
        input_frame = ttk.LabelFrame(parent, text="🔍 爬取设置", padding=15)
        input_frame.pack(fill='x', pady=(0, 15))
        
        # 关键词输入
        keyword_frame = ttk.Frame(input_frame)
        keyword_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(keyword_frame, text="爬取关键词:").pack(side='left')
        self.keyword_entry = ttk.Entry(keyword_frame, width=50)
        self.keyword_entry.pack(side='left', padx=(10, 0), fill='x', expand=True)
        
        # 网站选择
        website_frame = ttk.Frame(input_frame)
        website_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(website_frame, text="目标网站:").pack(side='left')
        
        # 创建网站分类选择
        self.website_category_var = tk.StringVar(value='news')
        category_frame = ttk.Frame(website_frame)
        category_frame.pack(side='left', padx=(10, 0), fill='x', expand=True)
        
        # 网站分类
        self.website_categories = {
            'news': '新闻媒体',
            'tech': '科技媒体', 
            'finance': '财经媒体',
            'international': '国际媒体'
        }
        
        # 分类选择下拉框
        ttk.Label(category_frame, text="分类:").pack(side='left')
        category_combo = ttk.Combobox(category_frame, textvariable=self.website_category_var, 
                                     width=15, state='readonly')
        category_combo.pack(side='left', padx=(5, 10))
        category_combo['values'] = list(self.website_categories.values())
        category_combo.set(self.website_categories['news'])
        category_combo.bind('<<ComboboxSelected>>', self.on_category_selected)
        
        # 网站选择下拉框
        ttk.Label(category_frame, text="网站:").pack(side='left')
        self.website_var = tk.StringVar(value='people')
        self.website_combo = ttk.Combobox(category_frame, textvariable=self.website_var, 
                                         width=30, state='readonly')
        self.website_combo.pack(side='left', padx=(5, 0), fill='x', expand=True)
        
        # 绑定网站选择事件
        self.website_combo.bind('<<ComboboxSelected>>', self.on_website_selected)
        
        # 显示当前选择的网站URL
        self.url_label = ttk.Label(website_frame, text="", font=('Arial', 9))
        self.url_label.pack(side='left', padx=(10, 0))
        
        # 初始化网站分类
        self.update_website_options()
        self.update_url_display()
        
        # 网站信息显示区域
        info_frame = ttk.Frame(input_frame)
        info_frame.pack(fill='x', pady=(5, 0))
        
        self.website_info_label = ttk.Label(info_frame, text="", 
                                           font=('Arial', 9), 
                                           foreground='#666666',
                                           wraplength=600)
        self.website_info_label.pack(fill='x')
        self.update_website_info_display()
        
        # 快速选择按钮区域
        quick_select_frame = ttk.Frame(input_frame)
        quick_select_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Label(quick_select_frame, text="快速选择:", font=('Arial', 9)).pack(side='left')
        
        # 常用网站快速选择按钮
        quick_sites = [
            ('people', '人民网'),
            ('xinhua', '新华网'),
            ('36kr', '36氪'),
            ('eastmoney', '东方财富')
        ]
        
        for key, name in quick_sites:
            btn = ttk.Button(quick_select_frame, text=name, 
                           command=lambda k=key: self.quick_select_website(k),
                           style='Small.TButton')
            btn.pack(side='left', padx=(5, 0))
        
        # 搜索页数
        pages_frame = ttk.Frame(input_frame)
        pages_frame.pack(fill='x')
        
        ttk.Label(pages_frame, text="爬取页数:").pack(side='left')
        self.pages_var = tk.StringVar(value='3')
        pages_spinbox = ttk.Spinbox(pages_frame, from_=1, to=10, 
                                   textvariable=self.pages_var, width=10)
        pages_spinbox.pack(side='left', padx=(10, 0))
        
        ttk.Label(pages_frame, text="页 (1-10)").pack(side='left', padx=(5, 0))
        
    def create_options_area(self, parent):
        """创建选项区域"""
        options_frame = ttk.LabelFrame(parent, text="⚙️ 高级选项", padding=15)
        options_frame.pack(fill='x', pady=(0, 15))
        
        # 输出格式选择
        format_frame = ttk.Frame(options_frame)
        format_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(format_frame, text="输出格式:").pack(side='left')
        self.format_var = tk.StringVar(value='excel')
        
        for i, (key, name) in enumerate(self.output_formats.items()):
            ttk.Radiobutton(format_frame, text=name, variable=self.format_var, 
                           value=key).pack(side='left', padx=(10, 20))
        
        # 输出目录
        output_frame = ttk.Frame(options_frame)
        output_frame.pack(fill='x')
        
        ttk.Label(output_frame, text="输出目录:").pack(side='left')
        self.output_dir_var = tk.StringVar(value=os.getcwd())
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var, width=50)
        output_entry.pack(side='left', padx=(10, 10), fill='x', expand=True)
        
        ttk.Button(output_frame, text="浏览", 
                  command=self.browse_output_dir).pack(side='right')
        
    def create_control_area(self, parent):
        """创建控制区域"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill='x', pady=(0, 15))
        
        # 左侧按钮
        left_frame = ttk.Frame(control_frame)
        left_frame.pack(side='left')
        
        self.start_btn = ttk.Button(left_frame, text="🚀 开始爬取", 
                                   command=self.start_crawling, style='Accent.TButton')
        self.start_btn.pack(side='left', padx=(0, 10))
        
        self.stop_btn = ttk.Button(left_frame, text="⏹️ 停止爬取", 
                                  command=self.stop_crawling, state='disabled')
        self.stop_btn.pack(side='left', padx=(0, 10))
        
        # 右侧按钮
        right_frame = ttk.Frame(control_frame)
        right_frame.pack(side='right')
        
        ttk.Button(right_frame, text="🗑️ 清空日志", 
                  command=self.clear_log).pack(side='right', padx=(10, 0))
        
        ttk.Button(right_frame, text="📁 打开输出目录", 
                  command=self.open_output_dir).pack(side='right', padx=(10, 0))
        
        ttk.Button(right_frame, text="❓ 帮助", 
                  command=self.show_help).pack(side='right')
        
    def create_log_area(self, parent):
        """创建日志区域"""
        log_frame = ttk.LabelFrame(parent, text="📝 爬取日志", padding=15)
        log_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap='word')
        self.log_text.pack(fill='both', expand=True)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(log_frame, variable=self.progress_var, 
                                          maximum=100)
        self.progress_bar.pack(fill='x', pady=(10, 0))
        
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill='x')
        
        # 状态信息
        status_info_frame = ttk.Frame(status_frame)
        status_info_frame.pack(fill='x')
        
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(status_info_frame, textvariable=self.status_var, 
                                relief='sunken', anchor='w')
        status_label.pack(side='left', fill='x', expand=True)
        
        # 模块状态
        module_status = self.update_dependency_status()
        
        self.module_status_var = tk.StringVar(value=module_status)
        module_label = ttk.Label(status_info_frame, textvariable=self.module_status_var, 
                                relief='sunken', anchor='e')
        module_label.pack(side='right')
        
                # 添加依赖检查按钮
        ttk.Button(status_frame, text="检查依赖", 
                  command=self.check_and_install_dependencies).pack(pady=(5, 0))
    
    def on_category_selected(self, event=None):
        """分类选择事件处理"""
        self.update_website_options()
        self.update_url_display()
        self.update_website_info_display()
    
    def on_website_selected(self, event=None):
        """网站选择事件处理"""
        self.update_url_display()
        self.update_website_info_display()
    
    def update_website_options(self):
        """更新网站选项"""
        try:
            selected_category = self.website_category_var.get()
            # 根据分类获取对应的网站key
            category_key = None
            for key, name in self.website_categories.items():
                if name == selected_category:
                    category_key = key
                    break
            
            if category_key:
                # 根据分类筛选网站
                if category_key == 'news':
                    website_keys = ['people', 'xinhua', 'cctv', 'chinanews', 'gmw', 'huanqiu', 
                                  'ce', 'chinadaily', 'china', 'youth', 'sina_news', 'qq_news', 
                                  'netease_news', 'sohu_news', 'ifeng', 'thepaper', 'caixin', 
                                  'jiemian', 'yicai', 'eeo']
                elif category_key == 'tech':
                    website_keys = ['36kr', 'huxiu', 'tmtpost', 'ifanr', 'sina_tech', 'readhub', 
                                  'kepuchina', 'ithome', 'geekpark', 'feng', 'guokr', 'sspai', 
                                  'dgtle', 'autohome', 'cnbeta', 'imooc', '24hmb', 'techweb']
                elif category_key == 'finance':
                    website_keys = ['eastmoney', 'sina_finance', 'qq_finance', 'netease_finance', 
                                  'sohu_finance', 'ljsw', '10jqka', 'xueqiu', 'cninfo', 'hibor', 
                                  'wind', 'wallstreetcn', 'cls', 'stcn', 'gelonghui', 'pedaily', 'wabei']
                elif category_key == 'international':
                    website_keys = ['bloomberg', 'reuters', 'cnbc', 'ft', 'wsj', 'marketwatch', 
                                  'yahoo_finance', 'seeking_alpha', 'investing', 'forbes']
                else:
                    website_keys = ['people']  # 默认
                
                # 更新网站选择下拉框
                website_options = []
                for key in website_keys:
                    if key in self.websites:
                        website_options.append(f"{self.websites[key]['name']} ({key})")
                
                self.website_combo['values'] = website_options
                if website_options:
                    self.website_combo.set(website_options[0])
                    # 更新选中的网站key
                    for key in website_keys:
                        if key in self.websites:
                            self.selected_website_key = key
                            break
                
        except Exception as e:
            logging.error(f"更新网站选项出错: {e}")
    
    def update_url_display(self):
        """更新URL显示"""
        try:
            selected_text = self.website_var.get()
            # 从选择文本中提取网站key
            for key, info in self.websites.items():
                if key in selected_text:
                    self.selected_website_key = key
                    self.url_label.config(text=f"URL: {info['url']}")
                    break
        except Exception as e:
            logging.error(f"更新URL显示出错: {e}")
    
    def update_website_info_display(self):
        """更新网站信息显示"""
        try:
            if hasattr(self, 'selected_website_key') and self.selected_website_key:
                website_info = self.websites.get(self.selected_website_key, {})
                if website_info:
                    # 获取网站分类
                    category_name = "未知分类"
                    for key, name in self.website_categories.items():
                        if key == 'news' and self.selected_website_key in ['people', 'xinhua', 'cctv', 'chinanews', 'gmw', 'huanqiu', 'ce', 'chinadaily', 'china', 'youth', 'sina_news', 'qq_news', 'netease_news', 'sohu_news', 'ifeng', 'thepaper', 'caixin', 'jiemian', 'yicai', 'eeo']:
                            category_name = name
                            break
                        elif key == 'tech' and self.selected_website_key in ['36kr', 'huxiu', 'tmtpost', 'ifanr', 'sina_tech', 'readhub', 'kepuchina', 'ithome', 'geekpark', 'feng', 'guokr', 'sspai', 'dgtle', 'autohome', 'cnbeta', 'imooc', '24hmb', 'techweb']:
                            category_name = name
                            break
                        elif key == 'finance' and self.selected_website_key in ['eastmoney', 'sina_finance', 'qq_finance', 'netease_finance', 'sohu_finance', 'ljsw', '10jqka', 'xueqiu', 'cninfo', 'hibor', 'wind', 'wallstreetcn', 'cls', 'stcn', 'gelonghui', 'pedaily', 'wabei']:
                            category_name = name
                            break
                        elif key == 'international' and self.selected_website_key in ['bloomberg', 'reuters', 'cnbc', 'ft', 'wsj', 'marketwatch', 'yahoo_finance', 'seeking_alpha', 'investing', 'forbes']:
                            category_name = name
                            break
                    
                    info_text = f"📰 {website_info['name']} | 🏷️ {category_name} | 🔗 {website_info['url']}"
                    self.website_info_label.config(text=info_text)
                else:
                    self.website_info_label.config(text="请选择目标网站")
            else:
                self.website_info_label.config(text="请选择目标网站")
        except Exception as e:
            logging.error(f"更新网站信息显示出错: {e}")
    
    def quick_select_website(self, website_key):
        """快速选择网站"""
        try:
            if website_key in self.websites:
                # 找到对应的分类
                category_key = None
                if website_key in ['people', 'xinhua', 'cctv', 'chinanews', 'gmw', 'huanqiu', 'ce', 'chinadaily', 'china', 'youth', 'sina_news', 'qq_news', 'netease_news', 'sohu_news', 'ifeng', 'thepaper', 'caixin', 'jiemian', 'yicai', 'eeo']:
                    category_key = 'news'
                elif website_key in ['36kr', 'huxiu', 'tmtpost', 'ifanr', 'sina_tech', 'readhub', 'kepuchina', 'ithome', 'geekpark', 'feng', 'guokr', 'sspai', 'dgtle', 'autohome', 'cnbeta', 'imooc', '24hmb', 'techweb']:
                    category_key = 'tech'
                elif website_key in ['eastmoney', 'sina_finance', 'qq_finance', 'netease_finance', 'sohu_finance', 'ljsw', '10jqka', 'xueqiu', 'cninfo', 'hibor', 'wind', 'wallstreetcn', 'cls', 'stcn', 'gelonghui', 'pedaily', 'wabei']:
                    category_key = 'finance'
                elif website_key in ['bloomberg', 'reuters', 'cnbc', 'ft', 'wsj', 'marketwatch', 'yahoo_finance', 'seeking_alpha', 'investing', 'forbes']:
                    category_key = 'international'
                
                if category_key:
                    # 设置分类
                    self.website_category_var.set(self.website_categories[category_key])
                    # 更新网站选项
                    self.update_website_options()
                    # 设置网站
                    website_name = f"{self.websites[website_key]['name']} ({website_key})"
                    self.website_var.set(website_name)
                    self.selected_website_key = website_key
                    # 更新显示
                    self.update_url_display()
                    self.update_website_info_display()
                    
                    self.log_message(f"🚀 快速选择网站: {self.websites[website_key]['name']}")
                
        except Exception as e:
            logging.error(f"快速选择网站出错: {e}")
    
    def get_selected_website_info(self):
        """获取当前选择的网站信息"""
        try:
            if hasattr(self, 'selected_website_key'):
                return self.websites.get(self.selected_website_key, None)
            return None
        except Exception as e:
            logging.error(f"获取网站信息出错: {e}")
            return None
        
    def browse_output_dir(self):
        """浏览输出目录"""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def start_crawling(self):
        """开始爬取"""
        if self.is_running:
            messagebox.showwarning("警告", "爬虫正在运行中")
            return
        
        try:
            # 验证输入
            if not self.keyword_entry:
                messagebox.showerror("错误", "界面初始化错误")
                return
                
            keyword = self.keyword_entry.get().strip()
            if not keyword:
                messagebox.showerror("错误", "请输入爬取关键词")
                return
            
            # 获取设置
            if not all([self.website_var, self.pages_var, self.format_var, self.output_dir_var]):
                messagebox.showerror("错误", "界面初始化错误")
                return
                
            website_info = self.get_selected_website_info()
            if not website_info:
                messagebox.showerror("错误", "请选择目标网站")
                return
                
            try:
                pages = int(self.pages_var.get())
            except ValueError:
                messagebox.showerror("错误", "爬取页数必须是数字")
                return
                
            output_format = self.format_var.get()
            output_dir = self.output_dir_var.get()
            
            # 检查输出目录
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir)
                    self.log_message(f"📁 已创建输出目录: {output_dir}")
                except Exception as e:
                    messagebox.showerror("错误", f"无法创建输出目录: {e}")
                    return
            
            # 开始爬取
            self.is_running = True
            self.should_stop = False
            
            # 更新UI状态
            try:
                if self.start_btn and self.start_btn.winfo_exists():
                    self.start_btn.config(state='disabled')
                if self.stop_btn and self.stop_btn.winfo_exists():
                    self.stop_btn.config(state='normal')
                if self.status_var:
                    self.status_var.set("正在爬取...")
                if self.progress_var:
                    self.progress_var.set(0)
            except Exception as e:
                logging.error(f"更新UI状态出错: {e}")
            
            # 在新线程中运行爬虫
            self.current_task = threading.Thread(
                target=self.run_crawler,
                args=(keyword, website_info, pages, output_format, output_dir),
                daemon=True
            )
            self.current_task.start()
            
            # 记录日志
            logging.info(f"开始爬取任务: 关键词={keyword}, 网站={website_info['name']}, 页数={pages}")
            
        except Exception as e:
            self.is_running = False
            messagebox.showerror("错误", f"启动爬虫任务失败: {e}")
            logging.error(f"启动爬虫任务错误: {traceback.format_exc()}")
    
    def run_crawler(self, keyword, website_info, pages, output_format, output_dir):
        """运行爬虫"""
        try:
            # 记录开始时间
            start_time = datetime.now()
            
            # 记录爬虫配置
            self.log_message(f"🚀 开始爬取关键词: {keyword}")
            self.log_message(f"🌐 目标网站: {website_info['name']}")
            self.log_message(f"🔗 网站地址: {website_info['url']}")
            self.log_message(f"📄 爬取页数: {pages}")
            self.log_message(f"💾 输出格式: {self.output_formats[output_format]}")
            self.log_message(f"📁 输出目录: {output_dir}")
            self.log_message("-" * 50)
            
            # 初始化进度条
            try:
                if self.progress_var and self.root and self.root.winfo_exists():
                    self.root.after(0, lambda: self.progress_var.set(10))
            except Exception:
                pass
            
            # 检查是否应该停止
            if self.should_stop:
                self.log_message("⏹️ 爬取任务被用户停止")
                try:
                    if self.status_var:
                        self.status_var.set("任务已停止")
                except Exception:
                    pass
                return
            
            # 调用真实的爬虫程序
            self.log_message("🔄 正在连接目标网站...")
            try:
                if self.progress_var and self.root and self.root.winfo_exists():
                    self.root.after(0, lambda: self.progress_var.set(20))
            except Exception:
                pass
            
            results = self.call_real_crawler(keyword, website_info, pages)
            
            # 检查是否应该停止
            if self.should_stop:
                self.log_message("⏹️ 爬取任务被用户停止")
                try:
                    if self.status_var:
                        self.status_var.set("任务已停止")
                except Exception:
                    pass
                return
            
            # 更新进度条
            try:
                if self.progress_var and self.root and self.root.winfo_exists():
                    self.root.after(0, lambda: self.progress_var.set(70))
            except Exception:
                pass
            
            if results and len(results) > 0 and self.is_running:
                # 记录结果数量
                self.log_message(f"📊 获取到 {len(results)} 条爬取结果")
                
                # 生成输出文件
                self.log_message("💾 正在保存爬取结果...")
                self.generate_output(keyword, results, output_format, output_dir, website_info)
                
                # 计算耗时
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                # 完成进度条
                try:
                    if self.progress_var and self.root and self.root.winfo_exists():
                        self.root.after(0, lambda: self.progress_var.set(100))
                except Exception:
                    pass
                
                self.log_message(f"🎉 爬取任务完成！耗时: {duration:.2f} 秒")
                try:
                    if self.status_var:
                        self.status_var.set("爬取完成")
                except Exception:
                    pass
            elif not self.is_running or self.should_stop:
                self.log_message("⏹️ 爬取任务被用户停止")
                try:
                    if self.status_var:
                        self.status_var.set("任务已停止")
                except Exception:
                    pass
            else:
                self.log_message("❌ 爬取失败，未获得结果")
                try:
                    if self.status_var:
                        self.status_var.set("爬取失败")
                except Exception:
                    pass
                
        except Exception as e:
            self.log_message(f"❌ 爬取过程中出错: {str(e)}")
            logging.error(f"爬虫运行错误: {traceback.format_exc()}")
            try:
                if self.status_var:
                    self.status_var.set("爬取出错")
            except Exception:
                pass
        finally:
            self.is_running = False
            self.should_stop = False
            try:
                if self.root and self.root.winfo_exists():
                    self.root.after(0, self.reset_ui)
            except Exception:
                pass
    
    def call_real_crawler(self, keyword, website_info, pages):
        """调用真实的爬虫程序"""
        try:
            # 检查是否应该停止
            if self.should_stop:
                return None
                
            # 更新进度条
            try:
                if self.progress_var and self.root and self.root.winfo_exists():
                    self.root.after(0, lambda: self.progress_var.set(30))
            except Exception:
                pass
                
            self.log_message(f"🔍 正在爬取网站: {website_info['name']}")
            self.log_message(f"🔗 目标URL: {website_info['url']}")
            
            # 使用通用网站爬虫
            if not self.available_modules['simple_crawler']:
                self.log_message("❌ 爬虫模块未安装，无法继续")
                return None
                
            from simple_crawler import SimpleCrawler
            crawler = SimpleCrawler()
            
            # 调用通用网站爬取方法
            results = crawler.search_website(keyword, website_info['url'], max_pages=pages)
            
            # 检查是否应该停止
            if self.should_stop:
                return None
            
            # 检查是否应该停止
            if self.should_stop:
                return None
                
            # 更新进度条
            try:
                if self.progress_var and self.root and self.root.winfo_exists():
                    self.root.after(0, lambda: self.progress_var.set(50))
            except Exception:
                pass
            
            # 检查结果
            if results and len(results) > 0:
                self.log_message(f"✅ 爬取完成，获得 {len(results)} 个结果")
                return results
            else:
                self.log_message("⚠️ 未获取到爬取结果，请检查网络连接或关键词")
                return []
            
        except ImportError as e:
            self.log_message(f"❌ 导入爬虫模块失败: {str(e)}")
            logging.error(f"导入爬虫模块错误: {traceback.format_exc()}")
            return None
        except Exception as e:
            self.log_message(f"❌ 调用爬虫程序失败: {str(e)}")
            logging.error(f"爬虫调用错误: {traceback.format_exc()}")
            return None
    
    def generate_output(self, keyword, results, output_format, output_dir, website_info):
        """生成输出文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crawler_results_{keyword}_{timestamp}"
        
        try:
            if output_format == 'excel':
                self.generate_excel_output(output_dir, filename, results, website_info)
            elif output_format == 'csv':
                self.generate_csv_output(output_dir, filename, results, website_info)
            elif output_format == 'json':
                self.generate_json_output(output_dir, filename, results, website_info)
                
            self.log_message(f"💾 结果已保存到: {os.path.join(output_dir, filename)}")
            
        except Exception as e:
            self.log_message(f"❌ 生成输出文件失败: {e}")
    
    def generate_excel_output(self, output_dir, filename, results, website_info):
        """生成Excel输出"""
        try:
            # 动态导入pandas，避免全局导入错误
            import pandas as pd
            
            # 处理真实的爬虫结果
            titles = []
            links = []
            abstracts = []
            sources = []
            timestamps = []
            
            for result in results:
                titles.append(result.get('title', '无标题'))
                links.append(result.get('link', '无链接'))
                abstracts.append(result.get('abstract', '无摘要'))
                sources.append(website_info['name'])
                timestamps.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            # 创建DataFrame
            data = {
                '标题': titles,
                '链接': links,
                '摘要': abstracts,
                '来源': sources,
                '爬取时间': timestamps
            }
            
            df = pd.DataFrame(data)
            output_path = os.path.join(output_dir, f"{filename}.xlsx")
            df.to_excel(output_path, index=False, engine='openpyxl')
            
            logging.info(f"Excel文件已保存: {output_path}")
            
        except ImportError as e:
            self.log_message(f"⚠️ 无法生成Excel文件: {e}")
            logging.error(f"Excel生成失败: {e}")
            raise
        except Exception as e:
            self.log_message(f"⚠️ Excel文件生成错误: {e}")
            logging.error(f"Excel生成异常: {traceback.format_exc()}")
            raise
    
    def generate_csv_output(self, output_dir, filename, results, website_info):
        """生成CSV输出"""
        try:
            # 动态导入pandas，避免全局导入错误
            import pandas as pd
            
            # 处理真实的爬虫结果
            titles = []
            links = []
            abstracts = []
            sources = []
            timestamps = []
            
            for result in results:
                titles.append(result.get('title', '无标题'))
                links.append(result.get('link', '无链接'))
                abstracts.append(result.get('abstract', '无摘要'))
                sources.append(website_info['name'])
                timestamps.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            # 创建DataFrame
            data = {
                '标题': titles,
                '链接': links,
                '摘要': abstracts,
                '来源': sources,
                '爬取时间': timestamps
            }
            
            df = pd.DataFrame(data)
            output_path = os.path.join(output_dir, f"{filename}.csv")
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            logging.info(f"CSV文件已保存: {output_path}")
            
        except ImportError as e:
            self.log_message(f"⚠️ 无法生成CSV文件: {e}")
            logging.error(f"CSV生成失败: {e}")
            raise
        except Exception as e:
            self.log_message(f"⚠️ CSV文件生成错误: {e}")
            logging.error(f"CSV生成异常: {traceback.format_exc()}")
            raise
    
    def generate_json_output(self, output_dir, filename, results, website_info):
        """生成JSON输出"""
        try:
            # 处理真实的爬虫结果
            search_results = []
            
            for result in results:
                search_results.append({
                    '标题': result.get('title', '无标题'),
                    '链接': result.get('link', '无链接'),
                    '摘要': result.get('abstract', '无摘要'),
                    '来源': website_info['name']
                })
            
            # 创建完整数据结构
            data = {
                '爬取信息': {
                    '关键词': self.keyword_entry.get().strip(),
                    '目标网站': website_info['name'],
                    '网站地址': website_info['url'],
                    '爬取页数': len(results) // 10 if len(results) > 0 else 0,  # 估算页数
                    '总结果数': len(results),
                    '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                '爬取结果': search_results
            }
            
            output_path = os.path.join(output_dir, f"{filename}.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            logging.info(f"JSON文件已保存: {output_path}")
            
        except Exception as e:
            self.log_message(f"⚠️ JSON文件生成错误: {e}")
            logging.error(f"JSON生成异常: {traceback.format_exc()}")
            raise
    
    def stop_crawling(self):
        """停止爬取"""
        if self.is_running:
            self.is_running = False
            self.should_stop = True
            try:
                if self.status_var:
                    self.status_var.set("正在停止...")
            except Exception:
                pass
            self.log_message("⏹️ 用户请求停止爬取...")
            logging.info("用户停止爬取任务")
    
    def reset_ui(self):
        """重置UI状态"""
        try:
            if self.start_btn and self.start_btn.winfo_exists():
                self.start_btn.config(state='normal')
            if self.stop_btn and self.stop_btn.winfo_exists():
                self.stop_btn.config(state='disabled')
            if self.progress_var:
                self.progress_var.set(0)
        except Exception as e:
            logging.error(f"重置UI出错: {e}")
    
    def clear_log(self):
        """清空日志"""
        try:
            if self.log_text and self.log_text.winfo_exists():
                self.log_text.delete('1.0', 'end')
                self.log_message("🗑️ 日志已清空")
        except Exception as e:
            logging.error(f"清空日志出错: {e}")
    
    def open_output_dir(self):
        """打开输出目录"""
        try:
            if self.output_dir_var and hasattr(self.output_dir_var, 'get'):
                output_dir = self.output_dir_var.get()
                if os.path.exists(output_dir):
                    try:
                        if sys.platform == 'win32':
                            os.startfile(output_dir)
                        elif sys.platform == 'darwin':  # macOS
                            subprocess.run(['open', output_dir])
                        else:  # Linux
                            subprocess.run(['xdg-open', output_dir])
                        self.log_message(f"📂 已打开输出目录: {output_dir}")
                    except Exception as e:
                        messagebox.showerror("错误", f"无法打开目录: {e}")
                        logging.error(f"打开目录错误: {e}")
                else:
                    messagebox.showwarning("警告", "输出目录不存在")
            else:
                messagebox.showerror("错误", "无法获取输出目录路径")
        except Exception as e:
            messagebox.showerror("错误", f"打开输出目录时出错: {e}")
            logging.error(f"打开输出目录错误: {traceback.format_exc()}")
    
    def show_help(self):
        """显示帮助"""
        help_text = """
📖 使用帮助:

🔍 爬取设置:
• 爬取关键词: 输入您要爬取的关键词
• 目标网站: 先选择网站分类，再选择具体网站
• 爬取页数: 设置要爬取的页数 (1-10页)

🌐 网站分类:
• 新闻媒体: 人民网、新华网、央视网、新浪新闻等
• 科技媒体: 36氪、虎嗅、钛媒体、IT之家等
• 财经媒体: 东方财富、新浪财经、腾讯财经等
• 国际媒体: 彭博、路透、CNBC、金融时报等

⚙️ 高级选项:
• 输出格式: 选择结果保存的格式
• 输出目录: 选择结果文件保存的位置

🚀 操作说明:
• 点击"开始爬取"开始任务
• 点击"停止爬取"可以随时停止
• 在日志区域查看爬取进度
• 完成后可以打开输出目录查看结果

💡 提示:
• 首次使用建议先运行依赖检查器
• 爬取过程中请勿关闭程序
• 结果文件会自动添加时间戳
• 支持新闻、科技、财经等各类网站
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("使用帮助")
        help_window.geometry("600x500")
        help_window.resizable(False, False)
        
        help_text_widget = scrolledtext.ScrolledText(help_window, wrap='word')
        help_text_widget.pack(fill='both', expand=True, padx=20, pady=20)
        help_text_widget.insert('1.0', help_text)
        help_text_widget.config(state='disabled')
        
        ttk.Button(help_window, text="关闭", 
                  command=help_window.destroy).pack(pady=10)
    
    def log_message(self, message):
        """添加日志消息"""
        # 记录到日志文件
        logging.info(message)
        
        # 添加到GUI日志
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # 确保在GUI线程中更新
        if self.root and not self.root.winfo_ismapped():
            # 如果窗口已关闭，只记录到文件
            return
            
        try:
            self.root.after(0, lambda: self._add_log_message(log_entry))
        except Exception:
            # 如果GUI已关闭，忽略错误
            pass
    
    def _add_log_message(self, log_entry):
        """在GUI线程中添加日志消息"""
        try:
            if self.log_text and self.log_text.winfo_exists():
                self.log_text.insert('end', log_entry)
                self.log_text.see('end')
        except Exception:
            # 如果GUI已关闭，忽略错误
            pass
    
    def run(self):
        """运行GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


def main():
    """主函数"""
    try:
        app = CrawlerGUI()
        app.run()
    except Exception as e:
        print(f"GUI启动失败: {e}")
        print("请尝试使用命令行版本: python smart_launcher.py")


if __name__ == "__main__":
    main()
