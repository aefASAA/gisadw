#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络关键词爬虫程序
支持多种搜索引擎，可自定义关键词和搜索参数
"""

import requests
import time
import random
import json
import re
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from tqdm import tqdm
import colorama
from colorama import Fore, Style
import os
from datetime import datetime

# 初始化colorama
colorama.init(autoreset=True)

class WebCrawler:
    """网络爬虫主类"""
    
    def __init__(self, use_selenium=False, headless=True):
        """
        初始化爬虫
        
        Args:
            use_selenium (bool): 是否使用Selenium（用于动态页面）
            headless (bool): 是否使用无头模式
        """
        self.use_selenium = use_selenium
        self.headless = headless
        self.driver = None
        self.session = requests.Session()
        self.ua = UserAgent()
        self.results = []
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        if self.use_selenium:
            self._setup_selenium()
    
    def _setup_selenium(self):
        """设置Selenium WebDriver"""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument(f'--user-agent={self.ua.random}')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print(f"{Fore.GREEN}✓ Selenium WebDriver 初始化成功{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Selenium 初始化失败: {e}{Style.RESET_ALL}")
            self.use_selenium = False
    
    def search_baidu(self, keyword, max_pages=3):
        """百度搜索"""
        print(f"{Fore.BLUE}正在搜索百度: {keyword}{Style.RESET_ALL}")
        results = []
        
        for page in range(max_pages):
            try:
                pn = page * 10
                url = f"https://www.baidu.com/s?wd={quote(keyword)}&pn={pn}"
                
                if self.use_selenium and self.driver:
                    self.driver.get(url)
                    time.sleep(random.uniform(2, 4))
                    
                    # 等待搜索结果加载
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "result"))
                    )
                    
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                else:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                
                # 解析搜索结果
                search_results = soup.find_all('div', class_='result')
                
                for result in search_results:
                    try:
                        title_elem = result.find('h3')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True)
                        link = title_elem.find('a')['href'] if title_elem.find('a') else ''
                        
                        # 获取摘要
                        abstract_elem = result.find('div', class_='c-abstract')
                        abstract = abstract_elem.get_text(strip=True) if abstract_elem else ''
                        
                        # 获取来源网站
                        source_elem = result.find('div', class_='c-abstract-source')
                        source = source_elem.get_text(strip=True) if source_elem else ''
                        
                        results.append({
                            'title': title,
                            'link': link,
                            'abstract': abstract,
                            'source': source,
                            'search_engine': '百度',
                            'keyword': keyword,
                            'page': page + 1
                        })
                        
                    except Exception as e:
                        continue
                
                print(f"{Fore.GREEN}第 {page + 1} 页完成，获取 {len(search_results)} 个结果{Style.RESET_ALL}")
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"{Fore.RED}百度搜索第 {page + 1} 页失败: {e}{Style.RESET_ALL}")
                continue
        
        return results
    
    def search_google(self, keyword, max_pages=3):
        """Google搜索（需要代理）"""
        print(f"{Fore.BLUE}正在搜索Google: {keyword}{Style.RESET_ALL}")
        results = []
        
        for page in range(max_pages):
            try:
                start = page * 10
                url = f"https://www.google.com/search?q={quote(keyword)}&start={start}"
                
                if self.use_selenium and self.driver:
                    self.driver.get(url)
                    time.sleep(random.uniform(2, 4))
                    
                    # 等待搜索结果加载
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "g"))
                    )
                    
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                else:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                
                # 解析搜索结果
                search_results = soup.find_all('div', class_='g')
                
                for result in search_results:
                    try:
                        title_elem = result.find('h3')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True)
                        link = title_elem.find('a')['href'] if title_elem.find('a') else ''
                        
                        # 获取摘要
                        abstract_elem = result.find('div', class_='VwiC3b')
                        abstract = abstract_elem.get_text(strip=True) if abstract_elem else ''
                        
                        # 获取来源网站
                        source_elem = result.find('cite')
                        source = source_elem.get_text(strip=True) if source_elem else ''
                        
                        results.append({
                            'title': title,
                            'link': link,
                            'abstract': abstract,
                            'source': source,
                            'search_engine': 'Google',
                            'keyword': keyword,
                            'page': page + 1
                        })
                        
                    except Exception as e:
                        continue
                
                print(f"{Fore.GREEN}第 {page + 1} 页完成，获取 {len(search_results)} 个结果{Style.RESET_ALL}")
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"{Fore.RED}Google搜索第 {page + 1} 页失败: {e}{Style.RESET_ALL}")
                continue
        
        return results
    
    def search_bing(self, keyword, max_pages=3):
        """必应搜索"""
        print(f"{Fore.BLUE}正在搜索必应: {keyword}{Style.RESET_ALL}")
        results = []
        
        for page in range(max_pages):
            try:
                first = page * 10
                url = f"https://www.bing.com/search?q={quote(keyword)}&first={first}"
                
                if self.use_selenium and self.driver:
                    self.driver.get(url)
                    time.sleep(random.uniform(2, 4))
                    
                    # 等待搜索结果加载
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "b_algo"))
                    )
                    
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                else:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                
                # 解析搜索结果
                search_results = soup.find_all('li', class_='b_algo')
                
                for result in search_results:
                    try:
                        title_elem = result.find('h3')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True)
                        link = title_elem.find('a')['href'] if title_elem.find('a') else ''
                        
                        # 获取摘要
                        abstract_elem = result.find('p')
                        abstract = abstract_elem.get_text(strip=True) if abstract_elem else ''
                        
                        # 获取来源网站
                        source_elem = result.find('cite')
                        source = source_elem.get_text(strip=True) if source_elem else ''
                        
                        results.append({
                            'title': title,
                            'link': link,
                            'abstract': abstract,
                            'source': source,
                            'search_engine': '必应',
                            'keyword': keyword,
                            'page': page + 1
                        })
                        
                    except Exception as e:
                        continue
                
                print(f"{Fore.GREEN}第 {page + 1} 页完成，获取 {len(search_results)} 个结果{Style.RESET_ALL}")
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"{Fore.RED}必应搜索第 {page + 1} 页失败: {e}{Style.RESET_ALL}")
                continue
        
        return results
    
    def search_sogou(self, keyword, max_pages=3):
        """搜狗搜索"""
        print(f"{Fore.BLUE}正在搜索搜狗: {keyword}{Style.RESET_ALL}")
        results = []
        
        for page in range(max_pages):
            try:
                page_num = page + 1
                url = f"https://www.sogou.com/web?query={quote(keyword)}&page={page_num}"
                
                if self.use_selenium and self.driver:
                    self.driver.get(url)
                    time.sleep(random.uniform(2, 4))
                    
                    # 等待搜索结果加载
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "vrwrap"))
                    )
                    
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                else:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                
                # 解析搜索结果
                search_results = soup.find_all('div', class_='vrwrap')
                
                for result in search_results:
                    try:
                        title_elem = result.find('h3')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True)
                        link = title_elem.find('a')['href'] if title_elem.find('a') else ''
                        
                        # 获取摘要
                        abstract_elem = result.find('p', class_='txt')
                        abstract = abstract_elem.get_text(strip=True) if abstract_elem else ''
                        
                        # 获取来源网站
                        source_elem = result.find('cite')
                        source = source_elem.get_text(strip=True) if source_elem else ''
                        
                        results.append({
                            'title': title,
                            'link': link,
                            'abstract': abstract,
                            'source': source,
                            'search_engine': '搜狗',
                            'keyword': keyword,
                            'page': page + 1
                        })
                        
                    except Exception as e:
                        continue
                
                print(f"{Fore.GREEN}第 {page + 1} 页完成，获取 {len(search_results)} 个结果{Style.RESET_ALL}")
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"{Fore.RED}搜狗搜索第 {page + 1} 页失败: {e}{Style.RESET_ALL}")
                continue
        
        return results
    
    def search_all_engines(self, keyword, max_pages=3, engines=None):
        """搜索所有指定的搜索引擎"""
        if engines is None:
            engines = ['baidu', 'bing', 'sogou']  # 默认搜索引擎
        
        all_results = []
        
        for engine in engines:
            try:
                if engine == 'baidu':
                    results = self.search_baidu(keyword, max_pages)
                elif engine == 'google':
                    results = self.search_google(keyword, max_pages)
                elif engine == 'bing':
                    results = self.search_bing(keyword, max_pages)
                elif engine == 'sogou':
                    results = self.search_sogou(keyword, max_pages)
                else:
                    print(f"{Fore.YELLOW}不支持的搜索引擎: {engine}{Style.RESET_ALL}")
                    continue
                
                all_results.extend(results)
                print(f"{Fore.GREEN}✓ {engine} 搜索完成，获取 {len(results)} 个结果{Style.RESET_ALL}")
                
            except Exception as e:
                print(f"{Fore.RED}✗ {engine} 搜索失败: {e}{Style.RESET_ALL}")
                continue
        
        return all_results
    
    def save_results(self, results, filename=None, format='excel'):
        """保存搜索结果"""
        if not results:
            print(f"{Fore.YELLOW}没有结果可保存{Style.RESET_ALL}")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_results_{timestamp}"
        
        try:
            df = pd.DataFrame(results)
            
            if format.lower() == 'excel':
                filepath = f"{filename}.xlsx"
                df.to_excel(filepath, index=False, engine='openpyxl')
                print(f"{Fore.GREEN}✓ 结果已保存到: {filepath}{Style.RESET_ALL}")
                
            elif format.lower() == 'csv':
                filepath = f"{filename}.csv"
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
                print(f"{Fore.GREEN}✓ 结果已保存到: {filepath}{Style.RESET_ALL}")
                
            elif format.lower() == 'json':
                filepath = f"{filename}.json"
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"{Fore.GREEN}✓ 结果已保存到: {filepath}{Style.RESET_ALL}")
                
            else:
                print(f"{Fore.RED}不支持的文件格式: {format}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}保存结果失败: {e}{Style.RESET_ALL}")
    
    def print_results_summary(self, results):
        """打印结果摘要"""
        if not results:
            print(f"{Fore.YELLOW}没有搜索结果{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}=== 搜索结果摘要 ==={Style.RESET_ALL}")
        print(f"总结果数: {len(results)}")
        
        # 按搜索引擎统计
        engine_stats = {}
        for result in results:
            engine = result.get('search_engine', '未知')
            engine_stats[engine] = engine_stats.get(engine, 0) + 1
        
        print(f"\n{Fore.YELLOW}按搜索引擎统计:{Style.RESET_ALL}")
        for engine, count in engine_stats.items():
            print(f"  {engine}: {count} 个结果")
        
        # 显示前5个结果
        print(f"\n{Fore.YELLOW}前5个结果预览:{Style.RESET_ALL}")
        for i, result in enumerate(results[:5], 1):
            print(f"\n{i}. {Fore.GREEN}{result.get('title', '无标题')}{Style.RESET_ALL}")
            print(f"   来源: {result.get('source', '未知')}")
            print(f"   搜索引擎: {result.get('search_engine', '未知')}")
            print(f"   摘要: {result.get('abstract', '无摘要')[:100]}...")
    
    def close(self):
        """关闭爬虫，释放资源"""
        if self.driver:
            self.driver.quit()
        if self.session:
            self.session.close()
        print(f"{Fore.GREEN}✓ 爬虫已关闭，资源已释放{Style.RESET_ALL}")


def main():
    """主函数"""
    print(f"{Fore.CYAN}=== 网络关键词爬虫程序 ==={Style.RESET_ALL}")
    
    try:
        # 获取用户输入
        keyword = input(f"{Fore.YELLOW}请输入要搜索的关键词: {Style.RESET_ALL}").strip()
        if not keyword:
            print(f"{Fore.RED}关键词不能为空{Style.RESET_ALL}")
            return
        
        max_pages = input(f"{Fore.YELLOW}请输入要搜索的页数 (默认3页): {Style.RESET_ALL}").strip()
        max_pages = int(max_pages) if max_pages.isdigit() else 3
        
        use_selenium = input(f"{Fore.YELLOW}是否使用Selenium (y/n, 默认n): {Style.RESET_ALL}").strip().lower()
        use_selenium = use_selenium == 'y'
        
        # 选择搜索引擎
        print(f"\n{Fore.CYAN}可用的搜索引擎:{Style.RESET_ALL}")
        print("1. 百度")
        print("2. 必应") 
        print("3. 搜狗")
        print("4. Google (需要代理)")
        print("5. 全部")
        
        engine_choice = input(f"{Fore.YELLOW}请选择搜索引擎 (1-5, 默认5): {Style.RESET_ALL}").strip()
        
        engine_map = {
            '1': ['baidu'],
            '2': ['bing'],
            '3': ['sogou'],
            '4': ['google'],
            '5': ['baidu', 'bing', 'sogou'],
            '': ['baidu', 'bing', 'sogou']
        }
        
        engines = engine_map.get(engine_choice, ['baidu', 'bing', 'sogou'])
        
        # 创建爬虫实例
        print(f"\n{Fore.BLUE}正在初始化爬虫...{Style.RESET_ALL}")
        crawler = WebCrawler(use_selenium=use_selenium)
        
        # 开始搜索
        print(f"\n{Fore.BLUE}开始搜索关键词: {keyword}{Style.RESET_ALL}")
        results = crawler.search_all_engines(keyword, max_pages, engines)
        
        # 显示结果摘要
        crawler.print_results_summary(results)
        
        # 保存结果
        if results:
            save_choice = input(f"\n{Fore.YELLOW}是否保存结果? (y/n, 默认y): {Style.RESET_ALL}").strip().lower()
            if save_choice != 'n':
                format_choice = input(f"{Fore.YELLOW}选择保存格式 (excel/csv/json, 默认excel): {Style.RESET_ALL}").strip().lower()
                format_choice = format_choice if format_choice in ['excel', 'csv', 'json'] else 'excel'
                
                filename = f"search_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                crawler.save_results(results, filename, format_choice)
        
        print(f"\n{Fore.GREEN}✓ 搜索完成！{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}用户中断程序{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}程序运行出错: {e}{Style.RESET_ALL}")
    finally:
        if 'crawler' in locals():
            crawler.close()


if __name__ == "__main__":
    main()
