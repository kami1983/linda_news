## 这是一个基于 Python 的爬虫项目

## Install python 3.9
* conda env list
* conda create --name linda-news python=3.9
* conda activate linda-news

### 项目结构

```bash
.
├── README.md
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── utils.py
├── tests
│   ├── __init__.py
│   ├── test_main.py
├── .gitignore
├── .pre-commit-config.yaml

```

## How to Run
```
bash
pip install -r requirements.txt
python main.py
```

## Start MySQL
```
docker-compose up -d
```

### supervisorctl

```
sudo apt update 
sudo apt install supervisor -y
sudo vi /etc/supervisor/conf.d/linda_trade.conf 
```
* 重启服务
```
sudo supervisorctl reread
sudo supervisorctl update
sudo systemctl restart supervisor
```

### fetch mysql data
```
SELECT * 
FROM linda_news.linda_news 
WHERE 
  publish_time >= CURDATE() 
  AND publish_time < CURDATE() + INTERVAL 1 DAY
ORDER BY 
  publish_time DESC;
```

### Start product frontend
```
cd frontend
npm install
npm run build
npm run preview
```

## Start unit test
```
python -m unittest discover -s test
python -m unittest discover -s test -p "test_csv_manager.py"
```

## Project Function
### fill news category and concept
* `python -m src.app_ai_filler`

### start api service
* `python -m src.app_api_service`

### start spider listener
* `python -m src.app_spider_listener`

