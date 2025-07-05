# 视频脚本一键生成器

## 功能
基于LangChain和OpenAI生成视频脚本的工具。

## 使用方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
创建`.env`文件：
```
BASE_URL=your_api_base_url
```

### 3. 运行测试
```bash
python test_runner.py
```

### 4. 使用代码
```python
from utils import generate_script

search_result, title, script = generate_script(
    subject="人工智能",
    video_length=5,
    creativity=0.7,
    api_key="your_api_key"
)
```

## 文件结构
```
├── utils.py           # 核心功能模块
├── requirements.txt   # 依赖包
├── test_runner.py     # 测试运行器
├── tests/
│   └── test_core.py   # 核心测试
├── pytest.ini        # 测试配置
└── .env              # 环境变量
```
