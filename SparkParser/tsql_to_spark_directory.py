import os
import json
from dotenv import load_dotenv
from tsql_to_spark import build_graph

load_dotenv()

# Configuration for Azure platform
PLATFORM_CONFIG = {
    "Azure": {
        "converter": {
            "base_url": os.getenv("AZURE_BASE_CONV_URL", "https://kian-m7ws0x3z-swedencentral.openai.azure.com/openai/deployments/gpt-4o-test/chat/completions?api-version=2024-10-21"),
            "api_key": os.getenv("AZURE_API_KEY"),
            "model": os.getenv("AZURE_BASE_CONV_MODEL", "gpt-4o-mini")
        },
        "judge": {
            "base_url": os.getenv("AZURE_BASE_JUDGE_URL", "https://kian-m7ws0x3z-swedencentral.openai.azure.com/openai/deployments/gpt-4o-test/chat/completions?api-version=2024-10-21"),
            "api_key": os.getenv("AZURE_API_KEY"),
            "model": os.getenv("AZURE_BASE_JUDGE_MODEL", "gpt-4o-mini")
        }
    }
}

# Settings
USE_RAG = False
USE_SYNTAX_CHECK = True
selected_platform = "Azure"
config = PLATFORM_CONFIG[selected_platform]

# Process JSON files
def process_json_file(file_path, graph):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        for item in data:
            if "sql" in item:
                tsql_query = item["sql"]
                initial_state = {
                    "tsql_query": tsql_query,
                    "sparksql_query": "",
                    "validation_errors": [],
                    "judge_feedback": "",
                    "syntax_feedback": "",
                    "attempt_count": 0
                }
                result = graph.invoke(initial_state)
                spark_query = result["sparksql_query"]
                if spark_query.startswith("```sql\n") and spark_query.endswith("\n```"):
                    spark_query = spark_query[6:-4].strip()
                item["spark"] = spark_query if spark_query else "none"
        
                # Save updated JSON
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                    print(f"Updated file: {file_path}")
        print(f"Processed: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def main():
    graph = build_graph()  # Use the imported build_graph function
    root_dir = "../GAC" 
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.json'):
                file_path = os.path.join(dirpath, filename)
                process_json_file(file_path, graph)

if __name__ == "__main__":
    main()