# Anaconda3环境下部署

## 环境

conda env list

### 创建虚拟环境

conda create -n autogpt
conda activate autogpt

### 从模板创建环境配置
cp .env.template .env

### 修改配置文件
OPENAI_API_KEY=your-openai-api-key

### 启动（GPT3.5 ONLY Mode）
python -m autogpt --gpt3only

## 日常启动
conda activate autogpt
e:
cd E:\~GitHub\Auto-GPT-0.2.0
python -m autogpt --gpt3only
