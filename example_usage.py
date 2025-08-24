#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫使用示例
展示如何在代码中使用爬虫类
"""

from simple_crawler import SimpleCrawler
from web_crawler import WebCrawler
import time

def example_simple_crawler():
    """使用简化版爬虫的示例"""
    print("=== 简化版爬虫使用示例 ===")
    
    # 创建爬虫实例
    crawler = SimpleCrawler()
    
    # 搜索关键词
    keyword = "Python爬虫教程"
    print(f"搜索关键词: {keyword}")
    
    # 执行搜索
    results = crawler.search_all(keyword, max_pages=2)
    
    # 显示结果
    crawler.print_summary(results)
    
    # 保存结果
    if results:
        filename = f"example_search_{keyword}"
        crawler.save_results(results, filename, 'excel')
    
    print("简化版爬虫示例完成！\n")

def example_web_crawler():
    """使用完整版爬虫的示例"""
    print("=== 完整版爬虫使用示例 ===")
    
    # 创建爬虫实例（使用Selenium）
    crawler = WebCrawler(use_selenium=False, headless=True)
    
    try:
        # 搜索关键词
        keyword = "机器学习算法"
        print(f"搜索关键词: {keyword}")
        
        # 选择搜索引擎
        engines = ['baidu', 'bing']
        
        # 执行搜索
        results = crawler.search_all_engines(keyword, max_pages=2, engines=engines)
        
        # 显示结果
        crawler.print_results_summary(results)
        
        # 保存结果
        if results:
            filename = f"example_advanced_{keyword}"
            crawler.save_results(results, filename, 'json')
        
        print("完整版爬虫示例完成！\n")
        
    finally:
        # 关闭爬虫
        crawler.close()

def example_batch_search():
    """批量搜索示例"""
    print("=== 批量搜索示例 ===")
    
    # 关键词列表
    keywords = [
        "人工智能",
        "深度学习", 
        "自然语言处理",
        "计算机视觉"
    ]
    
    # 创建爬虫实例
    crawler = SimpleCrawler()
    
    all_results = []
    
    for i, keyword in enumerate(keywords, 1):
        print(f"\n[{i}/{len(keywords)}] 搜索: {keyword}")
        
        # 搜索每个关键词
        results = crawler.search_all(keyword, max_pages=1)
        all_results.extend(results)
        
        # 添加延迟，避免请求过快
        if i < len(keywords):
            time.sleep(2)
    
    # 显示总结果
    print(f"\n批量搜索完成！总共获取 {len(all_results)} 个结果")
    
    # 保存所有结果
    if all_results:
        filename = "batch_search_results"
        crawler.save_results(all_results, filename, 'excel')
    
    print("批量搜索示例完成！\n")

def example_custom_filter():
    """自定义过滤示例"""
    print("=== 自定义过滤示例 ===")
    
    # 创建爬虫实例
    crawler = SimpleCrawler()
    
    # 搜索关键词
    keyword = "Python编程"
    results = crawler.search_all(keyword, max_pages=2)
    
    # 自定义过滤：只保留包含特定关键词的结果
    filtered_results = []
    target_keywords = ['教程', '入门', '基础']
    
    for result in results:
        title = result.get('title', '').lower()
        abstract = result.get('abstract', '').lower()
        
        # 检查标题或摘要是否包含目标关键词
        if any(keyword.lower() in title or keyword.lower() in abstract 
               for keyword in target_keywords):
            filtered_results.append(result)
    
    print(f"原始结果: {len(results)} 个")
    print(f"过滤后结果: {len(filtered_results)} 个")
    
    # 显示过滤后的结果
    if filtered_results:
        print("\n过滤后的结果:")
        for i, result in enumerate(filtered_results[:3], 1):
            print(f"{i}. {result.get('title', '无标题')}")
            print(f"   来源: {result.get('source', '未知')}")
    
    # 保存过滤后的结果
    if filtered_results:
        filename = f"filtered_{keyword}"
        crawler.save_results(filtered_results, filename, 'csv')
    
    print("自定义过滤示例完成！\n")

def main():
    """主函数"""
    print("网络关键词爬虫使用示例")
    print("=" * 50)
    
    try:
        # 运行各种示例
        example_simple_crawler()
        example_web_crawler()
        example_batch_search()
        example_custom_filter()
        
        print("所有示例运行完成！")
        
    except Exception as e:
        print(f"示例运行出错: {e}")
    
    print("\n提示: 您可以修改这些示例代码来满足自己的需求")

if __name__ == "__main__":
    main()
