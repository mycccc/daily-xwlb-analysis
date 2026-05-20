from datetime import datetime
import json

def generate_markdown(content, analysis, stock_analyses):
    """生成完整的 Markdown 文件"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    md = f"""# {today} 新闻联播分析报告

> 自动生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 数据来源：新闻联播

---

## 📰 新闻联播全文内容

{content}

---

## 🔍 核心概念识别

"""
    for i, concept in enumerate(analysis["concepts"], 1):
        md += f"### {i}. {concept['name']}\n"
        md += f"**关联理由**：{concept['reason']}\n\n"
    
    md += "---\n\n## 📈 相关龙头个股\n\n"
    md += "| 公司名称 | 股票代码 | 所属概念 | 关联理由 | 是否直接提及 |\n"
    md += "|----------|----------|----------|----------|------------|\n"
    
    for stock in analysis["stocks"]:
        directly = "⚠️ 新闻直接提及" if stock.get("directly_mentioned") else "概念关联"
        md += f"| {stock['name']} | {stock['code']} | {stock['concept']} | {stock['reason']} | {directly} |\n"
    
    md += "\n---\n\n## 🔬 个股深度分析\n\n"
    
    for i, analysis_text in enumerate(stock_analyses):
        md += analysis_text + "\n\n---\n\n"
    
    md += f"\n## ⚠️ 免责声明\n\n"
    md += "本报告由AI自动生成，仅供参考，不构成投资建议。股市有风险，投资需谨慎。\n"
    md += f"数据来源：新闻联播官方内容 | 分析模型：DeepSeek | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return md

def generate_html(md_content):
    """将 Markdown 转为 HTML（使用简单的 HTML 模板）"""
    # 这里简化处理，实际可使用 Python-Markdown 库
    # pip install markdown
    try:
        import markdown
        html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    except ImportError:
        html_body = f"<pre>{md_content}</pre>"
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>新闻联播分析报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.8; color: #333; }}
        h1 {{ color: #c00; border-bottom: 3px solid #c00; padding-bottom: 10px; }}
        h2 {{ color: #333; border-left: 4px solid #c00; padding-left: 12px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #f5f5f5; }}
        tr:hover {{ background-color: #fafafa; }}
        blockquote {{ background: #f9f9f9; border-left: 4px solid #ccc; padding: 10px 15px; margin: 10px 0; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""
    return html