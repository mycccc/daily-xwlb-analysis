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
            articles = soup.select("article, .content, .entry-content, main")
            if articles:
                text = articles[0].get_text(strip=True, separator="\n")
                return text
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

def fetch_from_mrxwlb(date_str):
    """
    从 mrxwlb.com 抓取
    URL 格式: https://mrxwlb.com/YYYY/MM/DD/
    """
    year, month, day = date_str[:4], date_str[4:6], date_str[6:8]
    url = f"https://mrxwlb.com/{year}/{month}/{day}/"
    try:
        resp = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # 常见内容容器
            content_div = soup.find("div", class_="entry-content") or \
                          soup.find("article") or \
                          soup.find("div", class_="post-content")
            if content_div:
                text = content_div.get_text(strip=True, separator="\n")
                text = re.sub(r'\n{3,}', '\n\n', text)
                return text
    except Exception as e:
        print(f"mrxwlb 抓取失败: {e}")
    return None

def fetch_from_0645(date_str):
    """
    从 www.0645.cn 抓取
    尝试两种 URL 格式: /xwlb/YYYYMMDD.html 或 /xwlb/YYYYMMDD
    """
    base = "https://www.0645.cn/xwlb/"
    urls = [f"{base}{date_str}.html", f"{base}{date_str}"]
    for url in urls:
        try:
            resp = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }, timeout=15)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                # 尝试常见文章容器
                content_div = soup.find("div", class_="article-content") or \
                              soup.find("div", class_="content") or \
                              soup.find("article")
                if content_div:
                    text = content_div.get_text(strip=True, separator="\n")
                else:
                    # 后备：移除干扰标签后取 body 文本
                    for tag in soup(["script", "style", "nav", "footer", "header"]):
                        tag.decompose()
                    text = soup.body.get_text(strip=True, separator="\n") if soup.body else ""
                if text and len(text) > 200:
                    return text
        except Exception as e:
            print(f"0645 抓取失败 ({url}): {e}")
    return None

def get_xwlb_content(date_str=None):
    """
    主抓取函数，按顺序尝试四个数据源
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")

    print(f"正在抓取 {date_str} 的新闻联播文字稿...")

    # 1. govopendata
    content = fetch_from_govopendata(date_str)
    if content and len(content) > 100:
        return content, "govopendata"

    # 2. CCTV 官网
    print("govopendata 失败，尝试 CCTV 官网...")
    content = fetch_from_cctv()
    if content and len(content) > 100:
        return content, "cctv"

    # 3. mrxwlb.com
    print("CCTV 失败，尝试 mrxwlb.com...")
    content = fetch_from_mrxwlb(date_str)
    if content and len(content) > 100:
        return content, "mrxwlb"

    # 4. 0645.cn
    print("mrxwlb 失败，尝试 0645.cn...")
    content = fetch_from_0645(date_str)
    if content and len(content) > 100:
        return content, "0645.cn"

    raise Exception("所有数据源均抓取失败，请检查网络或数据源可用性")

if __name__ == "__main__":
    content, source = get_xwlb_content()
    print(f"来源: {source}")
    print(content[:500])