import os
import time
import subprocess
import sys

def run_spider():
    # 获取当前脚本的路径
    current_file = os.path.abspath(__file__)
    spider_script = os.path.join(os.path.dirname(current_file), 'run_spider.py')
    
    # 使用子进程运行爬虫
    subprocess.run([sys.executable, spider_script], check=True)

def main():
    while True:
        try:
            # 运行爬虫
            run_spider()
        except Exception as e:
            print(f"爬虫运行出错: {e}")
        
        # 等待指定时间
        time.sleep(int(os.getenv('SCRAPY_INTERVAL_SECONDS', 60)))

if __name__ == '__main__':
    main() 