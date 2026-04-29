#!/usr/bin/env python3
import os
import json

def generate_articles_list():
    """扫描 assets/md 目录并生成 articles.json 文件"""
    md_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'md')
    articles = []
    
    # 遍历目录，找到所有 .md 文件
    for filename in os.listdir(md_dir):
        if filename.endswith('.md') and filename != 'index.md':
            # 去掉 .md 后缀，只保留文件名
            article_name = os.path.splitext(filename)[0]
            articles.append(article_name)
    
    # 按文件名排序
    articles.sort()
    
    # 创建输出内容
    output = {
        "articles": articles
    }
    
    # 写入 articles.json 文件
    output_path = os.path.join(md_dir, 'articles.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"已生成 {len(articles)} 篇文章列表")
    for article in articles:
        print(f"  - {article}")

if __name__ == '__main__':
    generate_articles_list()