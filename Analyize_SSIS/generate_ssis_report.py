import json
from pathlib import Path
import statistics
import os
import sys
from glob import glob


def calculate_total_tasks(task_types):
    """Calculate total tasks from task types dictionary."""
    return sum(task_types.values())

def get_sql_files_by_package(etl_output_dir):
    """Get all SQL files organized by package."""
    sql_files = {}
    
    for root, dirs, files in os.walk(etl_output_dir):
        for file in files:
            if file.endswith('.sql'):
                # Get the package name from the path
                path_parts = Path(root).parts
                if 'SQL_Scripts' in path_parts:
                    package_idx = path_parts.index('SQL_Scripts') - 1
                    if package_idx >= 0:
                        package_name = path_parts[package_idx]
                        if package_name not in sql_files:
                            sql_files[package_name] = []
                        sql_files[package_name].append({
                            'name': file,
                            'path': os.path.join(root, file)
                        })
    
    return sql_files

def generate_ssis_report(input_json, output_md, etl_output_dir, report_title):
    """Generate SSIS analysis report in Markdown format from JSON data."""
    
    # Read JSON data
    with open(input_json, 'r') as f:
        data = json.load(f)
    
    # Calculate metrics
    total_packages = data['total_packages']
    total_tasks = calculate_total_tasks(data['task_types'])
    avg_tasks_per_package = total_tasks / total_packages if total_packages > 0 else 0
    
    # Generate report content
    report = []
    
    # Header with custom title
    report.append(f"# SSIS Packages Analysis Report for {report_title}\n")
    
    # Section 1: Summary
    report.append("## 1. Summary\n")
    report.append("### Overall Statistics")
    report.append(f"- Total Number of Packages: {total_packages:,}")
    report.append(f"- Total Number of Tasks: {total_tasks:,}")
    report.append(f"- Average Tasks per Package: {avg_tasks_per_package:.1f}\n")
    
    # Tasks by Type
    report.append("### Tasks by Type")
    for task_type, count in data['task_types'].items():
        # Remove "Microsoft." prefix and replace Pipeline with Data Flow task
        task_name = task_type.replace("Microsoft.", "")
        if task_type == "Microsoft.Pipeline":
            task_name = "Data Flow task"
        report.append(f"- {task_name}: {count:,}")
    report.append("")
    
    # Section 2: Package Details
    report.append("## 2. Package Details\n")
    
    # Package Details Table
    report.append("### Task Count by Package\n")
    report.append("| Package Name | Total Tasks | Data Flow | Execute SQL | Expression | Sequence | Execute Package | Other Tasks |")
    report.append("|--------------|-------------|------------|-------------|------------|-----------|----------------|-------------|")
    
    for package in data['packages']:
        task_counts = package.get('task_type_counts', {})
        
        # Get counts for each task type, defaulting to 0 if not present
        data_flow = task_counts.get('Microsoft.Pipeline', 0)
        execute_sql = task_counts.get('Microsoft.ExecuteSQLTask', 0)
        expression = task_counts.get('Microsoft.ExpressionTask', 0)
        sequence = task_counts.get('STOCK:SEQUENCE', 0)
        execute_package = task_counts.get('Microsoft.ExecutePackageTask', 0)
        
        # Calculate other tasks
        main_task_count = data_flow + execute_sql + expression + sequence + execute_package
        other_tasks = package['task_count'] - main_task_count
        
        report.append(
            f"| {package['name']} | {package['task_count']} | "
            f"{data_flow} | {execute_sql} | {expression} | {sequence} | "
            f"{execute_package} | {other_tasks} |"
        )
    report.append("")
    
 
    file_name = report_title.replace(' ', '_').lower()
    file_path = os.path.join(output_md, f'{file_name}.md')
    print(file_path)
    # Write to file
    with open(file_path, 'w') as f:
        f.write('\n'.join(report))


    # Appendix Section with SQL Queries
    
    
    # Get all SQL files organized by package
    sql_files = get_sql_files_by_package(etl_output_dir)
    
    # Add each package's SQL queries
    for package_name, files in sorted(sql_files.items()):
        report = []
        report.append(f"### {package_name}\n")
        
        for i, sql_file in enumerate(sorted(files, key=lambda x: x['name']), 1):
            # Read SQL content
            with open(sql_file['path'], 'r') as f:
                sql_content = f.read().strip()
            
            report.append(f"{i}. **{sql_file['name']}**\n")
            report.append("```sql")
            report.append(sql_content)
            report.append("```\n")
        abs_sql_output = os.path.join(output_md, "SQL_mds", f'{file_name}.md')
        os.makedirs(abs_sql_output, exist_ok=True)
        sql_output_file = os.path.join(abs_sql_output, f'SQL_Scripts_{package_name}.md')
        
        # Write to file
        with open(sql_output_file, 'w') as f:
            f.write('\n'.join(report))
        
    

def main():
    # Define input and output paths
    current_dir = Path(__file__).parent
    analysis_dir = sys.argv[1]
    summary_dir = sys.argv[2]
    report_title = sys.argv[3]

    input_json = glob(f"{analysis_dir}/*.json")[0]
    
    # # Generate report
    generate_ssis_report(input_json, summary_dir, analysis_dir, report_title)
    print(f"Report generated successfully at: {summary_dir}")

if __name__ == "__main__":
    main()
