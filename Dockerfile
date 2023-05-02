FROM python:3.11
LABEL maintainer="warn1667@hotmail.com"
# set timezone=Asia/Shanghai
ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive
RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /WeatherData
WORKDIR /WeatherData

# 将 requirements.txt 复制到容器的 code 目录
ADD requirements.txt /WeatherData/requirements.txt
# 更新 pip & 安装库
RUN pip install pip --no-cache-dir -U -i https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir -r requirements.txt -U -i https://mirrors.aliyun.com/pypi/simple/ \

# 将当前目录复制到容器
#ADD ./WeatherData /WeatherData/