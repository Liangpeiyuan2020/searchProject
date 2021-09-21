FROM python:3.6
#代码添加到code文件夹
ADD . /code
# 设置code文件夹是工作目录
WORKDIR /code

COPY requirements.txt requirements.txt
#按照requirements.txt文件安装依赖并且
#从web获取nodejs
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/ &&\
    wget https://nodejs.org/dist/v10.16.0/node-v10.16.0-linux-x64.tar.xz &&\
    tar xf node-v10.16.0-linux-x64.tar.xz -C /opt/
ENV PATH=$PATH:/opt/node-v10.16.0-linux-x64/bin
RUN node -v
#复制项目到镜像
COPY ./app /app
#镜像执行入口
CMD ["python", "/app/main.py"]