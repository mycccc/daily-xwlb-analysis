import json
from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# 客户端在模块级别初始化，避免每次调用重复创建
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

def analyze_concepts_and_stocks(news_content):
    """任务2：概念识别 + 个股挖掘"""
    prompt = f"""你是一位资深A股分析师。请根据以下新闻联播内容，完成两个任务：

任务A——概念识别：分析当天新闻涉及的核心产业链概念（至少列出3个概念，注明理由）。

任务B——个股挖掘：针对每个概念，列出A股中最相关的龙头个股（含6位股票代码），并用一句话解释关联理由。如果新闻内容中有直接提及的个股，请重点标注。

新闻内容：
{news_content[:8000]}

请以JSON格式返回，结构如下：
{{
  "concepts": [
    {{"name": "概念名称", "reason": "关联理由"}}
  ],
  "stocks": [
    {{"name": "公司名称", "code": "股票代码", "concept": "所属概念", "reason": "关联理由", "directly_mentioned": true/false}}
  ]
}}"""
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    result_text = response.choices[0].message.content
    # 提取 JSON 部分（可能被 markdown 代码块包裹）
    json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    return json.loads(result_text)  # 如果直接是json

def analyze_single_stock(stock_name, stock_code):
    """任务3：对单只个股进行完整分析"""
    prompt = f"""你是一位资深A股分析师。请对 {stock_name}（{stock_code}）进行完整分析，输出格式如下：

## {stock_name}（{stock_code}）

### 第一步：新闻面
总结近一周关于该公司的3条关键新闻，判断市场情绪偏向（看涨/看跌/中性），并说明理由。

### 第二步：基本面
列出最近季度（2026Q1）的：
- 营业收入及同比变化
- EPS（每股收益）及同比变化
- 净资产收益率（ROE）

### 第三步：技术面
描述当前股价相对于50日均线及52周高点的位置，判断当前技术形态。

### 结论
基于以上信息，给出短期（1周）的操作倾向（买入/持有/观望/卖出），并简述理由。"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def analyze_all_stocks(stocks):
    """对所有个股逐一分析"""
    results = []
    for stock in stocks:
        print(f"正在分析 {stock['name']}（{stock['code']}）...")
        analysis = analyze_single_stock(stock["name"], stock["code"])
        results.append(analysis)
    return results