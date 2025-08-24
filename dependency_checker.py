#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖包检测和自动安装脚本
自动检测并安装爬虫程序所需的依赖包
"""

import subprocess
import sys
import os
import importlib
from typing import Dict, List, Tuple

class DependencyChecker:
    """依赖包检测和安装管理类"""
    
    def __init__(self):
        """初始化依赖检查器"""
        self.required_packages = {
            'requests': 'requests==2.31.0',
            'beautifulsoup4': 'beautifulsoup4==4.12.2',
            'pandas': 'pandas==2.1.1',
            'openpyxl': 'openpyxl==3.1.2'
        }
        
        self.optional_packages = {
            'fake-useragent': 'fake-useragent==1.4.0',
            'selenium': 'selenium==4.15.2',
            'webdriver-manager': 'webdriver-manager==4.0.1',
            'tqdm': 'tqdm==4.66.1',
            'colorama': 'colorama==0.4.6'
        }
        
        self.missing_required = []
        self.missing_optional = []
        self.installed_packages = {}
    
    def check_python_version(self) -> bool:
        """检查Python版本"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print(f"❌ Python版本过低: {version.major}.{version.minor}")
            print("   需要Python 3.7或更高版本")
            return False
        
        print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
        return True
    
    def check_pip(self) -> bool:
        """检查pip是否可用"""
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
    
    def check_package(self, package_name: str) -> bool:
        """检查单个包是否已安装"""
        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            return False
    
    def check_all_packages(self) -> Dict[str, List[str]]:
        """检查所有依赖包"""
        print("\n🔍 正在检查依赖包...")
        
        # 检查必需包
        for package, version in self.required_packages.items():
            if self.check_package(package):
                print(f"✅ {package} - 已安装")
                self.installed_packages[package] = True
            else:
                print(f"❌ {package} - 未安装")
                self.missing_required.append(version)
                self.installed_packages[package] = False
        
        # 检查可选包
        for package, version in self.optional_packages.items():
            if self.check_package(package):
                print(f"✅ {package} - 已安装")
                self.installed_packages[package] = True
            else:
                print(f"⚠️  {package} - 未安装 (可选)")
                self.missing_optional.append(version)
                self.installed_packages[package] = False
        
        return {
            'required': self.missing_required,
            'optional': self.missing_optional
        }
    
    def install_packages(self, packages: List[str], package_type: str = "必需") -> bool:
        """安装指定的包列表"""
        if not packages:
            print(f"✅ 所有{package_type}包都已安装")
            return True
        
        print(f"\n📦 正在安装{package_type}包...")
        
        for package in packages:
            try:
                print(f"正在安装: {package}")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package, '--quiet'
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print(f"✅ {package} 安装成功")
                else:
                    print(f"❌ {package} 安装失败")
                    print(f"错误信息: {result.stderr}")
                    return False
                    
            except subprocess.TimeoutExpired:
                print(f"❌ {package} 安装超时")
                return False
            except Exception as e:
                print(f"❌ {package} 安装异常: {e}")
                return False
        
        return True
    
    def upgrade_pip(self) -> bool:
        """升级pip到最新版本"""
        try:
            print("🔄 正在升级pip...")
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
    
    def auto_fix_dependencies(self) -> bool:
        """自动修复依赖问题"""
        print("\n🔧 开始自动修复依赖...")
        
        # 升级pip
        self.upgrade_pip()
        
        # 安装必需包
        if self.missing_required:
            if not self.install_packages(self.missing_required, "必需"):
                print("❌ 必需包安装失败，程序无法运行")
                return False
        
        # 安装可选包
        if self.missing_optional:
            print("\n💡 可选包安装失败不会影响基本功能")
            self.install_packages(self.missing_optional, "可选")
        
        return True
    
    def get_installation_summary(self) -> str:
        """获取安装摘要"""
        total_required = len(self.required_packages)
        total_optional = len(self.optional_packages)
        installed_required = sum(1 for pkg in self.required_packages.keys() 
                               if self.installed_packages.get(pkg, False))
        installed_optional = sum(1 for pkg in self.optional_packages.keys() 
                               if self.installed_packages.get(pkg, False))
        
        summary = f"""
📊 依赖包安装摘要:
   必需包: {installed_required}/{total_required} ✅
   可选包: {installed_optional}/{total_optional} ⚠️
        """
        
        if installed_required == total_required:
            summary += "\n🎉 所有必需包已安装，程序可以正常运行！"
        else:
            summary += f"\n❌ 缺少 {total_required - installed_required} 个必需包"
        
        return summary
    
    def run_full_check(self) -> bool:
        """运行完整的依赖检查"""
        print("=" * 60)
        print("🔍 网络爬虫程序依赖检查")
        print("=" * 60)
        
        # 检查Python版本
        if not self.check_python_version():
            return False
        
        # 检查pip
        if not self.check_pip():
            return False
        
        # 检查所有包
        missing = self.check_all_packages()
        
        # 显示摘要
        print(self.get_installation_summary())
        
        # 如果有缺失的包，询问是否自动安装
        if missing['required'] or missing['optional']:
            print("\n💡 检测到缺失的依赖包")
            
            if missing['required']:
                print("⚠️  必需包缺失，程序无法运行")
                choice = input("是否自动安装缺失的包? (y/n): ").strip().lower()
                if choice == 'y':
                    return self.auto_fix_dependencies()
                else:
                    print("❌ 用户取消安装，程序无法运行")
                    return False
            else:
                print("💡 只有可选包缺失，基本功能不受影响")
                choice = input("是否安装可选包? (y/n): ").strip().lower()
                if choice == 'y':
                    self.install_packages(missing['optional'], "可选")
        
        return True


def main():
    """主函数"""
    checker = DependencyChecker()
    
    try:
        if checker.run_full_check():
            print("\n✅ 依赖检查完成，程序可以运行！")
            return True
        else:
            print("\n❌ 依赖检查失败，请手动安装缺失的包")
            return False
            
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断检查")
        return False
    except Exception as e:
        print(f"\n❌ 依赖检查出错: {e}")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        input("\n按回车键退出...")
        sys.exit(1)
