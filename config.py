#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫配置文件
用户可以在这里修改各种参数
"""

# 搜索引擎配置
SEARCH_ENGINES = {
    'baidu': {
        'name': '百度',
        'url': 'https://www.baidu.com/s',
        'enabled': True,
        'max_pages': 5,
        'delay_range': (1, 3),  # 请求间隔范围（秒）
        'timeout': 10
    },
    'bing': {
        'name': '必应',
        'url': 'https://www.bing.com/search',
        'enabled': True,
        'max_pages': 5,
        'delay_range': (1, 3),
        'timeout': 10
    },
    'sogou': {
        'name': '搜狗',
        'url': 'https://www.sogou.com/web',
        'enabled': True,
        'max_pages': 5,
        'delay_range': (1, 3),
        'timeout': 10
    },
    'google': {
        'name': 'Google',
        'url': 'https://www.google.com/search',
        'enabled': False,  # 默认禁用，需要代理
        'max_pages': 3,
        'delay_range': (2, 5),
        'timeout': 15
    }
}

# 请求头配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# 输出配置
OUTPUT_CONFIG = {
    'default_format': 'excel',  # 默认输出格式
    'encoding': 'utf-8-sig',   # 文件编码
    'include_timestamp': True,  # 文件名是否包含时间戳
    'max_preview_results': 5,   # 预览结果的最大数量
}

# 爬虫行为配置
CRAWLER_CONFIG = {
    'use_selenium': False,      # 是否使用Selenium
    'headless': True,           # Selenium是否使用无头模式
    'retry_times': 3,           # 失败重试次数
    'respect_robots_txt': True, # 是否遵守robots.txt
    'random_delay': True,       # 是否使用随机延迟
}

# 代理配置（如果需要）
PROXY_CONFIG = {
    'use_proxy': False,
    'proxies': {
        'http': None,
        'https': None
    }
}

# 关键词过滤配置
FILTER_CONFIG = {
    'min_title_length': 5,      # 标题最小长度
    'max_title_length': 200,    # 标题最大长度
    'exclude_domains': [],      # 排除的域名
    'include_domains': [],      # 只包含的域名
    'keyword_blacklist': [],    # 关键词黑名单
}

# 日志配置
LOG_CONFIG = {
    'enable_logging': True,
    'log_level': 'INFO',
    'log_file': 'crawler.log',
    'log_format': '%(asctime)s - %(levelname)s - %(message)s'
}
