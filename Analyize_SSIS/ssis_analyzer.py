import xml.etree.ElementTree as ET
import json
import os
import glob
from typing import Dict, List, Any

class SSISAnalyzer:
    def __init__(self):
        self.ns = {
            'DTS': 'www.microsoft.com/SqlServer/Dts',
            'SQLTask': 'www.microsoft.com/sqlserver/dts/tasks/sqltask',
            'pipeline': 'www.microsoft.com/sqlserver/dts/tasks/pipeline'
        }
        
        # Create case-insensitive versions of namespaces
        self.ns_lower = {k: v.lower() for k, v in self.ns.items()}
    
    def generate_mermaid_diagram(self, analysis: Dict[str, Any]) -> str:
        """Generate a Mermaid diagram for an SSIS package."""
        diagram = ["```mermaid", "graph TD"]
        
        # Package info
        pkg_name = analysis['package_info'].get('ObjectName', 'Unknown Package')
        diagram.append(f"    subgraph {pkg_name}")
        
        # Connection Managers
        if analysis['connection_managers']:
            diagram.append("    subgraph Connections")
            for i, conn in enumerate(analysis['connection_managers']):
                conn_id = f"conn{i}"
                conn_name = conn.get('ObjectName', 'Unknown')
                conn_type = conn.get('CreationName', '')
                diagram.append(f"        {conn_id}[{conn_name}<br/>{conn_type}]")
            diagram.append("    end")
        
        # Tasks and their relationships
        task_ids = {}  # Store task IDs for precedence constraints
        for i, task in enumerate(analysis['tasks']):
            task_id = f"task{i}"
            task_ids[task.get('refId', '')] = task_id
            
            task_name = task.get('ObjectName', 'Unknown Task')
            task_type = task.get('CreationName', '')
            
            # Add task details
            if task_type == 'Microsoft.ExecuteSQLTask':
                sql_task = task.get('sqlTask', {})
                sql_stmt = sql_task.get('SqlStatement', '').replace('\n', '<br/>')
                if len(sql_stmt) > 50:
                    sql_stmt = sql_stmt[:47] + '...'
                diagram.append(f"        {task_id}[{task_name}<br/>{task_type}<br/>{sql_stmt}]")
            elif task_type == 'Microsoft.Pipeline':
                diagram.append(f"        {task_id}[{task_name}<br/>{task_type}]")
                
                # Add data flow components if present
                if 'components' in task:
                    diagram.append(f"        subgraph {task_name}_flow")
                    comp_ids = {}
                    for j, comp in enumerate(task['components']):
                        comp_id = f"comp{i}_{j}"
                        comp_ids[comp.get('refId', '')] = comp_id
                        comp_name = comp.get('name', 'Unknown Component')
                        comp_type = comp.get('componentClassID', '')
                        diagram.append(f"            {comp_id}[{comp_name}<br/>{comp_type}]")
                    
                    # Add component connections from paths
                    if 'paths' in task:
                        for path in task['paths']:
                            start_id = comp_ids.get(path.get('startId', ''))
                            end_id = comp_ids.get(path.get('endId', ''))
                            if start_id and end_id:
                                diagram.append(f"            {start_id} --> {end_id}")
                    
                    diagram.append("        end")
            else:
                diagram.append(f"        {task_id}[{task_name}<br/>{task_type}]")
        
        # Add precedence constraints
        for constraint in analysis['precedence_constraints']:
            from_task = constraint.get('From', '').split('\\')[-1]
            to_task = constraint.get('To', '').split('\\')[-1]
            
            from_id = None
            to_id = None
            
            # Find matching task IDs
            for task_ref, task_id in task_ids.items():
                if from_task in task_ref:
                    from_id = task_id
                if to_task in task_ref:
                    to_id = task_id
            
            if from_id and to_id:
                diagram.append(f"        {from_id} --> {to_id}")
        
        diagram.append("    end")
        
        # Add styling
        diagram.extend([
            "    classDef connection fill:#f9f,stroke:#333,stroke-width:2px;",
            "    classDef task fill:#bbf,stroke:#333,stroke-width:2px;",
            "    classDef component fill:#bfb,stroke:#333,stroke-width:2px;",
            "    class conn0,conn1,conn2,conn3,conn4,conn5 connection;",
            "    class task0,task1,task2,task3,task4,task5 task;",
            "    class comp0_0,comp0_1,comp0_2,comp0_3,comp0_4 component;"
        ])
        
        diagram.append("```")
        return "\n".join(diagram)
    
    def count_tasks_by_type(self, tasks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count the number of tasks by their CreationName."""
        task_type_counts = {}
        for task in tasks:
            task_type = task.get('CreationName', 'Unknown')
            task_type_counts[task_type] = task_type_counts.get(task_type, 0) + 1
        return task_type_counts
    
    def extract_attributes(self, element: ET.Element) -> Dict[str, str]:
        """Extract all DTS attributes from an element."""
        attrs = {}
        for k, v in element.attrib.items():
            if k.startswith('{'):
                ns, attr = k[1:].split('}')
                if ns in [self.ns['DTS'], self.ns['SQLTask']]:
                    attrs[attr] = v
            else:
                attrs[k] = v
        return attrs
    
    def parse_connection_managers(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Parse connection managers from SSIS package."""
        connections = []
        for conn in root.findall('.//DTS:ConnectionManager', self.ns):
            conn_info = self.extract_attributes(conn)
            
            # Get connection details from ObjectData
            obj_data = conn.find('.//DTS:ObjectData/DTS:ConnectionManager', self.ns)
            if obj_data is not None:
                conn_info.update(self.extract_attributes(obj_data))
                
                # Extract connection string
                conn_str = obj_data.get('DTS:ConnectionString')
                if conn_str:
                    conn_info['ConnectionString'] = conn_str
                
                # Extract flat file columns if present
                flat_file_cols = []
                for col in obj_data.findall('.//DTS:FlatFileColumn', self.ns):
                    col_info = self.extract_attributes(col)
                    flat_file_cols.append(col_info)
                if flat_file_cols:
                    conn_info['FlatFileColumns'] = flat_file_cols
            
            connections.append(conn_info)
        return connections
    
    def parse_sql_task(self, task: ET.Element) -> Dict[str, Any]:
        """Parse SQL Task specific information."""
        sql_info = {}
        
        # Find SQL Task data
        sql_task = task.find('.//SQLTask:SqlTaskData', self.ns)
        if sql_task is not None:
            sql_info.update(self.extract_attributes(sql_task))
            
            # Extract SQL statement
            sql_stmt = sql_task.get('SQLTask:SqlStatementSource')
            if sql_stmt:
                sql_info['SqlStatement'] = sql_stmt
            
            # Extract connection reference
            conn_ref = sql_task.get('SQLTask:Connection')
            if conn_ref:
                sql_info['ConnectionReference'] = conn_ref
        
        return sql_info
    
    def parse_components(self, pipeline: ET.Element) -> List[Dict[str, Any]]:
        """Parse components from a data flow task."""
        components = []
        for comp in pipeline.findall('.//component', {}):
            comp_info = {
                'refId': comp.get('refId', ''),
                'componentClassID': comp.get('componentClassID', ''),
                'name': comp.get('name', ''),
                'description': comp.get('description', ''),
                'properties': [],
                'inputs': [],
                'outputs': []
            }
            
            # Parse component properties
            for prop in comp.findall('.//property', {}):
                prop_info = {
                    'name': prop.get('name', ''),
                    'dataType': prop.get('dataType', ''),
                    'value': prop.text if prop.text else ''
                }
                comp_info['properties'].append(prop_info)
            
            # Parse inputs
            for inp in comp.findall('.//input', {}):
                input_info = {
                    'refId': inp.get('refId', ''),
                    'name': inp.get('name', ''),
                    'errorRowDisposition': inp.get('errorRowDisposition', ''),
                    'errorOrTruncationOperation': inp.get('errorOrTruncationOperation', ''),
                    'columns': []
                }
                
                # Input columns
                for col in inp.findall('.//inputColumn', {}):
                    input_info['columns'].append({
                        'refId': col.get('refId', ''),
                        'name': col.get('name', ''),
                        'dataType': col.get('dataType', ''),
                        'length': col.get('length', ''),
                        'precision': col.get('precision', ''),
                        'scale': col.get('scale', '')
                    })
                
                comp_info['inputs'].append(input_info)
            
            # Parse outputs
            for out in comp.findall('.//output', {}):
                output_info = {
                    'refId': out.get('refId', ''),
                    'name': out.get('name', ''),
                    'isErrorOut': out.get('isErrorOut', ''),
                    'columns': []
                }
                
                # Output columns
                for col in out.findall('.//outputColumn', {}):
                    output_info['columns'].append({
                        'refId': col.get('refId', ''),
                        'name': col.get('name', ''),
                        'dataType': col.get('dataType', ''),
                        'length': col.get('length', ''),
                        'precision': col.get('precision', ''),
                        'scale': col.get('scale', '')
                    })
                
                comp_info['outputs'].append(output_info)
            
            components.append(comp_info)
        return components
    
    def parse_tasks(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Parse all tasks in the package, maintaining their hierarchy."""
        tasks = []
        for executable in root.findall('.//DTS:Executable', self.ns):
            task = self.extract_attributes(executable)
            
            # Handle Data Flow Task components
            if task.get('CreationName') == 'Microsoft.Pipeline':
                pipeline = executable.find('.//pipeline', self.ns)
                if pipeline is not None:
                    components = []
                    for component in pipeline.findall('.//component', self.ns):
                        comp_info = self.extract_attributes(component)
                        
                        # Extract inputs
                        inputs = []
                        for input_elem in component.findall('.//inputs/input', self.ns):
                            input_info = self.extract_attributes(input_elem)
                            input_info['columns'] = []
                            for col in input_elem.findall('.//inputColumn', self.ns):
                                col_info = self.extract_attributes(col)
                                input_info['columns'].append(col_info)
                            inputs.append(input_info)
                        comp_info['inputs'] = inputs
                        
                        # Extract outputs
                        outputs = []
                        for output_elem in component.findall('.//outputs/output', self.ns):
                            output_info = self.extract_attributes(output_elem)
                            output_info['columns'] = []
                            for col in output_elem.findall('.//outputColumn', self.ns):
                                col_info = self.extract_attributes(col)
                                output_info['columns'].append(col_info)
                            outputs.append(output_info)
                        comp_info['outputs'] = outputs
                        
                        components.append(comp_info)
                    
                    # Extract data flow paths
                    paths = []
                    for path in pipeline.findall('.//path', self.ns):
                        path_info = self.extract_attributes(path)
                        paths.append(path_info)
                    
                    task['components'] = components
                    task['paths'] = paths
            
            # Handle SQL Task
            elif task.get('CreationName') == 'Microsoft.ExecuteSQLTask':
                sql_data = executable.find('.//SQLTask:SqlTaskData', self.ns)
                if sql_data is not None:
                    task['sqlTask'] = self.extract_attributes(sql_data)
            
            # Handle nested executables (sequence containers)
            nested_executables = executable.findall('./DTS:Executables/DTS:Executable', self.ns)
            if nested_executables:
                task['executables'] = []
                for nested in nested_executables:
                    nested_task = self.extract_attributes(nested)
                    
                    # Recursively parse nested components
                    if nested_task.get('CreationName') == 'Microsoft.Pipeline':
                        pipeline = nested.find('.//pipeline', self.ns)
                        if pipeline is not None:
                            components = []
                            for component in pipeline.findall('.//component', self.ns):
                                comp_info = self.extract_attributes(component)
                                
                                # Extract inputs
                                inputs = []
                                for input_elem in component.findall('.//inputs/input', self.ns):
                                    input_info = self.extract_attributes(input_elem)
                                    input_info['columns'] = []
                                    for col in input_elem.findall('.//inputColumn', self.ns):
                                        col_info = self.extract_attributes(col)
                                        input_info['columns'].append(col_info)
                                    inputs.append(input_info)
                                comp_info['inputs'] = inputs
                                
                                # Extract outputs
                                outputs = []
                                for output_elem in component.findall('.//outputs/output', self.ns):
                                    output_info = self.extract_attributes(output_elem)
                                    output_info['columns'] = []
                                    for col in output_elem.findall('.//outputColumn', self.ns):
                                        col_info = self.extract_attributes(col)
                                        output_info['columns'].append(col_info)
                                    outputs.append(output_info)
                                comp_info['outputs'] = outputs
                                
                                components.append(comp_info)
                            
                            # Extract data flow paths
                            paths = []
                            for path in pipeline.findall('.//path', self.ns):
                                path_info = self.extract_attributes(path)
                                paths.append(path_info)
                            
                            nested_task['components'] = components
                            nested_task['paths'] = paths
                    
                    # Handle nested SQL Task
                    elif nested_task.get('CreationName') == 'Microsoft.ExecuteSQLTask':
                        sql_data = nested.find('.//SQLTask:SqlTaskData', self.ns)
                        if sql_data is not None:
                            nested_task['sqlTask'] = self.extract_attributes(sql_data)
                    
                    task['executables'].append(nested_task)
                
                # Parse precedence constraints for sequence containers
                constraints = executable.findall('./DTS:PrecedenceConstraints/DTS:PrecedenceConstraint', self.ns)
                if constraints:
                    task['precedence_constraints'] = []
                    for constraint in constraints:
                        constraint_info = self.extract_attributes(constraint)
                        task['precedence_constraints'].append(constraint_info)
            
            tasks.append(task)
        
        return tasks
    
    def parse_precedence_constraints(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Parse precedence constraints between tasks."""
        constraints = []
        for constraint in root.findall('.//DTS:PrecedenceConstraint', self.ns):
            constraint_info = self.extract_attributes(constraint)
            constraints.append(constraint_info)
        return constraints
    
    def extract_sql_from_component(self, component: ET.Element, df_name: str, output_dir: str) -> None:
        """Extract SQL from Data Flow components."""
        comp_name = component.get('name', 'UnknownComponent')
        comp_type = component.get('componentClassID', '')
        print(f"\nDebug: Processing component {comp_name} of type {comp_type}")
        
        # Handle OLEDB Source
        if 'Microsoft.OLEDBSource' in comp_type:
            # Look for objectData/properties
            obj_data = component.find('objectData')
            if obj_data is not None:
                print("Debug: Found objectData")
                properties = obj_data.findall('.//properties/property')
                for prop in properties:
                    name = prop.get('name', '')
                    print(f"Debug: Found property: {name}")
                    if name in ['SqlCommand', 'OpenRowset']:
                        sql_cmd = prop.text
                        if sql_cmd and sql_cmd.strip():
                            sql_file_path = os.path.join(output_dir, f"{df_name}_{comp_name}_OLEDBSource.sql")
                            os.makedirs(os.path.dirname(sql_file_path), exist_ok=True)
                            with open(sql_file_path, 'w', encoding='utf-8') as f:
                                f.write(sql_cmd)
                            print(f"Extracted SQL from OLEDB Source '{comp_name}' in '{df_name}'")

            # Try component properties
            properties = component.findall('properties/property')
            for prop in properties:
                name = prop.get('name', '')
                print(f"Debug: Found direct property: {name}")
                if name in ['SqlCommand', 'OpenRowset']:
                    sql_cmd = prop.text
                    if sql_cmd and sql_cmd.strip():
                        sql_file_path = os.path.join(output_dir, f"{df_name}_{comp_name}_OLEDBSource.sql")
                        os.makedirs(os.path.dirname(sql_file_path), exist_ok=True)
                        with open(sql_file_path, 'w', encoding='utf-8') as f:
                            f.write(sql_cmd)
                        print(f"Extracted SQL from OLEDB Source '{comp_name}' in '{df_name}'")

    def extract_sql_queries(self, root: ET.Element, output_dir: str) -> None:
        """Extract all SQL queries from the SSIS package."""
        os.makedirs(output_dir, exist_ok=True)
        print(f"\nDebug: Extracting SQL to {output_dir}")
        
        # Extract from Execute SQL Tasks
        sql_tasks = root.findall('.//DTS:Executable[@DTS:CreationName="Microsoft.ExecuteSQLTask"]', self.ns)
        if not sql_tasks:  # Try case-insensitive
            sql_tasks = root.findall('.//DTS:Executable[@DTS:CreationName="MICROSOFT.EXECUTESQLTASK"]', self.ns)
        print(f"Debug: Found {len(sql_tasks)} SQL tasks")
        
        for task in sql_tasks:
            try:
                task_name = task.get('{' + self.ns['DTS'] + '}ObjectName', 'UnknownTask')
                print(f"\nDebug: Processing SQL task: {task_name}")
                
                # Try to find SQL in SQLTask:SqlTaskData
                sql_data = task.find('.//SQLTask:SqlTaskData', self.ns)
                if sql_data is not None:
                    sql_query = sql_data.get('SQLTask:SqlStatementSource', '')
                    print(f"Debug: Found SQL data with query length: {len(sql_query)}")
                    if sql_query.strip():
                        sql_file_path = os.path.join(output_dir, f"{task_name}_SQLTask.sql")
                        os.makedirs(os.path.dirname(sql_file_path), exist_ok=True)
                        with open(sql_file_path, 'w', encoding='utf-8') as f:
                            f.write(sql_query)
                        print(f"Extracted SQL from Execute SQL Task '{task_name}'")
                else:
                    print("Debug: No SQLTask:SqlTaskData found")
                    
                    # Try alternative path for SQL
                    obj_data = task.find('.//DTS:ObjectData', self.ns)
                    if obj_data is not None:
                        print("Debug: Found ObjectData")
                        for child in obj_data:
                            print(f"Debug: ObjectData child: {child.tag}")
                            if 'SQLTask' in child.tag:
                                sql_query = child.get('SQLStatementSource', '')
                                if sql_query and sql_query.strip():
                                    sql_file_path = os.path.join(output_dir, f"{task_name}_SQLTask.sql")
                                    os.makedirs(os.path.dirname(sql_file_path), exist_ok=True)
                                    with open(sql_file_path, 'w', encoding='utf-8') as f:
                                        f.write(sql_query)
                                    print(f"Extracted SQL from Execute SQL Task '{task_name}' (alternative path)")
                    
            except Exception as e:
                print(f"Error processing SQL task {task_name}: {str(e)}")
        
        # Extract from Data Flow Tasks
        data_flow_tasks = root.findall('.//DTS:Executable[@DTS:CreationName="Microsoft.Pipeline"]', self.ns)
        if not data_flow_tasks:  # Try case-insensitive
            data_flow_tasks = root.findall('.//DTS:Executable[@DTS:CreationName="MICROSOFT.PIPELINE"]', self.ns)
        print(f"\nDebug: Found {len(data_flow_tasks)} Data Flow tasks")
        
        for df_task in data_flow_tasks:
            try:
                df_name = df_task.get('{' + self.ns['DTS'] + '}ObjectName', 'UnknownDataFlow')
                print(f"\nDebug: Processing Data Flow task: {df_name}")
                
                # Look for components in the objectdata/pipeline/components path
                obj_data = df_task.find('.//DTS:ObjectData', self.ns)
                if obj_data is not None:
                    print("Debug: Found ObjectData")
                    pipeline = obj_data.find('pipeline')
                    if pipeline is not None:
                        print("Debug: Found pipeline")
                        components = pipeline.findall('.//component')
                        print(f"Debug: Found {len(components)} components")
                        for component in components:
                            try:
                                self.extract_sql_from_component(component, df_name, output_dir)
                            except Exception as e:
                                print(f"Error processing component: {str(e)}")
                    else:
                        print("Debug: No pipeline found in ObjectData")
                else:
                    print("Debug: No ObjectData found")
                    
            except Exception as e:
                print(f"Error processing Data Flow task {df_name}: {str(e)}")
    
    def analyze_package(self, dtsx_path: str, output_dir: str = None) -> Dict[str, Any]:
        """Analyze an SSIS package and return its structure."""
        print(f"\nAnalyzing package: {dtsx_path}")
        try:
            tree = ET.parse(dtsx_path)
            root = tree.getroot()
            
            # Extract package information and continue with analysis
            analysis = {
                'package_info': self.extract_attributes(root),
                'connection_managers': self.parse_connection_managers(root),
                'tasks': self.parse_tasks(root),
                'precedence_constraints': self.parse_precedence_constraints(root),
                'task_count': len(self.parse_tasks(root)),
                'task_type_counts': self.count_tasks_by_type(self.parse_tasks(root)),
                'connection_count': len(self.parse_connection_managers(root)),
                'sql_query_count': 0  # Initialize sql_query_count
            }

            # Extract SQL queries if output directory is provided
            if output_dir:
                package_name = os.path.splitext(os.path.basename(dtsx_path))[0]
                abs_output_dir = os.path.join(output_dir,package_name)
                sql_output_dir = os.path.join(abs_output_dir, 'SQL_Scripts')
                os.makedirs(abs_output_dir, exist_ok=True)
                os.makedirs(sql_output_dir, exist_ok=True)
                print(f"\nExtracting SQL queries from {os.path.basename(dtsx_path)}...")
                self.extract_sql_queries(root, sql_output_dir)
                analysis['sql_query_count'] = len(glob.glob(os.path.join(sql_output_dir, '*.sql')))
        
            return analysis, abs_output_dir
        except Exception as e:
            print(f"Error analyzing package {dtsx_path}: {str(e)}")
            return None

def analyze_all_packages(ssis_dir: str, output_dir: str = 'SSISDetailedAnalysisOutput') -> Dict[str, Any]:
    """Analyze all SSIS packages in a directory and its subdirectories."""
    analyzer = SSISAnalyzer()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all .dtsx files
    dtsx_files = []
    for root, _, files in os.walk(ssis_dir):
        for file in files:
            if file.endswith('.dtsx'):
                dtsx_files.append(os.path.join(root, file))
    
    # Analyze each package
    analyses = []
    total_sql_queries = 0
    connection_types = {}
    task_types = {}
    component_types = {}
    
    for dtsx_path in dtsx_files:
        analysis, abs_output_dir = analyzer.analyze_package(dtsx_path, output_dir=output_dir)
        # print(f"Analysis status:  {analysis}")
        if analysis:
            package_info = {
                'name': os.path.basename(dtsx_path),
                'path': os.path.relpath(dtsx_path, ssis_dir),
                'creation_date': analysis['package_info'].get('CreationDate', ''),
                'creator': analysis['package_info'].get('CreatorName', ''),
                'task_count': analysis['task_count'],
                'task_type_counts': analysis['task_type_counts'],
                'connection_count': analysis['connection_count'],
                'sql_query_count': analysis['sql_query_count']
            }
            analyses.append(package_info)
            
            # Update totals
            total_sql_queries += analysis['sql_query_count']
            
            # Update connection types
            for conn in analysis['connection_managers']:
                conn_type = conn.get('CreationName', 'Unknown')
                connection_types[conn_type] = connection_types.get(conn_type, 0) + 1
            
            # Update task types from task_type_counts
            for task_type, count in analysis['task_type_counts'].items():
                task_types[task_type] = task_types.get(task_type, 0) + count
            
            # Update component types
            for task in analysis['tasks']:
                if task.get('CreationName') == 'Microsoft.Pipeline':
                    for component in task.get('components', []):
                        comp_type = component.get('componentClassID', 'Unknown')
                        component_types[comp_type] = component_types.get(comp_type, 0) + 1
            # save analysis to file
            # create sub directory if it doesn't exist
            output_file = os.path.join(abs_output_dir, f"{os.path.splitext(os.path.basename(dtsx_path))[0]}_analysis.json")
            print(output_file)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"\nAnalysis complete! Results saved to {output_file}")
    
    # Create summary
    summary = {
        'total_packages': len(analyses),
        'total_sql_queries': total_sql_queries,
        'connection_types': connection_types,
        'task_types': task_types,
        'component_types': component_types,
        'packages': sorted(analyses, key=lambda x: x['path'])
    }
    
    # Write summary to file
    summary_path = os.path.join(output_dir, 'analysis_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary

if __name__ == "__main__":
    import sys
    import glob
    
    if len(sys.argv) < 2:
        print("Please provide the path to SSIS package(s)")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'SSISDetailedAnalysisOutput'
    
    if os.path.isfile(input_path):
        # Single file analysis
        if not input_path.endswith('.dtsx'):
            print("Input file must be a .dtsx file")
            sys.exit(1)
        
        analyzer = SSISAnalyzer()
        try:
            analysis = analyzer.analyze_package(input_path, output_dir)
            output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_path))[0]}_analysis.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"\nAnalysis complete! Results saved to {output_file}")
            
            # Generate diagram
            diagram = analyzer.generate_mermaid_diagram(analysis)
            diagram_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_path))[0]}_diagram.mmd")
            with open(diagram_file, 'w', encoding='utf-8') as f:
                f.write(diagram)
            print(f"Diagram saved to {diagram_file}")
            
        except Exception as e:
            print(f"Error analyzing file: {str(e)}")
            sys.exit(1)
    else:
        # Directory analysis
        results = analyze_all_packages(input_path, output_dir)
        print(f"\nAnalysis complete! Found {results['total_packages']} packages with {results['total_sql_queries']} SQL queries.")
        print("\nSummary:")
        print("Packages:")
        for package in results['packages']:
            print(f"  - {package['name']} ({package['path']}) - {package['sql_query_count']} SQL queries")
        print(f"\nDetailed analysis saved to {output_dir}/")