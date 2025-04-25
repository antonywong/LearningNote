FROM python:3.12-alpine
WORKDIR /app

COPY . .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 80

CMD gunicorn -c gunicorn.conf webapi:app
