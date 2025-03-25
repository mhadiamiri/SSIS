import json
from collections import Counter
from typing import Dict, List, Set
import os
from pathlib import Path
import sys
from contextlib import redirect_stdout
from datetime import datetime

def process_executables(executables, processed_dtsids=None):
    # Initialize set of processed DTSIDs if not provided
    if processed_dtsids is None:
        processed_dtsids = set()
        
    # Use dictionaries to track unique tasks and components
    unique_tasks = {}  # DTSID -> ExecutableType
    pipeline_components = []
    
    for task in executables:
        # Skip tasks that have EventHandlers in their refId
        if 'refId' in task and ('EventHandlers' in task['refId'] or 'precedence_constraints' in task['refId']):
            continue
            
        # Get the executable type and DTSID
        if 'ExecutableType' in task and 'DTSID' in task:
            dtsid = task['DTSID']
            
            # Skip if we've already processed this DTSID
            if dtsid in processed_dtsids:
                continue
                
            processed_dtsids.add(dtsid)
            exec_type = task['ExecutableType']
            unique_tasks[dtsid] = exec_type
            
            # If it's a Pipeline task, process its components
            if exec_type == 'Microsoft.Pipeline':
                components = task.get('components', [])
                for component in components:
                    if 'componentClassID' in component:
                        pipeline_components.append(component['componentClassID'])
        
        # Process nested executables
        if 'executables' in task:
            nested_tasks, nested_components = process_executables(task['executables'], processed_dtsids)
            unique_tasks.update(nested_tasks)
            pipeline_components.extend(nested_components)
    
    return unique_tasks, pipeline_components

def analyze_ssis_package(file_path: str) -> None:
    # Read the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Process only tasks, ignore precedence_constraints
    tasks = data.get('tasks', [])
    unique_tasks, pipeline_components = process_executables(tasks)
    
    # Print package name
    package_name = Path(file_path).parent.name
    print(f"\nAnalyzing package: {package_name}")
    print("=" * 60)
    
    # Count unique tasks by ExecutableType
    print("\nUnique Task Count by ExecutableType (by DTSID, excluding EventHandlers and precedence_constraints):")
    print("-" * 60)
    task_type_counts = Counter(unique_tasks.values())
    for exec_type, count in task_type_counts.most_common():
        print(f"{exec_type}: {count}")
    
    # Count and display components by componentClassID
    if pipeline_components:
        print("\nComponent Count by componentClassID (in unique Microsoft.Pipeline tasks):")
        print("-" * 60)
        for comp_type, count in Counter(pipeline_components).most_common():
            print(f"{comp_type}: {count}")
    
    print("\n")  # Add extra newline for readability

def find_json_files(directory: str) -> List[str]:
    """Find all JSON files in the given directory and its subdirectories."""
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('_analysis.json'):
                json_files.append(os.path.join(root, file))
    return json_files

if __name__ == "__main__":
    # Base directory containing the JSON files
    base_dir = sys.argv[1]
    output_file = f"{sys.argv[2]}/summary.txt"
    
    # Find all JSON files
    json_files = find_json_files(base_dir)
    
    # Redirect stdout to the file
    with open(output_file, 'w') as f:
        with redirect_stdout(f):
            print(f"SSIS Package Analysis Summary")
            print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            
            if not json_files:
                print(f"Error: No analysis JSON files found in {base_dir}")
            else:
                # Process each JSON file
                for json_file in sorted(json_files):
                    analyze_ssis_package(json_file)
    
    print(f"Analysis complete. Results saved to: {output_file}")
