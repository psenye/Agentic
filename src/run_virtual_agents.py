
import argparse
import json
import os
from datetime import datetime

from generate_prompts import load_profiles_from_jsonl as load_profiles
from generate_prompts import get_prompt
from chat_with_prompts import chat_with_prompts_4o as cot_function
from chat_with_prompts import chat_with_prompts_4o_plain as cot_function_plain

ResultFolder = "Results"

def save_response(ResultFolder, response):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file_path = os.path.join(ResultFolder, f"Agent_{args.ith}_result_{timestamp}.json")

    os.makedirs(ResultFolder, exist_ok=True)

    with open(result_file_path, "w", encoding="utf-8") as result_file:
        result_file.write(json.dumps(response, ensure_ascii=False, indent=4))

    print(f"Results saved to {result_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--v_agents_file_path",
        type=str,
        help="Path to the virtual agents JSONL file",
        default="Decisions/v_agents.jsonl",
    )
    parser.add_argument(
        "--ith",
        type=int,
        help="Index of the agent to chat with",
        default=0,
    )
    parser.add_argument(
        "--partial_prompt_path",
        nargs="+",
        type=str,
        help="List of prompt files",
        default="Prompts/vagent_partial.prompty",
    )
    parser.add_argument(
        "--json-strings",
        type=str,
        nargs="+",
        help="JSON strings to use as prompts",
        default=[],
    )
    args = parser.parse_args()

    profiles = load_profiles(args.v_agents_file_path)

    if args.ith >= len(profiles):
        print(f"Index {args.ith} out of bounds")
        exit(1)


    pf = profiles[args.ith]

    prompt_template = """# 角色设定
你是一名投资者，正在填写一份关于金融投资的调查问卷。你的个人情况如下：
- 年龄：{age} 岁
- 职业 / 主要收入来源：{occupation_or_income_source}
- 年收入范围：{annual_income_range}
- 流动性需求：{liquidity_need}
- 预计投资期限：{investment_horizon}
- 风险偏好：{risk_preference}
"""

    prompt = get_prompt(args.partial_prompt_path, prompt_template, pf)

    response = cot_function_plain(prompt,[])

    save_response(ResultFolder, response)