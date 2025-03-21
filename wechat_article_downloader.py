#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
from datetime import datetime
import logging
import sys
from typing import List, Dict, Optional
import urllib.parse
import requests
from dotenv import load_dotenv

class WechatArticleDownloader:
    def __init__(self):
        """初始化下载器"""
        self.logger = self._setup_logging()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        # 加载.env文件
        load_dotenv(os.path.join(self.base_dir, '.env'))
        # 从.env文件中读取API密钥
        self.api_key = os.getenv('WEB_READER_API_KEY')
        # 设置 Web Reader API 的基础 URL
        self.base_url = "https://api.unifuncs.com/api/web-reader/"

    def _setup_logging(self) -> logging.Logger:
        """设置日志记录"""
        os.makedirs('logs', exist_ok=True)
        log_filename = os.path.join('logs', f'downloader_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def validate_url(self, url: str) -> bool:
        """验证微信公众号合集URL"""
        try:
            parsed = urllib.parse.urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            if 'mp.weixin.qq.com' not in parsed.netloc:
                return False
            if 'appmsgalbum' not in parsed.path:
                return False
            return True
        except Exception as e:
            self.logger.error(f"URL验证失败: {str(e)}")
            return False

    def _setup_driver(self):
        """设置并返回Chrome驱动"""
        try:
            self.logger.info("开始设置Chrome驱动...")
            options = uc.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            
            driver = uc.Chrome(
                options=options,
                driver_executable_path='/Users/qinxiaoqiang/chromedriver/chromeddriver/chromedriver',
                suppress_welcome=True
            )
            self.logger.info("Chrome驱动初始化成功")
            return driver
        except Exception as e:
            self.logger.error(f"设置Chrome驱动时出错: {str(e)}")
            raise

    def _scroll_and_extract(self, driver) -> List[Dict[str, str]]:
        """滚动页面并提取文章信息"""
        articles = []
        scroll_count = 0
        last_articles_count = 0
        no_new_content_count = 0
        
        try:
            while True:
                scroll_count += 1
                self.logger.debug(f"执行第 {scroll_count} 次滚动")
                
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(3)
                
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.album__list-item'))
                    )
                except Exception as e:
                    self.logger.warning(f"等待文章元素超时: {str(e)}")
                
                items = driver.find_elements(By.CSS_SELECTOR, 'li.album__list-item')
                self.logger.debug(f"当前页面找到 {len(items)} 个文章元素")
                
                for item in items:
                    try:
                        title = item.get_attribute('data-title')
                        link = item.get_attribute('data-link')
                        if title and link and {'title': title, 'url': link} not in articles:
                            articles.append({'title': title, 'url': link})
                            self.logger.debug(f"新增文章: {title}")
                    except Exception as e:
                        self.logger.error(f"提取文章信息时出错: {str(e)}")
                
                if len(articles) > last_articles_count:
                    self.logger.info(f"已找到 {len(articles)} 篇文章")
                    last_articles_count = len(articles)
                    no_new_content_count = 0
                else:
                    no_new_content_count += 1
                
                if no_new_content_count >= 3 or scroll_count > 100:
                    break
            
            return articles
        except Exception as e:
            self.logger.error(f"滚动和提取过程出错: {str(e)}")
            raise

    def save_articles(self, articles: List[Dict[str, str]], output_dir: str):
        """保存文章信息到文件"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # 保存为文本格式
            txt_file = os.path.join(output_dir, 'article_list.txt')
            self.logger.info(f"保存文本格式到: {txt_file}")
            with open(txt_file, 'w', encoding='utf-8') as f:
                for idx, article in enumerate(articles, 1):
                    f.write(f'[{idx}] 标题：{article["title"]}\n链接：{article["url"]}\n\n')
            
            # 保存为JSON格式
            json_file = os.path.join(output_dir, 'article_list.json')
            self.logger.info(f"保存JSON格式到: {json_file}")
            articles_json = [{'id': idx, **article} for idx, article in enumerate(articles, 1)]
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(articles_json, f, ensure_ascii=False, indent=2)
            
            self.logger.info("文章列表保存完成")
        except Exception as e:
            self.logger.error(f"保存文章列表时出错: {str(e)}")
            raise

    def format_url(self, url: str) -> str:
        """格式化URL以供API使用"""
        try:
            parsed = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed.query)
            if 'chksm' in query_params:
                query_params['chksm'] = [query_params['chksm'][0]]
            new_query = urllib.parse.urlencode(query_params, doseq=True)
            clean_url = urllib.parse.urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment
            ))
            encoded_url = urllib.parse.quote_plus(clean_url)
            return f"{self.base_url}{encoded_url}?apiKey={self.api_key}"
        except Exception as e:
            self.logger.error(f"URL格式化错误: {str(e)}")
            encoded_url = urllib.parse.quote_plus(url)
            return f"{self.base_url}{encoded_url}?apiKey={self.api_key}"

    def get_article_content(self, url: str) -> Optional[str]:
        """通过Web Reader API获取文章内容"""
        try:
            formatted_url = self.format_url(url)
            headers = {
                'Accept': 'text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            
            with requests.get(formatted_url, headers=headers, timeout=30, stream=True) as response:
                response.raise_for_status()
                response.encoding = response.apparent_encoding or 'utf-8'
                chunks = []
                for chunk in response.iter_content(chunk_size=8192, decode_unicode=True):
                    if chunk:
                        chunks.append(chunk)
                
                markdown_content = ''.join(chunks)
                remove_keywords = [
                    '**推荐阅读**',
                    '推荐阅读',
                    '诊疗经验谈',
                    '继续滑动看下一个',
                    '轻触阅读原文'
                ]
                
                for keyword in remove_keywords:
                    if keyword in markdown_content:
                        markdown_content = markdown_content.split(keyword)[0].strip()
                
                return f"原始URL: {url}\n\n{markdown_content}"
        except Exception as e:
            self.logger.error(f"获取文章内容时出错: {str(e)}")
            return None

    def download_articles(self, articles: List[Dict[str, str]], output_dir: str):
        """下载文章内容"""
        download_dir = os.path.join(output_dir, 'download_content')
        os.makedirs(download_dir, exist_ok=True)
        
        total_articles = len(articles)
        for i, article in enumerate(articles, 1):
            try:
                url = article['url']
                title = article['title']
                self.logger.info(f'处理第 {i}/{total_articles} 个文章: {title}')
                
                content = self.get_article_content(url)
                if content:
                    safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_'))
                    safe_title = safe_title[:50] if len(safe_title) > 50 else safe_title
                    filename = f'{safe_title}_{datetime.now().strftime("%Y%m%d%H%M%S")}.md'
                    output_file = os.path.join(download_dir, filename)
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.logger.info(f'已保存到: {filename}')
                else:
                    self.logger.error(f'获取文章内容失败: {title}')
            except Exception as e:
                self.logger.error(f'处理文章时出错: {str(e)}')
                continue

    def run(self):
        """运行下载器"""
        try:
            # 第一步：输入并验证URL
            while True:
                url = input("请输入微信公众号合集URL: ").strip()
                if self.validate_url(url):
                    break
                print("无效的URL，请输入正确的微信公众号合集URL")
            
            # 第二步：输入保存路径
            while True:
                save_dir = input("请输入保存文件的目录路径: ").strip()
                if os.path.isabs(save_dir):
                    break
                print("请输入绝对路径")
            
            self.logger.info("=== 开始运行微信文章下载器 ===")
            self.logger.info(f"目标URL: {url}")
            
            # 设置浏览器驱动并获取文章列表
            driver = self._setup_driver()
            try:
                self.logger.info("正在访问页面...")
                driver.get(url)
                time.sleep(5)
                
                self.logger.info("开始提取文章列表...")
                articles = self._scroll_and_extract(driver)
                self.logger.info(f"共找到 {len(articles)} 篇文章")
                
                # 保存文章列表
                self.save_articles(articles, save_dir)
                
                # 下载文章内容
                self.download_articles(articles, save_dir)
                
                self.logger.info("=== 下载器运行完成 ===")
            finally:
                driver.quit()
                
        except Exception as e:
            self.logger.error(f"程序运行出错: {str(e)}")
            sys.exit(1)

def main():
    try:
        downloader = WechatArticleDownloader()
        downloader.run()
    except Exception as e:
        print(f"程序执行失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()