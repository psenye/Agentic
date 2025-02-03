import os
import json
from chat_with_4o import chat_with_4o as chat_function

ResultFolder = "Results"

def load_prompts(file_paths: list[str]) -> list[dict]:
    messages = []
    for prompt_path in file_paths:
        if prompt_path.endswith(".prompty"):
            with open(prompt_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                messages.append({"role": "system", "content": content})
    return messages

def load_prompts_plain(prompt: str) -> list[dict]:
    messages = []
    messages.append({"role": "system", "content": prompt})
    return messages



def load_json_strings(json_strings: list[str]) -> list[dict]:
    messages = []
    for js_str in json_strings:
        try:
            data = json.loads(js_str)
            text_content = json.dumps(data, ensure_ascii=False)
            messages.append({"role": "user", "content": text_content})
        except json.JSONDecodeError:
            pass
    return messages

def load_prompts_and_jsons(file_paths: list[str], json_strings: list[str]) -> list[dict]:
    messages = load_prompts(file_paths)
    messages.extend(load_json_strings(json_strings))
    return messages

def load_prompts_and_jsons_plain(prompt: str, json_strings: list[str]) -> list[dict]:
    messages = load_prompts_plain(prompt)
    messages.extend(load_json_strings(json_strings))
    return messages

def chat_with_prompts(file_paths: list[str], json_strings: list[str], chat_function) -> dict:
    messages = load_prompts_and_jsons(file_paths, json_strings)
    response = chat_function(messages)
    if 'message' in response and 'content' in response['message']:
        content = response['message']['content']
        try:
            start_index = content.find("```json\n") + len("```json\n")
            end_index = content.rfind("\n```")
            # 如果没有找到开始标记，则使用整个内容
            if start_index == -1 :
                start_index = 0
            else:
                if end_index == -1:
                    end_index = len(content)
            json_content = content[start_index:end_index].strip()
            json_content_dict = json.loads(json_content)
            return json_content_dict
        except json.JSONDecodeError:
            pass
    return response

def chat_with_prompts_plain(prompt: str, json_strings: list[str], chat_function) -> dict:
    messages = load_prompts_and_jsons_plain(prompt, json_strings)
    response = chat_function(messages)
    if 'message' in response and 'content' in response['message']:
        content = response['message']['content']
        try:
            start_index = content.find("```json\n") + len("```json\n")
            end_index = content.rfind("\n```")
            # 如果没有找到开始标记，则使用整个内容
            if start_index == -1 :
                start_index = 0
            else:
                if end_index == -1:
                    end_index = len(content)
            json_content = content[start_index:end_index].strip()
            json_content_dict = json.loads(json_content)
            return json_content_dict
        except json.JSONDecodeError:
            pass
    return response

def chat_with_prompts_4o(file_paths: list[str], json_strings: list[str]) -> dict:
    return chat_with_prompts(file_paths, json_strings, chat_function)

def chat_with_prompts_4o_plain(prompt: str, json_strings: list[str]) -> dict:
    return chat_with_prompts_plain(prompt, json_strings, chat_function)

if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file-paths",
        nargs="+",
        type=str,
        help="List of prompt files",
        default=["Prompts/4o-test.prompty"],
    )
    parser.add_argument(
        "--json-strings",
        type=str,
        nargs="+",
        help="JSON strings to use as prompts",
        default=[],
    )
    args = parser.parse_args()

    response = chat_with_prompts_4o(args.file_paths, args.json_strings)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file_path = os.path.join(ResultFolder, f"result_{timestamp}.txt")

    os.makedirs(ResultFolder, exist_ok=True)

    with open(result_file_path, "w", encoding="utf-8") as result_file:
        result_file.write("File Paths:\n")
        result_file.write("\n".join(args.file_paths) + "\n\n")
        result_file.write("Response:\n")
        result_file.write(json.dumps(response, ensure_ascii=False, indent=4))

    print(f"Results saved to {result_file_path}")