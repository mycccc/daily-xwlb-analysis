import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def fetch_from_govopendata(date_str):
    """从 cn.govopendata.com 抓取新闻联播文字稿"""
    url = f"https://cn.govopendata.com/xinwenlianbo/{date_str}/"
    try:
        resp = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # 定位主要内容区域
            articles = soup.select("article, .content, .entry-content, main")
            if articles:
                return articles[0].get_text(strip=True, separator="\n")
    except Exception as e:
        print(f"govopendata 抓取失败: {e}")
    return None

def fetch_from_cctv():
    """从央视官网抓取（备用）"""
    url = "https://tv.cctv.com/lm/xwlb/"
    try:
        resp = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # 查找当天新闻链接
            today_links = soup.find_all("a", href=re.compile(r"xwlb"))
            if today_links:
                detail_url = today_links[0]["href"]
                if not detail_url.startswith("http"):
                    detail_url = "https://tv.cctv.com" + detail_url
                detail_resp = requests.get(detail_url, timeout=15)
                if detail_resp.status_code == 200:
                    detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
                    content = detail_soup.find("div", class_=re.compile(r"content|text|article"))
                    if content:
                        return content.get_text(strip=True, separator="\n")
    except Exception as e:
        print(f"CCTV 抓取失败: {e}")
    return None

def get_xwlb_content(date_str=None):
    """主抓取函数：优先 govopendata，失败则用 CCTV"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")

    print(f"正在抓取 {date_str} 的新闻联播文字稿...")

    # 方案1：govopendata
    content = fetch_from_govopendata(date_str)
    if content and len(content) > 100:
        print("成功从 govopendata 获取内容")
        return content, "govopendata"

    # 方案2：CCTV 官网
    print("govopendata 失败，尝试 CCTV 官网...")
    content = fetch_from_cctv()
    if content and len(content) > 100:
        print("成功从 CCTV 官网获取内容")
        return content, "cctv"

    raise Exception("所有数据源均抓取失败，请检查网络或数据源可用性")

if __name__ == "__main__":
    content, source = get_xwlb_content()
    print(f"来源: {source}")
    print(content[:500])