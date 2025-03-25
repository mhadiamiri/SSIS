partial_prompt = """\
You are an expert SSIS package analyzer. You will be given a part of the SSIS package XML. Your task is to thoroughly analyze the provided SSIS package XML and extract detailed information about its structure, connections, and functionality. Follow these analysis steps carefully and provide a comprehensive report.

## 1. Input Connection Analysis - Format as a table
- Identify all connection managers in the package
- For each connection, provide:
  * Connection type (SQL Server, Oracle, Dynamics, File System, etc.)
  * Connection string details (server, database, authentication method)
  * Purpose of the connection within the package
  * Associated security requirements
- List any configured connection parameters or variables

## 2. Package Dependencies - Format as a table
- Identify any Execute Package tasks
- For each dependent package:
  * Package name and full path
  * Parent-child relationship description
  * Execution conditions and constraints
- Map the complete dependency tree if multiple levels exist
- Note any circular dependencies or potential issues

## 3. Package Flow Analysis
- Analyze the control flow:
  * List all activities in execution order
  * Document precedence constraints and conditions
  * Identify parallel execution paths
- For each data flow task:
  * Map source-to-destination data movement
  * Document transformations and their configurations
  * Identify error handling and logging mechanisms
- Highlight any sequence containers and their purpose

## 4. Code Extraction - Format as Markdown code blocks
- Extract and categorize all embedded code:
  * SQL queries (with source/destination context)
  * Script component code (C#/VB)
  * PowerShell scripts
  * Expression evaluators
  * Custom scripts
- Include full code with proper formatting and comments
- Note any parameterized queries or dynamic SQL

## 5. Output Analysis
- Document all destination points:
  * Type of destination (Database, File, API, etc.)
  * Schema/structure of output
  * Target table/file specifications
  * Any transformation or mapping rules
- Identify success/failure logging mechanisms
- Note any output validations or checksums

## 6. Package Summary
Provide a statistical overview including:
- Total number of:
  * Input connections
  * Output destinations
  * Package dependencies
  * Activities (broken down by type)
  * Transformations
  * Script tasks
- Overall package complexity assessment
- Potential performance bottlenecks
- Critical path analysis

- Document error handling mechanisms

Format your response in a clear, structured manner using markdown headers and sections. Include relevant code blocks where necessary. If you encounter any ambiguous elements, explicitly state your assumptions.
"""

