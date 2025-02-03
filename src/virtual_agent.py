# -*- coding: utf-8 -*-

"""
virtual_agent.py

定义一个“虚拟人Agent”类（Agent-0 ~ Agent-(n-1)），
其内部通过 Azure AI Foundry 的工具 (LLM, RAG, Web Search 等) 来处理请求。
"""

import json
import os
import uuid
import datetime

from chat_with_prompts import chat_with_prompts_4o as cot_function

class VirtualAgent:
    def __init__(self, 
                 agent_name: str, 
                 persona: dict,
                 foundry_client,  
                 tools: dict = None):
        """
        初始化虚拟人Agent。

        :param agent_name:   Agent名称，如 "Agent-0"
        :param persona:      虚拟人画像(dict)，包含该Agent的背景、性格、财务特征等
        :param foundry_client:  Azure AI Foundry 的客户端或上下文，用于调用 LLM/RAG/WebSearch 等
        :param tools:        可选，Agent可用的工具集合(dict)。例如 {
                                "rag_tool": foundry_rag_tool_instance,
                                "web_search_tool": foundry_web_search_tool_instance
                             }
                             也可以直接整合在 foundry_client 内。
        """
        self.agent_name = agent_name
        self.persona = persona
        self.foundry_client = foundry_client
        self.tools = tools if tools else {}

        # 初始化对话历史或其他内部状态
        self.conversation_history = []
        self.is_configured = False

    def init_persona(self, persona: dict):
        """
        重新设置/更新Agent的画像信息。
        """
        self.persona = persona
        print(f"[{self.agent_name}] Persona initialized/updated.")

    def configure_agent_with_rag(self, additional_info_query: str = None):
        """
        让Agent调用 Azure AI Foundry 中的 RAG 工具 (或类似功能) 来进行“Full Configured”，
        即在回答问题或填问卷前，基于知识库/搜索获取更多信息。
        
        :param additional_info_query: 可选，自定义的检索请求。
        """
        if "rag_tool" not in self.tools:
            print(f"[{self.agent_name}] No RAG tool available. Skipping configure.")
            return

        # 示例：调用 RAG 工具，根据 persona/需求获取背景信息
        query_text = additional_info_query or f"为角色: {self.persona} 查询所需背景资料。"
        rag_tool = self.tools["rag_tool"]

        # 通过 foundry_client 或 rag_tool 发起检索
        rag_results = rag_tool.search(query_text, top_k=5)  
        # rag_tool.search(...) 为示例方法，需要你在实际中实现

        # 这里可以将检索到的资料整合到Agent的内部知识库中
        # 在实际场景下可能将 rag_results 存到 self.conversation_history 或一个 internal_context
        self.conversation_history.append({
            "role": "system",
            "content": f"RAG results for agent: {rag_results}"
        })

        self.is_configured = True
        print(f"[{self.agent_name}] Agent configured with RAG data.")

    def web_search_if_needed(self, query: str):
        """
        如果需要最新/实时信息，可调用 Web 搜索。
        """
        if "web_search_tool" not in self.tools:
            print(f"[{self.agent_name}] No web search tool available.")
            return None
        
        web_tool = self.tools["web_search_tool"]
        search_results = web_tool.search_web(query=query, count=3)
        # 同样这里 search_web(...) 为示例方法，需要结合 Azure AI Foundry 或 Bing API 实现
        
        return search_results

    def receive_message(self, message: str):
        """
        模拟从外部接收到一条问询消息（可来自用户、问卷或其他Agent）。
        这里记录到对话历史中，等待回答。
        """
        self.conversation_history.append({"role": "user", "content": message})
        print(f"[{self.agent_name}] Received message: {message}")

    def generate_answer(self, temperature=0.7) -> str:
        """
        利用 Azure AI Foundry 提供的 LLM 生成回答（对话/答案）。
        将 persona、对话历史、RAG或搜索得到的上下文融合成 Prompt 调用大模型。
        """
        # 组合一个系统提示或 context
        system_prompt = (
            f"你现在是一个虚拟人Agent，名叫 {self.agent_name}。"
            f"你的人设信息：{self.persona}. "
            "请根据以下对话历史、检索资料与角色设定来回答问题："
        )

        # 收集已有对话
        conversation_text = ""
        for turn in self.conversation_history:
            role = turn["role"]
            content = turn["content"]
            conversation_text += f"{role.upper()}: {content}\n"

        # 构造API请求——此处仅为示例，可根据实际的foundry_client做调用
        prompt = system_prompt + "\n对话历史如下：\n" + conversation_text
        
        # 调用 Azure AI Foundry 的大模型推理
        # 具体做法取决于 foundry_client 的API，比如:
        llm_response = self.foundry_client.invoke_llm(
            prompt=prompt,
            temperature=temperature
        )
        # 这里的 foundry_client.invoke_llm(...) 为示例，需要你在实际中实现

        answer_text = llm_response.get("text", "")  # 视具体返回格式而定
        print(f"[{self.agent_name}] Generated answer: {answer_text}")
        return answer_text

    def reply_to_message(self, message: str, do_search=False):
        """
        高层API：接收外部消息 -> 视需要调用search/RAG -> 生成回答 -> 返回给外部。
        """
        # 先将消息存入对话历史
        self.receive_message(message)

        # 如果需要搜索最新信息，可以调用
        if do_search:
            search_results = self.web_search_if_needed(message)
            if search_results:
                # 将搜索结果写入对话历史，提供上下文
                self.conversation_history.append({
                    "role": "system",
                    "content": f"Web Search Results: {search_results}"
                })

        # 最后生成回答
        answer = self.generate_answer()
        # 将回答也存到对话历史
        self.conversation_history.append({"role": "assistant", "content": answer})
        return answer

    def fill_survey(self, survey: dict):
        """
        让Agent自动填写传入的问卷。 
        :param survey: 一个包含问题结构的 dict (或你自定义的问卷对象)
        :return: 一个 dict，代表填写后的答案
        """
        if not self.is_configured:
            # 如果尚未做RAG配置，也可在此处强制执行
            self.configure_agent_with_rag("获取中国金融市场问卷回答所需信息")

        answers = {}
        # 简化处理：对每个问题把 question 传到 generate_answer 
        # (也可以一次性拼大prompt回答整份问卷)
        if "questions" in survey:
            for q_id, question_content in survey["questions"].items():
                # 这里做一个简单对话
                self.receive_message(f"问卷问题: {question_content}")
                answer = self.generate_answer(temperature=0.5)
                answers[q_id] = answer
                # 记录到对话历史
                self.conversation_history.append(
                    {"role": "assistant", "content": f"Answer for {q_id}: {answer}"}
                )

        return answers

    def get_agent_state(self):
        """
        返回Agent当前的内部状态，用于调试或外部监控。
        """
        return {
            "agent_name": self.agent_name,
            "persona": self.persona,
            "conversation_history": self.conversation_history,
            "configured": self.is_configured
        }

    def __repr__(self):
        return f"<VirtualAgent name={self.agent_name}, configured={self.is_configured}>"
    
    def cot_with_prompt(self, file_paths, question: str):
        """
        通过 Chain of Thought (CoT) 的方式来回答问题。
        """
        # 先将问题存入对话历史
        self.receive_message(question)

        # 调用 CoT 函数
        answer = cot_function(
            file_paths,
            json_strings=[question]
        )

        # 将回答也存到对话历史
        self.conversation_history.append({"role": "assistant", "content": answer})
        return answer

    def cot(self, question: str):
        """
        通过 Chain of Thought (CoT) 的方式来回答问题。
        """
        # 先将问题存入对话历史
        self.receive_message(question)

        # 调用 CoT 函数
        answer = cot_function(
            file_paths=["Prompts/4o-test.prompty"],
            json_strings=[question]
        )

        # 将回答也存到对话历史
        self.conversation_history.append({"role": "assistant", "content": answer})
        return answer
    
