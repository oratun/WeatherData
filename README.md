使用 Python 获取香港每日实时AQI和气温等数据，保存到mysql数据库中，同时保存一份CSV数据备用。

## 安装依赖
pip install -r requirements.txt

## 创建数据表
创建MYSQL数据表
hko.sql
pollutant.sql
## 指定数据库配置
vim db_config.py
```python
config = {
    'user': 'username',
    'password': 'pwd',
    'host': 'ip',
    'port': 3306,
    'db': 'test'
}
```

## 运行
通过linux crontab 命令运行定时任务  
其中AQI数据脚本(run.sh)每天运行两次，气温数据(hko.sh)每五分钟运行一次。  
crontab -e  
0 0 * * * /usr/bin/zsh /opt/air/run.sh >> /opt/air/log.log 2>&1 &  
0 12 * * * /usr/bin/zsh /opt/air/run.sh >> /opt/air/log.log 2>&1 &  
*/5 * * * * /usr/bin/zsh /opt/air/hko.sh >> /opt/air/hko_log.log 2>&1 &