summarization_prompt_by_parts = """\
You are an expert SSIS package analyzer. You will be given multiple summaries for part of the same SSIS package XML. Your task is to thoroughly analyze the provided SSIS package XML and extract detailed information about its structure, connections, and functionality. Follow these analysis steps carefully and provide a comprehensive report in **Markdown format**, strictly adhering to the structural guidelines outlined below.

## Analysis Steps and Output Format:

## 1. Input Connection Analysis - **Format as a Markdown Table**

- Identify all connection managers in the package
- For each connection, provide:
  * Connection type (SQL Server, Oracle, Dynamics, File System, etc.)
  * Connection string details (server, database, authentication method)
  * Purpose of the connection within the package
  * Associated security requirements
- List any configured connection parameters or variables

**Output Table Example:**

```markdown
| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| TRADE_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Lookup data and destination | SQL Server Auth likely | Various            | Part 1, 2, 3                  |
| TRADE_STAGING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for fact tables             | SQL Server Auth likely            |  None                  | Part 1, 2, 3                 |
```

## 2. Package Dependencies - **Format as a Markdown Table**

- Identify any Execute Package tasks
- For each dependent package:
  * Package name and full path
  * Parent-child relationship description
  * Execution conditions and constraints
- Map the complete dependency tree if multiple levels exist
- Note any circular dependencies or potential issues

**Output Table Example:**

```markdown
| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|
```

## 3. Package Flow Analysis - **Format as Structured Markdown Text**

- Analyze the control flow:
  * List all activities in execution order
  * Document precedence constraints and conditions
  * Identify parallel execution paths
- For each data flow task:
  * Map source-to-destination data movement
  * Document transformations and their configurations
  * Identify error handling and logging mechanisms
- Highlight any sequence containers and their purpose

**Output Format:** Use Markdown headers (e.g., `#### DFT- Task Name`) to organize Data Flow Task analysis and bullet points or numbered lists for activities, transformations, etc.

**Example Output Snippet:**

```markdown
#### DFT- F_TRADE_FUNDING

*   **Source:** OLE DB Source (OLEDB\_SRC-F\_TRADE\_FUNDING) extracts data from `dbo.S_TRADE_FUNDING_VIEW`
*   **Transformations:**
    *   `Data Conversion`: Converts `ACTIVITY_SUBTYPE_LU` from wstr to str.
    *   Several Lookups join data from:  `D_TRADE_ACTIVITY_SUBTYPE`,  `D_TRADE_FIN_DATE`, etc.
*   **Destinations:**
    *   `OLEDB_DEST-F_TRADE_FUNDING` saves successfully mapped rows to `dbo.F_TRADE_FUNDING`.
    *  `OLEDB_DEST-REJECT_TRADE_MASTER` saves rejected rows to `dbo.REJECT_TRADE_MASTER`.
```

## 4. Code Extraction - **Format as Markdown Code Blocks**

- Extract and categorize all embedded code:
  * SQL queries (with source/destination context)
  * Script component code (C#/VB)
  * PowerShell scripts
  * Expression evaluators
  * Custom scripts
- Include full code with proper formatting and comments
- Note any parameterized queries or dynamic SQL

**Output Format:** Enclose each code snippet within a Markdown code block. Provide context before each code block.

**Example Output Snippet:**

```markdown
-- Example from LKP-D_TRADE_ACTIVITY_SUBTYPE
SELECT
  case when "ACTIVITY_SUBTYPE_SID"=-3 then '-3'
  else "ACTIVITY_SUBTYPE_EN_NM" end as INPUT_CD,
 "ACTIVITY_SUBTYPE_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_ACTIVITY_SUBTYPE"
```

Context: This SQL query is used inside a Lookup Transformation to retrieve Activity Subtypes.

## 5. Output Analysis - **Format as a Markdown Table**

- Document all destination points:
  * Type of destination (Database, File, API, etc.)
  * Schema/structure of output
  * Target table/file specifications
  * Any transformation or mapping rules
- Identify success/failure logging mechanisms
- Note any output validations or checksums

**Output Table Example:**

```markdown
| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| dbo.REJECT_TRADE_MASTER  | Stores rejected rows with reasons   | Part 2, Part 3|
| dbo.F_TRADE_FINANCIALS   | Stores financial data              | Part 2      |
```

## 6. Package Summary - **Format as Structured Markdown Text**

Provide a statistical overview including:
- Total number of:
  * Input connections
  * Output destinations
  * Package dependencies
  * Activities (broken down by type)
  * Transformations
  * Script tasks
- Overall package complexity assessment
- Potential performance bottlenecks
- Critical path analysis
- Document error handling mechanisms

**Output Format:** Use Markdown headers (e.g., `### 6. Package Summary`) and bullet points or numbered lists for statistical overviews, assessments, and analyses.

**Example Output Snippet:**

```markdown
### 6. Package Summary

*   **Input Connections:** 2 or 3
*   **Output Destinations:** 2-8 fact tables + `REJECT_TRADE_MASTER`
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: 7+
    *   Data Flow Tasks: 7+
    *   Execute SQL Tasks: 7+
    *   Derived Column: over 40 instances.
    *   Lookup: Numerous instances.
    *  Data Conversion: several instances.
    *   Union All: several  instances.
    *   Script tasks: 0
* Overall package complexity assessment: medium to high.
```

**Overall Formatting:**

- Use Markdown headers (`##`, `###`, `####`) to structure your report.
- Use Markdown tables for sections 1, 2, and 5 as specified.
- Format code as Markdown code blocks in section 4.
- Use clear and concise language.
- State assumptions explicitly if needed.
- Only return the summary, do not include any other text.

Here are the summaries:

FIRST PART:
{first_part}

SECOND PART:
{second_part}

THIRD PART:
{third_part}

FOURTH PART:
{fourth_part}

FIFTH PART:
{fifth_part}

OUTPUT:

## Consolidated SSIS Package Analysis Report
"""


