# 配置
~/.condarc


## 软件源
conda config --show channels
### 切换为中国科技大学源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
### 搜索时显示通道地址
conda config --set show_channel_urls yes


## 包管理
conda list
conda install pip
conda update conda
conda update --all
### 清理
conda clean -a      //删除所有没有依托的包以及tar包
conda clean -p      //删除没有用的包
conda clean -t      //删除tar包


## 环境
conda env list
conda create -n your_env_name python=x.x
### 激活
conda init cmd.exe
conda activate your_env_name
conda deactivate


