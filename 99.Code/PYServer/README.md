# README

## 环境初始化
python -m venv .venv
call .venv/Scripts/activate.bat
python -m pip install --upgrade pip
pip install -r 99.Code/PYServer/requirements.txt
deactivate

## 安装预编译包
pip install ta_lib-0.6.3-cp312-cp312-win_amd64.whl

## 运行
python 99.Code/PYServer/option_arbitrage_01.py

## 打包
pyinstaller --onefile 99.Code/PYServer/option_collect.py
pyinstaller --onefile 99.Code/PYServer/option_delta_monitor.py


## docker
docker build -t ***stock-server*** .

# 运行容器（按需设置环境变量）
docker run -d  --name ***stock-service*** \
  -e MSSQL_HOST=mssql \
  -e MSSQL_PASSWORD=your_sa_password \
  ***stock-server***