FROM python:3.11
LABEL maintainer="warn1667@hotmail.com"
# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /WeatherData
WORKDIR /WeatherData

# 将 requirements.txt 复制到容器的 code 目录
ADD requirements.txt /WeatherData/requirements.txt
# 更新 pip & 安装库
RUN pip install pip -U && pip install -r requirements.txt -U
# 将当前目录复制到容器
#ADD ./WeatherData /WeatherData/