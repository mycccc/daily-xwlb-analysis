import os
from datetime import datetime

# 新闻联播数据源
XWLB_URL_TEMPLATE = "https://cn.govopendata.com/xinwenlianbo/{date}/"
XWLB_FALLBACK_URL = "https://tv.cctv.com/lm/xwlb/"

# 当天日期
TODAY = datetime.now().strftime("%Y%m%d")
TODAY_FULL = datetime.now().strftime("%Y-%m-%d")

# DeepSeek API 配置（通过环境变量读取）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# 输出文件
OUTPUT_MD = f"output/{TODAY}_xinwenlianbo.md"
OUTPUT_HTML = f"output/{TODAY}_xinwenlianbo.html"