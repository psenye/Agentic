import json

def render_html_from_json(json_data):
    """
    根据问卷的 JSON 数据生成 HTML 字符串
    """
    investor_info = json_data.get("investor_basic_info", {})
    market_sentiment = json_data.get("market_sentiment", {})
    return_and_risk = json_data.get("return_and_risk", {})
    investment_pref = json_data.get("investment_preference", {})
    risk_events = json_data.get("risk_events", {})
    notes = json_data.get("additional_notes", "")

    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8" />
    <title>Financial Survey 结果</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        h1, h2, h3 {{
            color: #2F4F4F;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section-title {{
            font-size: 20px;
            margin-bottom: 10px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }}
        .item {{
            margin: 5px 0;
        }}
        .label {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>Financial Survey 结果报告</h1>

    <!-- 第一部分：投资者基本信息 -->
    <div class="section">
        <div class="section-title">1. 投资者基本信息</div>
        <div class="item"><span class="label">年龄：</span>{investor_info.get("age", "")}</div>
        <div class="item"><span class="label">职业 / 主要收入来源：</span>{investor_info.get("occupation_or_income_source", "")}</div>
        <div class="item"><span class="label">年收入范围：</span>{investor_info.get("annual_income_range", "")}</div>
        <div class="item"><span class="label">流动性需求：</span>{investor_info.get("liquidity_need", "")}</div>
        <div class="item"><span class="label">投资期限：</span>{investor_info.get("investment_horizon", "")}</div>
        <div class="item"><span class="label">风险偏好等级：</span>{investor_info.get("risk_preference", "")}</div>
    </div>

    <!-- 第二部分：市场情绪及预期 -->
    <div class="section">
        <div class="section-title">2. 市场情绪及预期</div>
        <div class="item"><span class="label">未来 6~12 个月整体经济形势：</span>{market_sentiment.get("economic_outlook_6_12_months", "")}</div>
        <div class="item"><span class="label">理由：</span>{market_sentiment.get("economic_outlook_reason", "")}</div>
        <div class="item"><span class="label">利率环境预期：</span>{market_sentiment.get("interest_rate_expectation", "")}</div>
        <div class="item"><span class="label">理由：</span>{market_sentiment.get("interest_rate_reason", "")}</div>
        <div class="item"><span class="label">通胀水平预期：</span>{market_sentiment.get("inflation_expectation", "")}</div>
        <div class="item"><span class="label">理由：</span>{market_sentiment.get("inflation_reason", "")}</div>

        <!-- 对不同资产类别的涨跌判断 -->
        <div class="item"><span class="label">资产类别预期：</span></div>
        <ul>
            <li><span class="label">股票市场：</span>{market_sentiment.get("asset_class_expectations", {}).get("stocks", "")}</li>
            <li><span class="label">债券市场：</span>{market_sentiment.get("asset_class_expectations", {}).get("bonds", "")}</li>
            <li><span class="label">房地产市场：</span>{market_sentiment.get("asset_class_expectations", {}).get("real_estate", "")}</li>
            <li><span class="label">商品市场：</span>{market_sentiment.get("asset_class_expectations", {}).get("commodities", "")}</li>
        </ul>
    </div>

    <!-- 第三部分：收益期望与风险容忍度 -->
    <div class="section">
        <div class="section-title">3. 收益期望与风险容忍度</div>
        <div class="item"><span class="label">年化收益率目标：</span>{return_and_risk.get("annual_return_target", "")}</div>
        <div class="item"><span class="label">最大可容忍的回撤幅度：</span>{return_and_risk.get("max_drawdown_tolerance", "")}</div>
        <div class="item"><span class="label">对亏损的心理承受度：</span>{return_and_risk.get("loss_tolerance_behaviour", "")}</div>
    </div>

    <!-- 第四部分：投资策略偏好 -->
    <div class="section">
        <div class="section-title">4. 投资策略偏好</div>
        <div class="item"><span class="label">股票类资产配置比例：</span>{investment_pref.get("preferred_asset_allocation", {}).get("stocks_ratio", "")}%</div>
        <div class="item"><span class="label">固定收益资产配置比例：</span>{investment_pref.get("preferred_asset_allocation", {}).get("bonds_ratio", "")}%</div>
        <div class="item"><span class="label">另类资产配置比例：</span>{investment_pref.get("preferred_asset_allocation", {}).get("alternative_ratio", "")}%</div>
        <div class="item"><span class="label">其他资产配置比例：</span>{investment_pref.get("preferred_asset_allocation", {}).get("other_ratio", "")}%</div>
        <div class="item"><span class="label">ESG / 主题投资偏好：</span>{investment_pref.get("esg_preference", "")}</div>

        <div class="item"><span class="label">常用投资工具：</span></div>
        <ul>
            {"".join([f"<li>{tool}</li>" for tool in investment_pref.get("common_investment_tools", [])])}
        </ul>
    </div>

    <!-- 第五部分：对当前及潜在风险事件的关注度 -->
    <div class="section">
        <div class="section-title">5. 风险事件关注度</div>
        <div class="item"><span class="label">主要关注的风险事件：</span></div>
        <ul>
            {"".join([f"<li>{event}</li>" for event in risk_events.get("main_concerns", [])])}
        </ul>
        <div class="item"><span class="label">风险事件发生概率评估：</span></div>
        <ul>
        {"".join([
            f"<li><strong>事件：</strong>{re.get('risk_event', '')}；"
            f" <strong>短期：</strong>{re.get('short_term_probability', '')}；"
            f" <strong>中期：</strong>{re.get('mid_term_probability', '')}</li>"
            for re in risk_events.get("risk_occurrence_probability", [])
        ])}
        </ul>
    </div>

    <!-- 其他补充说明 -->
    <div class="section">
        <div class="section-title">6. 其他补充说明</div>
        <div class="item">{notes}</div>
    </div>

</body>
</html>
    """

    return html_content


if __name__ == "__main__":
    # 假设问卷答案存储在 survey_data.json 文件中
    with open("example1.json", "r", encoding="utf-8") as f:
        survey_data = json.load(f)
    
    # 调用函数生成 HTML
    html_result = render_html_from_json(survey_data)

    # 输出或保存到文件
    with open("survey_result.html", "w", encoding="utf-8") as f:
        f.write(html_result)

    print("HTML 文件已生成：survey_result.html")
