import os
import time
import subprocess
import sys

from dotenv import load_dotenv
load_dotenv()

def run_spider():
    subprocess.run([sys.executable, '-m', 'src.run_spider'], check=True)

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