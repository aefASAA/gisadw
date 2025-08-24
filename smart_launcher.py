#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能启动器
集成依赖检查、程序选择和错误处理
"""

import os
import sys
import subprocess
import time
from typing import Optional

class SmartLauncher:
    """智能启动器类"""
    
    def __init__(self):
        """初始化启动器"""
        self.programs = {
            '1': {
                'name': '简化版爬虫',
                'file': 'simple_crawler.py',
                'description': '适合新手，功能简单易用',
                'dependencies': ['requests', 'beautifulsoup4', 'pandas', 'openpyxl']
            },
            '2': {
                'name': '完整版爬虫',
                'file': 'web_crawler.py',
                'description': '功能完整，支持多种搜索引擎',
                'dependencies': ['requests', 'beautifulsoup4', 'pandas', 'openpyxl', 'selenium']
            },
            '3': {
                'name': '依赖检查器',
                'file': 'dependency_checker.py',
                'description': '检查并安装缺失的依赖包',
                'dependencies': []
            },
            '4': {
                'name': '使用示例',
                'file': 'example_usage.py',
                'description': '查看各种使用示例',
                'dependencies': ['requests', 'beautifulsoup4', 'pandas', 'openpyxl']
            },
            '5': {
                'name': '图形化启动器',
                'file': 'gui_launcher.py',
                'description': '图形化界面启动器',
                'dependencies': []
            },
            '6': {
                'name': '图形化爬虫',
                'file': 'gui_crawler.py',
                'description': '直接在GUI中执行爬虫任务',
                'dependencies': ['requests', 'beautifulsoup4', 'pandas', 'openpyxl']
            }
        }
        
        self.current_choice = None
    
    def print_banner(self):
        """打印程序横幅"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🕷️ 网络关键词爬虫程序 🕷️                    ║
║                                                              ║
║  功能强大 • 易于使用 • 智能检测 • 自动安装                    ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_menu(self):
        """打印主菜单"""
        print("\n📋 请选择要运行的程序:")
        print("-" * 60)
        
        for key, program in self.programs.items():
            status = "✅" if self.check_program_available(program) else "❌"
            print(f"{key}. {status} {program['name']}")
            print(f"   {program['description']}")
            print()
        
        print("0. 退出程序")
        print("-" * 60)
    
    def check_program_available(self, program: dict) -> bool:
        """检查程序是否可用"""
        # 检查文件是否存在
        if not os.path.exists(program['file']):
            return False
        
        # 检查依赖包
        if program['dependencies']:
            for dep in program['dependencies']:
                try:
                    __import__(dep)
                except ImportError:
                    return False
        
        return True
    
    def get_user_choice(self) -> Optional[str]:
        """获取用户选择"""
        while True:
            try:
                choice = input("请输入选择 (0-6): ").strip()
                
                if choice == '0':
                    return None
                
                if choice in self.programs:
                    return choice
                else:
                    print("❌ 无效选择，请输入 0-6 之间的数字")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  用户中断程序")
                return None
            except EOFError:
                return None
    
    def run_dependency_check(self) -> bool:
        """运行依赖检查"""
        print("\n🔍 正在运行依赖检查...")
        
        try:
            # 导入依赖检查器
            from dependency_checker import DependencyChecker
            
            checker = DependencyChecker()
            return checker.run_full_check()
            
        except ImportError:
            print("❌ 依赖检查器不可用，请先运行依赖检查")
            return False
        except Exception as e:
            print(f"❌ 依赖检查失败: {e}")
            return False
    
    def run_program(self, choice: str) -> bool:
        """运行选中的程序"""
        program = self.programs[choice]
        
        print(f"\n🚀 正在启动: {program['name']}")
        print(f"📁 文件: {program['file']}")
        print(f"📝 描述: {program['description']}")
        
        # 检查程序是否可用
        if not self.check_program_available(program):
            print(f"❌ {program['name']} 不可用")
            
            # 检查是否是依赖问题
            missing_deps = []
            for dep in program['dependencies']:
                try:
                    __import__(dep)
                except ImportError:
                    missing_deps.append(dep)
            
            if missing_deps:
                print(f"❌ 缺少依赖包: {', '.join(missing_deps)}")
                choice = input("是否运行依赖检查器? (y/n): ").strip().lower()
                if choice == 'y':
                    return self.run_dependency_check()
            
            return False
        
        # 运行程序
        try:
            print(f"\n✅ 启动成功！正在运行 {program['name']}...")
            print("=" * 60)
            
            # 使用subprocess运行程序
            result = subprocess.run([sys.executable, program['file']], 
                                  cwd=os.getcwd())
            
            print("=" * 60)
            if result.returncode == 0:
                print(f"✅ {program['name']} 运行完成")
            else:
                print(f"⚠️  {program['name']} 运行异常 (退出码: {result.returncode})")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ 找不到文件: {program['file']}")
            return False
        except Exception as e:
            print(f"❌ 运行程序失败: {e}")
            return False
    
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
        """
        print(help_text)
    
    def show_status(self):
        """显示系统状态"""
        print("\n📊 系统状态:")
        print("-" * 40)
        
        # Python版本
        version = sys.version_info
        print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
        
        # 当前目录
        print(f"当前目录: {os.getcwd()}")
        
        # 程序文件状态
        print("\n📁 程序文件状态:")
        for key, program in self.programs.items():
            status = "✅" if os.path.exists(program['file']) else "❌"
            print(f"  {status} {program['file']}")
        
        # 依赖包状态
        print("\n📦 依赖包状态:")
        all_deps = set()
        for program in self.programs.values():
            all_deps.update(program['dependencies'])
        
        for dep in sorted(all_deps):
            try:
                __import__(dep)
                print(f"  ✅ {dep}")
            except ImportError:
                print(f"  ❌ {dep}")
    
    def run(self):
        """运行启动器"""
        self.print_banner()
        
        while True:
            try:
                self.print_menu()
                choice = self.get_user_choice()
                
                if choice is None:
                    print("\n👋 感谢使用，再见！")
                    break
                
                if choice == '3':
                    # 运行依赖检查器
                    self.run_dependency_check()
                elif choice == '5':
                    # 显示帮助
                    self.show_help()
                elif choice == '6':
                    # 显示状态
                    self.show_status()
                else:
                    # 运行选中的程序
                    self.run_program(choice)
                
                # 询问是否继续
                if choice in ['1', '2', '4']:
                    print("\n" + "=" * 60)
                    continue_choice = input("是否返回主菜单? (y/n): ").strip().lower()
                    if continue_choice != 'y':
                        print("\n👋 感谢使用，再见！")
                        break
                
            except KeyboardInterrupt:
                print("\n\n⚠️  用户中断程序")
                break
            except Exception as e:
                print(f"\n❌ 启动器运行出错: {e}")
                input("按回车键继续...")
    
    def quick_start(self, program_name: str) -> bool:
        """快速启动指定程序"""
        # 查找程序
        target_program = None
        for key, program in self.programs.items():
            if program['name'] == program_name or program['file'] == program_name:
                target_program = program
                break
        
        if not target_program:
            print(f"❌ 找不到程序: {program_name}")
            return False
        
        # 运行程序
        return self.run_program(list(self.programs.keys())[
            list(self.programs.values()).index(target_program)
        ])


def main():
    """主函数"""
    launcher = SmartLauncher()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        program_name = sys.argv[1]
        print(f"🚀 快速启动: {program_name}")
        launcher.quick_start(program_name)
    else:
        # 交互式启动
        launcher.run()


if __name__ == "__main__":
    main()
