## 软件源
conda config –-show
### 切换为中国科技大学源
conda config –-add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
conda config –-add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
conda config –-add channels https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
conda config –-add channels https://mirrors.ustc.edu.cn/anaconda/cloud/msys2/
conda config –-add channels https://mirrors.ustc.edu.cn/anaconda/cloud/bioconda/
conda config –-add channels https://mirrors.ustc.edu.cn/anaconda/cloud/menpo/
conda config –-set show_channel_urls yes



## 包管理
conda list
conda install pip
conda update conda
conda update --all



## 环境
conda env list
conda create -n your_env_name python=x.x
### 激活
conda activate your_env_name
conda deactivate