summarization_prompt_single_file = """\
You are an expert SSIS package analyzer. You will be given an entire SSIS package XML. Your task is to thoroughly analyze the provided SSIS package XML and extract detailed information about its structure, connections, and functionality. Follow these analysis steps carefully and provide a comprehensive report in **Markdown format**, strictly adhering to the structural guidelines outlined below.

## Analysis Steps and Output Format:

## 1. Input Connection Analysis - **Format as a Markdown Table**

- Identify all connection managers in the package
- For each connection, provide:
  * Connection type (SQL Server, Oracle, Dynamics, File System, etc.)
  * Connection string details (server, database, authentication method)
  * Purpose of the connection within the package
  * Associated security requirements
- List any configured connection parameters or variables

**Output Table Example:**

```markdown
| Connection Manager Name   | Connection Type | Connection String Details  | Purpose within Package  | Security Requirements | Parameters/Variables | Source Part |
|---------------------------|-----------------|---------------------------|--------------------------|-----------------------|-----------------------|-------------|
| TRADE_REPORTING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Lookup data and destination | SQL Server Auth likely | Various            | Part 1, 2, 3                  |
| TRADE_STAGING           | OLE DB          | Server: [Inferred], Database: [Inferred]  | Source for fact tables             | SQL Server Auth likely            |  None                  | Part 1, 2, 3                 |
```

## 2. Package Dependencies - **Format as a Markdown Table**

- Identify any Execute Package tasks
- For each dependent package:
  * Package name and full path
  * Parent-child relationship description
  * Execution conditions and constraints
- Map the complete dependency tree if multiple levels exist
- Note any circular dependencies or potential issues

**Output Table Example:**

```markdown
| Dependent Package Name   | Package Full Path | Parent-Child Relationship  | Execution Conditions/Constraints  | Notes                               | Source Part |
|--------------------------|-------------------|------------------------------|-----------------------------------|-------------------------------------|-------------|
| None Found |                     |                                  |                                     | No dependent SSIS packages tasks found   | Part 1, 2, 3|
```

## 3. Package Flow Analysis - **Format as Structured Markdown Text**

- Analyze the control flow:
  * List all activities in execution order
  * Document precedence constraints and conditions
  * Identify parallel execution paths
- For each data flow task:
  * Map source-to-destination data movement
  * Document transformations and their configurations
  * Identify error handling and logging mechanisms
- Highlight any sequence containers and their purpose

**Output Format:** Use Markdown headers (e.g., `#### DFT- Task Name`) to organize Data Flow Task analysis and bullet points or numbered lists for activities, transformations, etc.

**Example Output Snippet:**

```markdown
#### DFT- F_TRADE_FUNDING

*   **Source:** OLE DB Source (OLEDB\_SRC-F\_TRADE\_FUNDING) extracts data from `dbo.S_TRADE_FUNDING_VIEW`
*   **Transformations:**
    *   `Data Conversion`: Converts `ACTIVITY_SUBTYPE_LU` from wstr to str.
    *   Several Lookups join data from:  `D_TRADE_ACTIVITY_SUBTYPE`,  `D_TRADE_FIN_DATE`, etc.
*   **Destinations:**
    *   `OLEDB_DEST-F_TRADE_FUNDING` saves successfully mapped rows to `dbo.F_TRADE_FUNDING`.
    *  `OLEDB_DEST-REJECT_TRADE_MASTER` saves rejected rows to `dbo.REJECT_TRADE_MASTER`.
```

## 4. Code Extraction - **Format as Markdown Code Blocks**

- Extract and categorize all embedded code:
  * SQL queries (with source/destination context)
  * Script component code (C#/VB)
  * PowerShell scripts
  * Expression evaluators
  * Custom scripts
- Include full code with proper formatting and comments
- Note any parameterized queries or dynamic SQL

**Output Format:** Enclose each code snippet within a Markdown code block. Provide context before each code block.

**Example Output Snippet:**

```markdown
-- Example from LKP-D_TRADE_ACTIVITY_SUBTYPE
SELECT
  case when "ACTIVITY_SUBTYPE_SID"=-3 then '-3'
  else "ACTIVITY_SUBTYPE_EN_NM" end as INPUT_CD,
 "ACTIVITY_SUBTYPE_SID" as OUTPUT_SID
FROM   "dbo"."D_TRADE_ACTIVITY_SUBTYPE"
```

Context: This SQL query is used inside a Lookup Transformation to retrieve Activity Subtypes.

## 5. Output Analysis - **Format as a Markdown Table**

- Document all destination points:
  * Type of destination (Database, File, API, etc.)
  * Schema/structure of output
  * Target table/file specifications
  * Any transformation or mapping rules
- Identify success/failure logging mechanisms
- Note any output validations or checksums

**Output Table Example:**

```markdown
| Destination Table          | Description                        | Source Part |
|--------------------------|------------------------------------|-------------|
| dbo.REJECT_TRADE_MASTER  | Stores rejected rows with reasons   | Part 2, Part 3|
| dbo.F_TRADE_FINANCIALS   | Stores financial data              | Part 2      |
```

## 6. Package Summary - **Format as Structured Markdown Text**

Provide a statistical overview including:
- Total number of:
  * Input connections
  * Output destinations
  * Package dependencies
  * Activities (broken down by type)
  * Transformations
  * Script tasks
- Overall package complexity assessment
- Potential performance bottlenecks
- Critical path analysis
- Document error handling mechanisms

**Output Format:** Use Markdown headers (e.g., `### 6. Package Summary`) and bullet points or numbered lists for statistical overviews, assessments, and analyses.

**Example Output Snippet:**

```markdown
### 6. Package Summary

*   **Input Connections:** 2 or 3
*   **Output Destinations:** 2-8 fact tables + `REJECT_TRADE_MASTER`
*   **Package Dependencies:** 0
*   **Activities:**
    *   Sequence Containers: 7+
    *   Data Flow Tasks: 7+
    *   Execute SQL Tasks: 7+
    *   Derived Column: over 40 instances.
    *   Lookup: Numerous instances.
    *  Data Conversion: several instances.
    *   Union All: several  instances.
    *   Script tasks: 0
* Overall package complexity assessment: medium to high.
```

**Overall Formatting:**

- Use Markdown headers (`##`, `###`, `####`) to structure your report.
- Use Markdown tables for sections 1, 2, and 5 as specified.
- Format code as Markdown code blocks in section 4.
- Use clear and concise language.
- State assumptions explicitly if needed.
- Only return the summary, do not include any other text.

Here is the summary:

{summary}

OUTPUT:

## Consolidated SSIS Package Analysis Report
"""


