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
pyinstaller --onefile 99.Code/PYServer/webapi.py


## docker
cd ~/github/LearningNote/99.Code/PYServer/
docker build -t=dsi-delta:0.0.1 .

### 运行容器（按需设置环境变量）
docker run -d --name dsi-delta -p 5000:80 \
  --restart=always dsi-delta:0.0.1