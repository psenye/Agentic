# usage_example.py

from virtual_agent import VirtualAgent

# 假设有一个foundry_client，可以调用Azure AI Foundry LLM
foundry_client = ...  # 你自己初始化
rag_tool_instance = ...  # RAG 工具实例
web_search_tool_instance = ...  # Web搜索工具实例

# 定义 persona
persona_0 = {
    "name": "Alice",
    "age": 30,
    "incomeLevel": "中高",
    "riskPreference": "积极型投资者",
    "backgroundStory": "拥有IT行业背景，对新兴科技比较感兴趣"
}

agent_0 = VirtualAgent(
    agent_name="Agent-0",
    persona=persona_0,
    foundry_client=foundry_client,
    tools={
        "rag_tool": rag_tool_instance,
        "web_search_tool": web_search_tool_instance
    }
)

# 初始化后，可以先做 RAG 配置
agent_0.configure_agent_with_rag("中国科技行业投资信息")

# 收到一条外部问题
question = "你好，请问现在投资科技型指数基金是不是好时机？"
answer = agent_0.reply_to_message(question, do_search=True)
print("Agent-0 final answer:", answer)

# 如果有一份问卷 (dict 格式)
survey_example = {
    "questions": {
       "q1": "请简述你对当前经济形势的看法？",
       "q2": "你对股票资产的配置比例愿意达到多少？"
    }
}
survey_answers = agent_0.fill_survey(survey_example)
print("Survey answers:", survey_answers)

