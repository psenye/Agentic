import os
import json
import datetime

def merge_json_files_to_jsonl(results_dir, output_file):
    all_data = []
    for i in range(10):
        file_name_pattern = f"Agent_{i}_result_"
        for file_name in os.listdir(results_dir):
            if file_name.startswith(file_name_pattern) and file_name.endswith(".json"):
                with open(os.path.join(results_dir, file_name), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_data.append(data)
    with open(output_file, "w", encoding="utf-8") as out_f:
        for item in all_data:
            out_f.write(json.dumps(item, ensure_ascii=False) + "\n")


def merge(merge_json_files_to_jsonl):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"merged_results_{timestamp}.jsonl"
    merge_json_files_to_jsonl("Results", output_file)

if __name__ == "__main__":
    merge(merge_json_files_to_jsonl)