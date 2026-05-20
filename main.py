import os
import json
from datetime import datetime
from scraper import get_xwlb_content
from analyzer import analyze_concepts_and_stocks, analyze_all_stocks
from generator import generate_markdown, generate_html

def main():
    print("=" * 50)
    print(f"新闻联播自动化分析系统 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 任务1：抓取新闻联播文字稿
    print("\n[任务1] 抓取新闻联播文字稿...")
    date_str = datetime.now().strftime("%Y%m%d")
    try:
        content, source = get_xwlb_content(date_str)
        print(f"✅ 成功获取文字稿，来源: {source}，字符数: {len(content)}")
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        return

    # 任务2：DeepSeek 分析（概念识别 + 个股挖掘）
    print("\n[任务2] DeepSeek 分析中...")
    analysis_result = analyze_concepts_and_stocks(content)
    print(f"✅ 识别出 {len(analysis_result['concepts'])} 个概念, {len(analysis_result['stocks'])} 只个股")
    print(f"概念: {[c['name'] for c in analysis_result['concepts']]}")
    print(f"个股: {[s['name'] for s in analysis_result['stocks']]}")

    # 任务3：对每只个股进行完整分析
    print("\n[任务3] 个股深度分析...")
    stock_analyses = analyze_all_stocks(analysis_result["stocks"])
    print(f"✅ 完成 {len(stock_analyses)} 只个股的深度分析")

    # 任务4：生成 Markdown 和 HTML 文件
    print("\n[任务4] 生成输出文件...")
    os.makedirs("output", exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")

    md_content = generate_markdown(content, analysis_result, stock_analyses)
    md_path = f"output/{today}_xinwenlianbo.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✅ Markdown 已保存: {md_path}")

    html_content = generate_html(md_content)
    html_path = "docs/index.html"
    os.makedirs("docs", exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ HTML 已保存: {html_path}")

    print("\n" + "=" * 50)
    print("🎉 全部任务完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()