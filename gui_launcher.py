#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图形化启动器
提供友好的GUI界面来启动各种爬虫程序
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import sys
import os
import threading
import importlib
from typing import Dict, List

class CrawlerGUI:
    """爬虫程序图形化界面"""
    
    def __init__(self):
        """初始化GUI"""
        self.root = tk.Tk()
        self.root.title("🕷️ 网络关键词爬虫程序")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置图标和样式
        self.setup_styles()
        
        # 程序配置
        self.programs = {
            'simple_crawler': {
                'name': '简化版爬虫',
                'file': 'simple_crawler.py',
                'description': '适合新手，功能简单易用',
                'dependencies': ['requests', 'beautifulsoup4', 'pandas', 'openpyxl'],
                'icon': '🕷️'
            },
            'web_crawler': {
                'name': '完整版爬虫',
                'file': 'web_crawler.py',
                'description': '功能完整，支持多种搜索引擎',
                'dependencies': ['requests', 'beautifulsoup4', 'pandas', 'openpyxl', 'selenium'],
                'icon': '🕸️'
            },
            'dependency_checker': {
                'name': '依赖检查器',
                'file': 'dependency_checker.py',
                'description': '检查并安装缺失的依赖包',
                'dependencies': [],
                'icon': '🔍'
            },
            'example_usage': {
                'name': '使用示例',
                'file': 'example_usage.py',
                'description': '查看各种使用场景的示例代码',
                'dependencies': ['requests', 'beautifulsoup4', 'pandas', 'openpyxl'],
                'icon': '📚'
            }
        }
        
        self.current_process = None
        self.setup_ui()
        
    def setup_styles(self):
        """设置界面样式"""
        # 配置ttk样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义样式
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10))
        
    def setup_ui(self):
        """设置用户界面"""
        # 主标题
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = ttk.Label(title_frame, 
                               text="🕷️ 网络关键词爬虫程序", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="功能强大 • 易于使用 • 智能检测 • 自动安装",
                                  style='Status.TLabel')
        subtitle_label.pack()
        
        # 程序选择区域
        self.create_program_buttons()
        
        # 状态显示区域
        self.create_status_area()
        
        # 控制按钮区域
        self.create_control_buttons()
        
        # 日志显示区域
        self.create_log_area()
        
    def create_program_buttons(self):
        """创建程序选择按钮"""
        button_frame = ttk.LabelFrame(self.root, text="📋 选择要运行的程序", padding=20)
        button_frame.pack(fill='x', padx=20, pady=10)
        
        # 创建按钮网格
        for i, (key, program) in enumerate(self.programs.items()):
            row = i // 2
            col = i % 2
            
            # 程序按钮框架
            prog_frame = ttk.Frame(button_frame)
            prog_frame.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
            
            # 程序图标和名称
            header_frame = ttk.Frame(prog_frame)
            header_frame.pack(fill='x')
            
            icon_label = ttk.Label(header_frame, text=program['icon'], font=('Arial', 16))
            icon_label.pack(side='left', padx=(0, 5))
            
            name_label = ttk.Label(header_frame, text=program['name'], style='Header.TLabel')
            name_label.pack(side='left')
            
            # 程序描述
            desc_label = ttk.Label(prog_frame, text=program['description'], 
                                  wraplength=300, justify='left')
            desc_label.pack(anchor='w', pady=(5, 10))
            
            # 运行按钮
            run_btn = ttk.Button(prog_frame, 
                                text="🚀 运行程序",
                                command=lambda p=key: self.run_program(p))
            run_btn.pack(side='left', padx=(0, 10))
            
            # 检查依赖按钮
            check_btn = ttk.Button(prog_frame, 
                                  text="🔍 检查依赖",
                                  command=lambda p=key: self.check_dependencies(p))
            check_btn.pack(side='left')
            
        # 配置网格权重
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
    def create_status_area(self):
        """创建状态显示区域"""
        status_frame = ttk.LabelFrame(self.root, text="📊 系统状态", padding=15)
        status_frame.pack(fill='x', padx=20, pady=10)
        
        # Python版本
        python_version = f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        ttk.Label(status_frame, text=f"🐍 {python_version}").pack(anchor='w')
        
        # 当前目录
        current_dir = os.getcwd()
        ttk.Label(status_frame, text=f"📁 当前目录: {current_dir}").pack(anchor='w')
        
        # 依赖包状态
        self.dependency_status = ttk.Label(status_frame, text="🔍 正在检查依赖包状态...")
        self.dependency_status.pack(anchor='w', pady=(10, 0))
        
        # 更新依赖状态
        self.update_dependency_status()
        
    def create_control_buttons(self):
        """创建控制按钮"""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # 左侧按钮
        left_frame = ttk.Frame(control_frame)
        left_frame.pack(side='left')
        
        ttk.Button(left_frame, text="🔄 刷新状态", 
                  command=self.refresh_status).pack(side='left', padx=(0, 10))
        
        ttk.Button(left_frame, text="📦 一键安装", 
                  command=self.auto_install).pack(side='left', padx=(0, 10))
        
        # 右侧按钮
        right_frame = ttk.Frame(control_frame)
        right_frame.pack(side='right')
        
        ttk.Button(right_frame, text="❌ 停止程序", 
                  command=self.stop_program).pack(side='right', padx=(10, 0))
        
        ttk.Button(right_frame, text="❓ 帮助", 
                  command=self.show_help).pack(side='right')
        
    def create_log_area(self):
        """创建日志显示区域"""
        log_frame = ttk.LabelFrame(self.root, text="📝 运行日志", padding=15)
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap='word')
        self.log_text.pack(fill='both', expand=True)
        
        # 清空日志按钮
        clear_btn = ttk.Button(log_frame, text="🗑️ 清空日志", 
                              command=self.clear_log)
        clear_btn.pack(anchor='e', pady=(10, 0))
        
    def update_dependency_status(self):
        """更新依赖包状态"""
        try:
            missing_deps = []
            total_deps = 0
            
            for program in self.programs.values():
                for dep in program['dependencies']:
                    total_deps += 1
                    try:
                        importlib.import_module(dep)
                    except ImportError:
                        missing_deps.append(dep)
            
            if missing_deps:
                status_text = f"⚠️  依赖包状态: {total_deps - len(missing_deps)}/{total_deps} ✅ (缺失: {', '.join(set(missing_deps))})"
                self.dependency_status.config(text=status_text)
            else:
                status_text = f"✅ 依赖包状态: {total_deps}/{total_deps} ✅ (全部已安装)"
                self.dependency_status.config(text=status_text)
                
        except Exception as e:
            self.dependency_status.config(text=f"❌ 依赖检查失败: {e}")
    
    def run_program(self, program_key: str):
        """运行指定程序"""
        program = self.programs[program_key]
        
        # 检查文件是否存在
        if not os.path.exists(program['file']):
            messagebox.showerror("错误", f"找不到程序文件: {program['file']}")
            return
        
        # 检查依赖
        missing_deps = []
        for dep in program['dependencies']:
            try:
                importlib.import_module(dep)
            except ImportError:
                missing_deps.append(dep)
        
        if missing_deps:
            result = messagebox.askyesno("依赖缺失", 
                                       f"程序 {program['name']} 缺少以下依赖包:\n{', '.join(missing_deps)}\n\n是否现在安装?")
            if result:
                self.install_dependencies(missing_deps)
            return
        
        # 在新线程中运行程序
        def run_in_thread():
            try:
                self.log_message(f"🚀 正在启动: {program['name']}")
                
                # 运行程序
                process = subprocess.Popen([sys.executable, program['file']],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         text=True,
                                         cwd=os.getcwd())
                
                self.current_process = process
                
                # 读取输出
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.log_message(output.strip())
                
                # 检查退出码
                return_code = process.poll()
                if return_code == 0:
                    self.log_message(f"✅ {program['name']} 运行完成")
                else:
                    self.log_message(f"⚠️  {program['name']} 运行异常 (退出码: {return_code})")
                
                self.current_process = None
                
            except Exception as e:
                self.log_message(f"❌ 运行程序失败: {e}")
                self.current_process = None
        
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
    
    def check_dependencies(self, program_key: str):
        """检查指定程序的依赖"""
        program = self.programs[program_key]
        
        missing_deps = []
        for dep in program['dependencies']:
            try:
                importlib.import_module(dep)
            except ImportError:
                missing_deps.append(dep)
        
        if missing_deps:
            messagebox.showinfo("依赖检查", 
                              f"程序 {program['name']} 缺少以下依赖包:\n{', '.join(missing_deps)}")
        else:
            messagebox.showinfo("依赖检查", 
                              f"程序 {program['name']} 的所有依赖包都已安装 ✅")
    
    def install_dependencies(self, packages: List[str]):
        """安装依赖包"""
        def install_in_thread():
            try:
                self.log_message(f"📦 正在安装依赖包: {', '.join(packages)}")
                
                for package in packages:
                    self.log_message(f"正在安装: {package}")
                    
                    result = subprocess.run([sys.executable, '-m', 'pip', 'install', package],
                                          capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0:
                        self.log_message(f"✅ {package} 安装成功")
                    else:
                        self.log_message(f"❌ {package} 安装失败")
                        self.log_message(f"错误信息: {result.stderr}")
                
                # 更新状态
                self.root.after(0, self.update_dependency_status)
                
            except Exception as e:
                self.log_message(f"❌ 安装依赖失败: {e}")
        
        thread = threading.Thread(target=install_in_thread, daemon=True)
        thread.start()
    
    def auto_install(self):
        """一键安装所有依赖"""
        all_deps = set()
        for program in self.programs.values():
            all_deps.update(program['dependencies'])
        
        if all_deps:
            self.install_dependencies(list(all_deps))
        else:
            messagebox.showinfo("提示", "没有需要安装的依赖包")
    
    def stop_program(self):
        """停止当前运行的程序"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.log_message("⏹️  程序已停止")
                self.current_process = None
            except Exception as e:
                self.log_message(f"❌ 停止程序失败: {e}")
        else:
            messagebox.showinfo("提示", "当前没有运行的程序")
    
    def refresh_status(self):
        """刷新系统状态"""
        self.update_dependency_status()
        self.log_message("🔄 状态已刷新")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
📖 使用帮助:

1. 简化版爬虫: 适合新手用户，功能简单，依赖较少
2. 完整版爬虫: 功能完整，支持多种搜索引擎，需要更多依赖
3. 依赖检查器: 自动检测并安装缺失的Python包
4. 使用示例: 查看各种使用场景的示例代码

💡 提示:
- 首次使用建议先运行"依赖检查器"
- 如果程序无法运行，通常是依赖包缺失
- 简化版爬虫依赖较少，更容易成功运行
- 可以在日志区域查看程序运行状态
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("使用帮助")
        help_window.geometry("500x400")
        help_window.resizable(False, False)
        
        help_text_widget = scrolledtext.ScrolledText(help_window, wrap='word')
        help_text_widget.pack(fill='both', expand=True, padx=20, pady=20)
        help_text_widget.insert('1.0', help_text)
        help_text_widget.config(state='disabled')
        
        ttk.Button(help_window, text="关闭", 
                  command=help_window.destroy).pack(pady=10)
    
    def log_message(self, message: str):
        """添加日志消息"""
        self.root.after(0, lambda: self._add_log_message(message))
    
    def _add_log_message(self, message: str):
        """在GUI线程中添加日志消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert('end', log_entry)
        self.log_text.see('end')
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete('1.0', 'end')
    
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
