#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键安装脚本
自动安装所有依赖包并配置环境
"""

import subprocess
import sys
import os
import platform
from typing import List, Dict

class AutoInstaller:
    """自动安装器类"""
    
    def __init__(self):
        """初始化安装器"""
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.install_log = []
        
        # 基础依赖包
        self.basic_packages = [
            'requests==2.31.0',
            'beautifulsoup4==4.12.2',
            'pandas==2.1.1',
            'openpyxl==3.1.2'
        ]
        
        # 增强功能包
        self.enhanced_packages = [
            'fake-useragent==1.4.0',
            'selenium==4.15.2',
            'webdriver-manager==4.0.1',
            'tqdm==4.66.1',
            'colorama==0.4.6'
        ]
        
        # 开发工具包
        self.dev_packages = [
            'pytest',
            'black',
            'flake8',
            'mypy'
        ]
    
    def print_banner(self):
        """打印安装横幅"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 网络爬虫一键安装器 🚀                    ║
║                                                              ║
║  自动检测 • 智能安装 • 环境配置 • 一键部署                    ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_python_version(self) -> bool:
        """检查Python版本"""
        print("🔍 检查Python版本...")
        
        if self.python_version.major < 3 or (self.python_version.major == 3 and self.python_version.minor < 7):
            print(f"❌ Python版本过低: {self.python_version.major}.{self.python_version.minor}")
            print("   需要Python 3.7或更高版本")
            return False
        
        print(f"✅ Python版本检查通过: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        return True
    
    def check_pip(self) -> bool:
        """检查pip是否可用"""
        print("🔍 检查pip...")
        
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ pip检查通过")
                return True
            else:
                print("❌ pip不可用")
                return False
        except Exception as e:
            print(f"❌ pip检查失败: {e}")
            return False
    
    def upgrade_pip(self) -> bool:
        """升级pip"""
        print("🔄 升级pip...")
        
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', '--quiet'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ pip升级成功")
                return True
            else:
                print("⚠️  pip升级失败，继续使用当前版本")
                return False
                
        except Exception as e:
            print(f"⚠️  pip升级失败: {e}")
            return False
    
    def install_packages(self, packages: List[str], package_type: str = "基础") -> bool:
        """安装包列表"""
        if not packages:
            print(f"✅ 所有{package_type}包都已安装")
            return True
        
        print(f"\n📦 正在安装{package_type}包...")
        
        success_count = 0
        total_count = len(packages)
        
        for package in packages:
            try:
                print(f"正在安装: {package}")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package, '--quiet'
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print(f"✅ {package} 安装成功")
                    success_count += 1
                    self.install_log.append(f"✅ {package}")
                else:
                    print(f"❌ {package} 安装失败")
                    self.install_log.append(f"❌ {package}")
                    
            except subprocess.TimeoutExpired:
                print(f"❌ {package} 安装超时")
                self.install_log.append(f"⏰ {package} (超时)")
            except Exception as e:
                print(f"❌ {package} 安装异常: {e}")
                self.install_log.append(f"❌ {package} (异常: {e})")
        
        print(f"\n📊 {package_type}包安装完成: {success_count}/{total_count}")
        return success_count == total_count
    
    def install_system_dependencies(self) -> bool:
        """安装系统级依赖"""
        print("\n🔧 检查系统依赖...")
        
        if self.system == "linux":
            return self.install_linux_dependencies()
        elif self.system == "darwin":  # macOS
            return self.install_macos_dependencies()
        elif self.system == "windows":
            return self.install_windows_dependencies()
        else:
            print(f"⚠️  不支持的操作系统: {self.system}")
            return True
    
    def install_linux_dependencies(self) -> bool:
        """安装Linux系统依赖"""
        print("🐧 检测到Linux系统")
        
        # 检查包管理器
        if os.path.exists("/usr/bin/apt-get"):
            print("📦 使用apt-get安装系统依赖...")
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "python3-dev", "build-essential"], check=True)
                print("✅ Linux系统依赖安装成功")
                return True
            except subprocess.CalledProcessError:
                print("⚠️  Linux系统依赖安装失败，继续安装Python包")
                return True
        
        elif os.path.exists("/usr/bin/yum"):
            print("📦 使用yum安装系统依赖...")
            try:
                subprocess.run(["sudo", "yum", "install", "-y", "python3-devel", "gcc"], check=True)
                print("✅ Linux系统依赖安装成功")
                return True
            except subprocess.CalledProcessError:
                print("⚠️  Linux系统依赖安装失败，继续安装Python包")
                return True
        
        return True
    
    def install_macos_dependencies(self) -> bool:
        """安装macOS系统依赖"""
        print("🍎 检测到macOS系统")
        
        # 检查Homebrew
        if os.path.exists("/usr/local/bin/brew") or os.path.exists("/opt/homebrew/bin/brew"):
            print("🍺 使用Homebrew安装系统依赖...")
            try:
                subprocess.run(["brew", "install", "openssl", "readline"], check=True)
                print("✅ macOS系统依赖安装成功")
                return True
            except subprocess.CalledProcessError:
                print("⚠️  macOS系统依赖安装失败，继续安装Python包")
                return True
        
        return True
    
    def install_windows_dependencies(self) -> bool:
        """安装Windows系统依赖"""
        print("🪟 检测到Windows系统")
        print("💡 Windows系统通常不需要额外依赖")
        return True
    
    def create_requirements_file(self):
        """创建requirements.txt文件"""
        print("\n📝 创建requirements.txt文件...")
        
        try:
            with open('requirements.txt', 'w', encoding='utf-8') as f:
                f.write("# 网络爬虫程序依赖包\n")
                f.write("# 自动生成于安装过程\n\n")
                
                f.write("# 基础依赖包\n")
                for package in self.basic_packages:
                    f.write(f"{package}\n")
                
                f.write("\n# 增强功能包\n")
                for package in self.enhanced_packages:
                    f.write(f"{package}\n")
                
                f.write("\n# 开发工具包 (可选)\n")
                for package in self.dev_packages:
                    f.write(f"# {package}\n")
            
            print("✅ requirements.txt文件创建成功")
            
        except Exception as e:
            print(f"⚠️  创建requirements.txt失败: {e}")
    
    def test_installation(self) -> bool:
        """测试安装是否成功"""
        print("\n🧪 测试安装...")
        
        test_packages = ['requests', 'bs4', 'pandas']
        success_count = 0
        
        for package in test_packages:
            try:
                if package == 'bs4':
                    __import__('bs4')
                else:
                    __import__(package)
                print(f"✅ {package} 导入成功")
                success_count += 1
            except ImportError:
                print(f"❌ {package} 导入失败")
        
        return success_count == len(test_packages)
    
    def show_installation_summary(self):
        """显示安装摘要"""
        print("\n" + "=" * 60)
        print("📊 安装摘要")
        print("=" * 60)
        
        print(f"操作系统: {platform.system()} {platform.release()}")
        print(f"Python版本: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print(f"安装日志: {len(self.install_log)} 条记录")
        
        print("\n📋 安装详情:")
        for log in self.install_log:
            print(f"  {log}")
        
        print("\n🎯 下一步操作:")
        print("  1. 运行依赖检查器: python dependency_checker.py")
        print("  2. 启动智能启动器: python smart_launcher.py")
        print("  3. 运行简化版爬虫: python simple_crawler.py")
    
    def run_installation(self) -> bool:
        """运行完整安装流程"""
        print("🚀 开始自动安装...")
        
        # 检查Python版本
        if not self.check_python_version():
            return False
        
        # 检查pip
        if not self.check_pip():
            return False
        
        # 升级pip
        self.upgrade_pip()
        
        # 安装系统依赖
        self.install_system_dependencies()
        
        # 安装基础包
        basic_success = self.install_packages(self.basic_packages, "基础")
        
        # 安装增强包
        enhanced_success = self.install_packages(self.enhanced_packages, "增强功能")
        
        # 创建requirements.txt
        self.create_requirements_file()
        
        # 测试安装
        test_success = self.test_installation()
        
        # 显示摘要
        self.show_installation_summary()
        
        return basic_success and test_success


def main():
    """主函数"""
    installer = AutoInstaller()
    
    try:
        installer.print_banner()
        
        if installer.run_installation():
            print("\n🎉 安装完成！程序可以正常运行了！")
        else:
            print("\n⚠️  安装过程中遇到一些问题，请检查错误信息")
            print("💡 建议运行依赖检查器: python dependency_checker.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断安装")
    except Exception as e:
        print(f"\n❌ 安装过程出错: {e}")
    
    print("\n按回车键退出...")
    input()


if __name__ == "__main__":
    main()
