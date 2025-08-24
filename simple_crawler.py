#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版网络关键词爬虫
专门用于快速搜索和获取结果
"""

import requests
import time
import random
from urllib.parse import quote
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json

class SimpleCrawler:
    """简化版爬虫类"""
    
    def __init__(self):
        """初始化爬虫"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.results = []
    
    def search_baidu(self, keyword, max_pages=3):
        """百度搜索"""
        print(f"正在搜索百度: {keyword}")
        results = []
        
        for page in range(max_pages):
            try:
                pn = page * 10
                url = f"https://www.baidu.com/s?wd={quote(keyword)}&pn={pn}"
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找搜索结果
                search_results = soup.find_all('div', class_='result')
                
                for result in search_results:
                    try:
                        # 获取标题
                        title_elem = result.find('h3')
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        link = title_elem.find('a')['href'] if title_elem.find('a') else ''
                        
                        # 获取摘要
                        abstract_elem = result.find('div', class_='c-abstract')
                        abstract = abstract_elem.get_text(strip=True) if abstract_elem else ''
                        
                        # 获取来源
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
                
                print(f"第 {page + 1} 页完成，获取 {len(search_results)} 个结果")
                time.sleep(random.uniform(1, 2))  # 避免请求过快
                
            except Exception as e:
                print(f"百度搜索第 {page + 1} 页失败: {e}")
                continue
        
        return results
    
    def search_bing(self, keyword, max_pages=3):
        """必应搜索"""
        print(f"正在搜索必应: {keyword}")
        results = []
        
        for page in range(max_pages):
            try:
                first = page * 10
                url = f"https://www.bing.com/search?q={quote(keyword)}&first={first}"
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找搜索结果
                search_results = soup.find_all('li', class_='b_algo')
                
                for result in search_results:
                    try:
                        # 获取标题
                        title_elem = result.find('h3')
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        link = title_elem.find('a')['href'] if title_elem.find('a') else ''
                        
                        # 获取摘要
                        abstract_elem = result.find('p')
                        abstract = abstract_elem.get_text(strip=True) if abstract_elem else ''
                        
                        # 获取来源
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
                
                print(f"第 {page + 1} 页完成，获取 {len(search_results)} 个结果")
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"必应搜索第 {page + 1} 页失败: {e}")
                continue
        
        return results
    
    def search_all(self, keyword, max_pages=3):
        """搜索所有支持的搜索引擎"""
        all_results = []
        
        # 搜索百度
        baidu_results = self.search_baidu(keyword, max_pages)
        all_results.extend(baidu_results)
        
        # 搜索必应
        bing_results = self.search_bing(keyword, max_pages)
        all_results.extend(bing_results)
        
        return all_results
    
    def search_website(self, keyword, website_url, max_pages=3):
        """直接爬取指定网站"""
        print(f"正在爬取网站: {website_url}")
        print(f"搜索关键词: {keyword}")
        results = []
        
        try:
            # 更新请求头，模拟真实浏览器
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
                'Referer': 'https://www.google.com/',
                'DNT': '1',
                'Sec-Fetch-User': '?1'
            }
            
            print(f"🔍 正在发送请求到: {website_url}")
            
            # 设置更长的超时时间和重试机制
            for attempt in range(3):
                try:
                    response = self.session.get(website_url, headers=headers, timeout=30)
                    response.raise_for_status()
                    print(f"✅ 请求成功，状态码: {response.status_code}")
                    print(f"📄 响应大小: {len(response.text)} 字符")
                    print(f"🔍 响应编码: {response.encoding}")
                    print(f"🔍 响应头Content-Type: {response.headers.get('Content-Type', '未知')}")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e
                    print(f"第{attempt + 1}次尝试失败，正在重试...")
                    time.sleep(3)
            
            # 尝试多种编码方式
            html_content = None
            encodings_to_try = ['utf-8', 'gbk', 'gb2312', 'big5', 'latin1']
            
            for encoding in encodings_to_try:
                try:
                    response.encoding = encoding
                    html_content = response.text
                    print(f"✅ 使用编码 {encoding} 成功解析")
                    break
                except Exception as e:
                    print(f"❌ 编码 {encoding} 失败: {e}")
                    continue
            
            if html_content is None:
                # 如果所有编码都失败，使用默认方式
                html_content = response.text
                print("⚠️ 使用默认编码解析")
            
            # 尝试多种解析器
            soup = None
            parsers_to_try = ['html.parser', 'lxml', 'html5lib']
            
            for parser in parsers_to_try:
                try:
                    soup = BeautifulSoup(html_content, parser)
                    print(f"✅ 使用解析器 {parser} 成功")
                    break
                except Exception as e:
                    print(f"❌ 解析器 {parser} 失败: {e}")
                    continue
            
            if soup is None:
                raise Exception("所有解析器都失败了")
            
            # 调试：检查页面基本结构
            print(f"🔍 页面标题: {soup.title.get_text() if soup.title else '无标题'}")
            print(f"🔍 找到的标题标签数量: {len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))}")
            print(f"🔍 找到的段落标签数量: {len(soup.find_all('p'))}")
            print(f"🔍 找到的链接标签数量: {len(soup.find_all('a'))}")
            print(f"🔍 找到的div标签数量: {len(soup.find_all('div'))}")
            print(f"🔍 找到的span标签数量: {len(soup.find_all('span'))}")
            
            # 尝试查找JavaScript变量中的内容
            print("🔍 搜索JavaScript变量中的内容...")
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string:
                    script_content = script.string
                    if keyword.lower() in script_content.lower():
                        print(f"✅ 在JavaScript中找到关键词")
                        # 提取包含关键词的上下文
                        keyword_index = script_content.lower().find(keyword.lower())
                        if keyword_index != -1:
                            start = max(0, keyword_index - 100)
                            end = min(len(script_content), keyword_index + 100)
                            context = script_content[start:end]
                            
                            results.append({
                                'title': f"JavaScript中的关键词内容",
                                'link': website_url,
                                'abstract': context,
                                'source': website_url,
                                'search_engine': '直接爬取',
                                'keyword': keyword,
                                'page': 1
                            })
            
            # 方法1: 查找标题包含关键词的元素（更全面的标题标签）
            title_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title', 'a'])
            print(f"🔍 开始搜索标题元素，共找到 {len(title_elements)} 个")
            
            for title_elem in title_elements:
                title_text = title_elem.get_text(strip=True)
                if keyword.lower() in title_text.lower() and len(title_text) > 2:
                    print(f"✅ 在标题中找到关键词: {title_text[:50]}...")
                    # 查找相关的链接和摘要
                    link_url = ''
                    if title_elem.name == 'a' and title_elem.get('href'):
                        link_url = title_elem['href']
                    else:
                        link = title_elem.find('a')
                        if link and link.get('href'):
                            link_url = link['href']
                    
                    # 处理相对链接
                    if link_url and not link_url.startswith('http'):
                        if link_url.startswith('/'):
                            link_url = website_url.rstrip('/') + link_url
                        else:
                            link_url = website_url.rstrip('/') + '/' + link_url
                    
                    # 查找摘要（更智能的摘要查找）
                    abstract = ''
                    # 查找标题附近的段落
                    next_elem = title_elem.find_next_sibling()
                    if next_elem and next_elem.name == 'p':
                        abstract = next_elem.get_text(strip=True)
                    # 查找父元素中的段落
                    elif title_elem.parent:
                        parent_para = title_elem.parent.find('p')
                        if parent_para:
                            abstract = parent_para.get_text(strip=True)
                    
                    results.append({
                        'title': title_text,
                        'link': link_url,
                        'abstract': abstract,
                        'source': website_url,
                        'search_engine': '直接爬取',
                        'keyword': keyword,
                        'page': 1
                    })
            
            # 方法2: 查找段落中包含关键词的内容（更智能的段落查找）
            paragraphs = soup.find_all(['p', 'div', 'span'])
            print(f"🔍 开始搜索段落元素，共找到 {len(paragraphs)} 个")
            
            for p in paragraphs:
                p_text = p.get_text(strip=True)
                if (keyword.lower() in p_text.lower() and 
                    len(p_text) > 15 and 
                    len(p_text) < 500):  # 避免过长的内容
                    
                    print(f"✅ 在段落中找到关键词: {p_text[:50]}...")
                    
                    # 查找相关的标题
                    title = ''
                    # 向上查找标题
                    prev_elem = p.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    if prev_elem:
                        title = prev_elem.get_text(strip=True)
                    # 查找父元素中的标题
                    elif p.parent:
                        parent_title = p.parent.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                        if parent_title:
                            title = parent_title.get_text(strip=True)
                    
                    # 查找链接
                    link_url = ''
                    link = p.find('a')
                    if link and link.get('href'):
                        link_url = link['href']
                        if not link_url.startswith('http'):
                            if link_url.startswith('/'):
                                link_url = website_url.rstrip('/') + link_url
                            else:
                                link_url = website_url.rstrip('/') + '/' + link_url
                    
                    results.append({
                        'title': title or f"包含关键词的段落",
                        'link': link_url,
                        'abstract': p_text[:200] + '...' if len(p_text) > 200 else p_text,
                        'source': website_url,
                        'search_engine': '直接爬取',
                        'keyword': keyword,
                        'page': 1
                    })
            
            # 方法3: 查找链接文本包含关键词的链接
            links = soup.find_all('a')
            print(f"🔍 开始搜索链接元素，共找到 {len(links)} 个")
            
            for link in links:
                link_text = link.get_text(strip=True)
                if (keyword.lower() in link_text.lower() and 
                    len(link_text) > 2 and 
                    len(link_text) < 100):  # 避免过长的链接文本
                    
                    print(f"✅ 在链接中找到关键词: {link_text[:50]}...")
                    
                    link_url = link.get('href', '')
                    if link_url and not link_url.startswith('http'):
                        if link_url.startswith('/'):
                            link_url = website_url.rstrip('/') + link_url
                        else:
                            link_url = website_url.rstrip('/') + '/' + link_url
                    
                    # 查找链接附近的摘要
                    abstract = ''
                    next_elem = link.find_next_sibling()
                    if next_elem and next_elem.name == 'p':
                        abstract = next_elem.get_text(strip=True)
                    # 查找父元素中的段落
                    elif link.parent:
                        parent_para = link.parent.find('p')
                        if parent_para:
                            abstract = parent_para.get_text(strip=True)
                    
                    results.append({
                        'title': link_text,
                        'link': link_url,
                        'abstract': abstract,
                        'source': website_url,
                        'search_engine': '直接爬取',
                        'keyword': keyword,
                        'page': 1
                    })
            
            # 方法4: 查找表格中包含关键词的内容
            tables = soup.find_all('table')
            print(f"🔍 开始搜索表格元素，共找到 {len(tables)} 个")
            
            for table in tables:
                table_text = table.get_text(strip=True)
                if keyword.lower() in table_text.lower():
                    print(f"✅ 在表格中找到关键词")
                    # 查找表格标题
                    caption = table.find('caption')
                    title = caption.get_text(strip=True) if caption else "包含关键词的表格"
                    
                    # 提取表格摘要
                    rows = table.find_all('tr')
                    table_summary = []
                    for row in rows[:3]:  # 只取前3行作为摘要
                        cells = row.find_all(['td', 'th'])
                        row_text = ' | '.join([cell.get_text(strip=True) for cell in cells])
                        if row_text:
                            table_summary.append(row_text)
                    
                    abstract = ' | '.join(table_summary)
                    
                    results.append({
                        'title': title,
                        'link': '',
                        'abstract': abstract,
                        'source': website_url,
                        'search_engine': '直接爬取',
                        'keyword': keyword,
                        'page': 1
                    })
            
            print(f"🔍 初步搜索完成，找到 {len(results)} 个结果")
            
            # 去重结果（基于标题和摘要的组合）
            unique_results = []
            seen_content = set()
            for result in results:
                content_key = f"{result['title']}_{result['abstract'][:50]}"
                if content_key not in seen_content:
                    unique_results.append(result)
                    seen_content.add(content_key)
            
            print(f"🔍 去重后剩余 {len(unique_results)} 个结果")
            
            # 如果没有找到结果，尝试更宽松的搜索
            if not unique_results:
                print("⚠️ 未找到精确匹配，尝试模糊搜索...")
                # 搜索包含关键词字符的内容
                all_text = soup.get_text()
                print(f"🔍 页面总文本长度: {len(all_text)} 字符")
                
                if keyword.lower() in all_text.lower():
                    print("✅ 页面确实包含关键词，尝试提取上下文...")
                    # 提取包含关键词的上下文
                    keyword_index = all_text.lower().find(keyword.lower())
                    if keyword_index != -1:
                        start = max(0, keyword_index - 100)
                        end = min(len(all_text), keyword_index + 100)
                        context = all_text[start:end]
                        
                        unique_results.append({
                            'title': f"包含关键词的页面内容",
                            'link': website_url,
                            'abstract': context,
                            'source': website_url,
                            'search_engine': '直接爬取',
                            'keyword': keyword,
                            'page': 1
                        })
                        print("✅ 通过模糊搜索找到相关内容")
                else:
                    print("❌ 页面中确实没有找到关键词")
                    
                    # 尝试搜索关键词的部分字符
                    print("🔍 尝试搜索关键词的部分字符...")
                    for i in range(len(keyword), 1, -1):
                        partial_keyword = keyword[:i]
                        if partial_keyword.lower() in all_text.lower():
                            print(f"✅ 找到部分关键词: {partial_keyword}")
                            keyword_index = all_text.lower().find(partial_keyword.lower())
                            start = max(0, keyword_index - 100)
                            end = min(len(all_text), keyword_index + 100)
                            context = all_text[start:end]
                            
                            unique_results.append({
                                'title': f"包含部分关键词'{partial_keyword}'的页面内容",
                                'link': website_url,
                                'abstract': context,
                                'source': website_url,
                                'search_engine': '直接爬取',
                                'keyword': keyword,
                                'page': 1
                            })
                            break
            
            print(f"🎯 最终结果数量: {len(unique_results)}")
            return unique_results
            
        except Exception as e:
            print(f"❌ 爬取网站失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def save_results(self, results, filename=None, format='excel'):
        """保存搜索结果"""
        if not results:
            print("没有结果可保存")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_{timestamp}"
        
        try:
            df = pd.DataFrame(results)
            
            if format.lower() == 'excel':
                filepath = f"{filename}.xlsx"
                df.to_excel(filepath, index=False, engine='openpyxl')
                print(f"结果已保存到: {filepath}")
                
            elif format.lower() == 'csv':
                filepath = f"{filename}.csv"
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
                print(f"结果已保存到: {filepath}")
                
            elif format.lower() == 'json':
                filepath = f"{filename}.json"
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"结果已保存到: {filepath}")
                
            else:
                print(f"不支持的文件格式: {format}")
                
        except Exception as e:
            print(f"保存结果失败: {e}")
    
    def print_summary(self, results):
        """打印结果摘要"""
        if not results:
            print("没有搜索结果")
            return
        
        print(f"\n=== 搜索结果摘要 ===")
        print(f"总结果数: {len(results)}")
        
        # 按搜索引擎统计
        engine_stats = {}
        for result in results:
            engine = result.get('search_engine', '未知')
            engine_stats[engine] = engine_stats.get(engine, 0) + 1
        
        print(f"\n按搜索引擎统计:")
        for engine, count in engine_stats.items():
            print(f"  {engine}: {count} 个结果")
        
        # 显示前3个结果
        print(f"\n前3个结果预览:")
        for i, result in enumerate(results[:3], 1):
            print(f"\n{i}. {result.get('title', '无标题')}")
            print(f"   来源: {result.get('source', '未知')}")
            print(f"   搜索引擎: {result.get('search_engine', '未知')}")
            if result.get('abstract'):
                print(f"   摘要: {result.get('abstract', '')[:80]}...")


def main():
    """主函数"""
    print("=== 简化版网络关键词爬虫 ===")
    
    try:
        # 获取用户输入
        keyword = input("请输入要搜索的关键词: ").strip()
        if not keyword:
            print("关键词不能为空")
            return
        
        max_pages = input("请输入要搜索的页数 (默认2页): ").strip()
        max_pages = int(max_pages) if max_pages.isdigit() else 2
        
        # 创建爬虫实例
        print(f"\n正在搜索关键词: {keyword}")
        crawler = SimpleCrawler()
        
        # 开始搜索
        results = crawler.search_all(keyword, max_pages)
        
        # 显示结果摘要
        crawler.print_summary(results)
        
        # 保存结果
        if results:
            save_choice = input(f"\n是否保存结果? (y/n, 默认y): ").strip().lower()
            if save_choice != 'n':
                format_choice = input("选择保存格式 (excel/csv/json, 默认excel): ").strip().lower()
                format_choice = format_choice if format_choice in ['excel', 'csv', 'json'] else 'excel'
                
                filename = f"search_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                crawler.save_results(results, filename, format_choice)
        
        print(f"\n搜索完成！")
        
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"\n程序运行出错: {e}")


if __name__ == "__main__":
    main()
