~~使用 Python 获取香港每日实时AQI和气温等数据，保存到mysql数据库中，同时保存一份CSV数据备用。~~

通过 Python 获取新加坡气象网站上的实时污染物和气象数据，保存到MySQL数据库中。
## HOW TO USE
### CREATE MYSQL DATABASE & TABLE
you can find the sql files in the directory sg/
- ~~hko.sql~~
- ~~pollutant.sql~~
- sg_pollutant.sql
- sg_weather.sql
- sg_visibility.sql

### ADD CONFIGURE FILE
add settings.py which contains the following code to the directory weatherdata/
```python
# mysql info must be specified 
config = {
    'user': 'username', # your mysql username
    'password': 'pwd',  # your mysql password
    'host': 'ip',     # your mysql host
    'port': 3306,      # your mysql port
    'db': 'test'  # your mysql database
}
# optional config [smtp server and email info] for receiving error message
MAIL_SERVER_HOST = ''
MAIL_SERVER_USER = ''
MAIL_SERVER_PASSWORD = ''
mail_to = [
    '',
]
```

### RUN DOCKER CONTAINER
```shell
# first run, git clone project to directory <weatherdata>
cd weatherdata && sudo docker build -t wd:1.0.0 .
# run docker container
sudo docker-compose up -d 
````

### SCHEDULE TASK
```shell
# run scheduled tasks by linux crontab   
crontab -e  
# run docker service per 8 hours
0 */8 * * * /usr/bin/zsh /opt/weatherdata/sg/sg.sh >> /opt/weatherdata/log.log 2>&1 &