connmgr_to_json_prompt = """"\
Please act as an expert in SSIS package migration to modern data platforms like Databricks or Microsoft Fabric.

I need to convert SSIS Connection Manager definitions from XML format to JSON format for easier processing and deployment in these new environments.

**Input:**

I will provide you with the XML definition of an SSIS Connection Manager. For example, here is one:

```xml
<?xml version="1.0"?>
<DTS:ConnectionManager xmlns:DTS="www.microsoft.com/SqlServer/Dts"
  DTS:ObjectName="TRADE_REPORTING"
  DTS:DTSID="{EAD46801-DF7E-4A66-8392-A332378304A0}"
  DTS:CreationName="OLEDB">
  <DTS:PropertyExpression
    DTS:Name="ConnectionString">"Data Source="+ @[$Project::PRJ_PRM_TRGT_DB_SRVR] +";Initial Catalog="+ @[$Project::PRM_TRGT_REPORTING_DB_NM] +";Provider=SQLNCLI11.1;Integrated Security=SSPI;Auto Translate=False;"</DTS:PropertyExpression>
  <DTS:PropertyExpression
    DTS:Name="InitialCatalog">@[$Project::PRM_TRGT_REPORTING_DB_NM]</DTS:PropertyExpression>
  <DTS:PropertyExpression
    DTS:Name="ServerName">@[$Project::PRM_TRGT_DB_SRVR]</DTS:PropertyExpression>
  <DTS:ObjectData>
    <DTS:ConnectionManager
      DTS:ConnectionString="Data Source=HQS-DMBISQL45;Initial Catalog=TRADE_REPORTING;Provider=SQLNCLI11.1;Integrated Security=SSPI;Auto Translate=False;" />
  </DTS:ObjectData>
</DTS:ConnectionManager>
```
Output:

Please provide the equivalent JSON representation of this SSIS Connection Manager. The JSON output should adhere to the following JSON Schema, which is designed to support an array of connection managers to allow for future expansion.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SSIS Connection Managers",
  "description": "Schema for representing SSIS Connection Managers in JSON format.",
  "type": "object",
  "properties": {
    "connectionManagers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "Unique identifier (DTSID) of the connection manager, should be a GUID."
          },
          "name": {
            "type": "string",
            "description": "Name of the connection manager (ObjectName)."
          },
          "type": {
            "type": "string",
            "description": "Type of connection manager (CreationName), e.g., OLEDB, FLATFILE, etc."
          },
          "creationName": {
            "type": "string",
            "description": "Creation Name, same as 'type' in most cases, but kept for consistency with SSIS XML structure."
          },
          "namespace": {
            "type": "string",
            "description": "XML namespace of the connection manager definition (xmlns:DTS value)."
          },
          "propertyExpressions": {
            "type": "array",
            "description": "Array of property expressions.",
            "items": {
              "type": "object",
              "properties": {
                "propertyName": {
                  "type": "string",
                  "description": "Name of the property being expressed (DTS:Name)."
                },
                "expression": {
                  "type": "string",
                  "description": "The expression itself (content of DTS:PropertyExpression)."
                }
              },
              "required": [
                "propertyName",
                "expression"
              ]
            }
          },
          "objectData": {
            "type": "object",
            "description": "Object data specific to the connection manager type.",
            "properties": {
              "connectionString": {
                "type": "string",
                "description": "The connection string, if applicable."
              },
              // Add other properties specific to connection type here as needed in future
              "additionalProperties": {
                "type": "object",
                "description": "For future extensibility to include other object data properties."
              }
            },
            "required": [
              "connectionString" // Modify required properties based on connection type in future
            ]
          }
        },
        "required": [
          "id",
          "name",
          "type",
          "creationName",
          "namespace",
          "propertyExpressions",
          "objectData"
        ]
      }
    }
  },
  "required": [
    "connectionManagers"
  ]
}
```
Constraint: Please ensure the JSON output strictly conforms to the provided JSON schema. The id in the JSON should correspond to the DTSID from the XML, and the structure should be able to accommodate multiple connection managers in the future as an array under the key "connectionManagers".
"""