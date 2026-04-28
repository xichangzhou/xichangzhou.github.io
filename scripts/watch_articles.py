#!/usr/bin/env python3
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 添加父目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generate_articles_list import generate_articles_list

class ArticlesHandler(FileSystemEventHandler):
    """处理文章目录变化的事件处理器"""
    
    def __init__(self):
        self.last_modified = time.time()
    
    def on_any_event(self, event):
        # 避免重复触发（某些编辑器会产生多个事件）
        now = time.time()
        if now - self.last_modified < 1:
            return
        self.last_modified = now
        
        # 只处理 .md 文件的变化
        if event.src_path.endswith('.md') or event.src_path.endswith('.json'):
            print(f"\n检测到文件变化: {event.event_type} - {os.path.basename(event.src_path)}")
            print("正在更新文章列表...")
            try:
                generate_articles_list()
                print("文章列表更新完成！")
            except Exception as e:
                print(f"更新失败: {e}")

def main():
    """启动文件监视"""
    md_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'md')
    
    if not os.path.exists(md_dir):
        print(f"错误：目录不存在: {md_dir}")
        sys.exit(1)
    
    print(f"开始监视目录: {md_dir}")
    print("按 Ctrl+C 停止监视")
    print("-" * 50)
    
    # 先运行一次生成初始列表
    generate_articles_list()
    print("-" * 50)
    
    # 创建事件处理器和观察者
    event_handler = ArticlesHandler()
    observer = Observer()
    observer.schedule(event_handler, md_dir, recursive=False)
    
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n停止监视")
    
    observer.join()

if __name__ == '__main__':
    main()