def test():
    # 示例：创建一个虚拟人Agent
    agent = VirtualAgent(
        agent_name="Agent-0",
        persona={
            "name": "Alice",
            "age": 30,
            "occupation": "Financial Analyst",
            "traits": ["analytical", "detail-oriented"]
        },
        foundry_client=None,  # 这里需要传入实际的 Foundry 客户端
        tools={
            "rag_tool": None,  # 这里需要传入实际的 RAG 工具实例
            "web_search_tool": None  # 这里需要传入实际的 Web 搜索工具实例
        }
    )

    # 配置 Agent
    agent.configure_agent_with_rag()

    # 模拟接收消息
    agent.receive_message("请问中国金融市场的最新动态如何？")

    # 生成回答
    answer = agent.generate_answer()
    print(f"Answer: {answer}")

    # 自动填写问卷
    survey = {
        "questions": {
            "q1": "你对中国金融市场的看法是什么？",
            "q2": "你认为未来的发展趋势如何？"
        }
    }
    answers = agent.fill_survey(survey)
    print(f"Survey Answers: {answers}")

def load_agents_from_jsonl(path: str, foundry_client=None, tools: dict=None) -> list["VirtualAgent"]:
    import json
    agents = []
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            data = json.loads(line.strip())
            agent_name = f"Agent-{idx}"
            agent = VirtualAgent(agent_name, data, foundry_client, tools)
            agents.append(agent)
    return agents

def save_response(ResultFolder, args, response):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file_path = os.path.join(ResultFolder, f"Agent_result_{timestamp}.txt")

    os.makedirs(ResultFolder, exist_ok=True)

    with open(result_file_path, "w", encoding="utf-8") as result_file:
        result_file.write("File Paths:\n")
        result_file.write("\n".join(args.file_paths) + "\n\n")
        result_file.write("Response:\n")
        result_file.write(json.dumps(response, ensure_ascii=False, indent=4))

    print(f"Results saved to {result_file_path}")

if __name__ == "__main__":
    from chat_with_prompts import chat_with_prompts_4o as cot_function
    import argparse
    from datetime import datetime

    ResultFolder = "Results"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file-paths",
        nargs="+",
        type=str,
        help="List of prompt files",
        default=["Prompts/survey_generator_2.prompty"],
    )
    parser.add_argument(
        "--json-strings",
        type=str,
        nargs="+",
        help="JSON strings to use as prompts",
        default=[],
    )
    args = parser.parse_args()
    response = cot_function(args.file_paths, args.json_strings)
    save_response(ResultFolder, args, response)


