# 配置
~\AppData\Roaming\pip\pip.ini

## 查看
pip config list
## 切换为中国科技大学源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

## 安装与更新
python -m pip install --upgrade pip

## 软件管理
pip list
pip list --not-required
pip list --outdated

pip install pandas
pip install --upgrade pandas
pip uninstall pandas -y

pip freeze --local | grep -v '^\-e' | cut -d = -f 1 | xargs pip install -U