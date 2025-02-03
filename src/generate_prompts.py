
import argparse
import json
import os
from datetime import datetime

from chat_with_prompts import chat_with_prompts_4o as cot_function
from chat_with_prompts import chat_with_prompts_4o_plain as cot_function_plain
from virtual_agent import load_agents_from_jsonl

partial_prompt_path = "Prompts/vagent_partial.prompty"

ResultFolder = "Results"

def load_profiles_from_jsonl(path: str, foundry_client=None, tools: dict=None) -> list["dict"]:
    import json
    profiles = []
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            data = json.loads(line.strip())
            profiles.append(data)
    return profiles

def get_prompt(partial_prompt_path, prompt_template, profile):
    prompt = prompt_template.format(**profile)

    print(prompt)

    partial_prompt = open(partial_prompt_path, "r", encoding="utf-8").read()

    whole_prompt = prompt + partial_prompt
    return whole_prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--v_agents_file-path",
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
    
    args = parser.parse_args()


    prompt_template = """# 角色设定
你是一名投资者，正在填写一份关于金融投资的调查问卷。你的个人情况如下：
- 年龄：{age} 岁
- 职业 / 主要收入来源：{occupation_or_income_source}
- 年收入范围：{annual_income_range}
- 流动性需求：{liquidity_need}
- 预计投资期限：{investment_horizon}
- 风险偏好：{risk_preference}
"""
   

    profilel = load_profiles_from_jsonl(args.v_agents_file_path)

    if args.ith >= len(profilel):
        print(f"Index {args.ith} out of bounds")
        exit(1)

    profile = profilel[args.ith]

    whole_prompt = get_prompt(partial_prompt_path, prompt_template, profile)

    

    

    
    response = cot_function_plain(whole_prompt, agent_list[args.ith])