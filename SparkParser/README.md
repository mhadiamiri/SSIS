# Spark SQL Parser and T-SQL to Spark SQL Converter

This tool provides functionality to validate Spark SQL syntax and convert T-SQL queries to Spark SQL using a sophisticated LLM-based approach with validation mechanisms.

## Overview

The project consists of two main components:

1. **Spark SQL Syntax Validation**: A Docker-based validation system that checks if Spark SQL queries are syntactically correct
2. **T-SQL to Spark SQL Conversion**: A Streamlit application that converts T-SQL to Spark SQL using LLMs with multi-step validation

## 1. Spark SQL Syntax Validation

We evaluated multiple approaches for validating Spark SQL syntax and implemented a reliable solution using a containerized Spark environment.

### Validation Approaches Evaluated

1. **sqlglot Library**: Initial tests with the Python `sqlglot` library showed it couldn't reliably detect erroneous queries (too many false negatives).
   
2. **Antlr4 Spark Parser**: We explored using Antlr4 to build custom lexers and parsers, but the Python port had issues, and the manual verified version (~2400 lines) still lacked full coverage of Spark SQL syntax.

3. **Manual Spark Parser**: A simplified custom parser which only worked for basic queries.

4. **Spark Docker Container** (Selected Approach): Executes queries in a containerized Spark environment to perform real-time syntax checking.

### Spark Container Implementation

The container-based validation:

1. Takes a SQL query as input
2. Creates a temporary Python script with the query
3. Runs the script in a Docker container with Spark
4. Analyzes the output to determine if the query is valid

```python
def check_spark_sql_syntax(sql_query):
    """
    Runs a shell script that checks Spark SQL syntax and returns the output.
    
    :param sql_query: The SQL query to check
    :return: Tuple of (is_valid: bool, message: str)
    """
    try:
        # Run the query in Docker container
        command = ["bash", absolute_path, sql_query]
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Process results
        if "[PARSE_SYNTAX_ERROR]" in stdout:
            return False, result_text
        elif "[TABLE_OR_VIEW_NOT_FOUND]" in stdout:
            return True, stdout  # This is expected in syntax check
        else:
            return (result.returncode == 0), stdout or stderr
    except Exception as e:
        return False, f"Exception: {str(e)}"
```

### Testing

We've included extensive test cases covering:

- **Valid Queries**: Complex SELECTs with JOINs, window functions, CTEs, UNION ALL, aggregations with CUBE, nested subqueries, etc.
- **Invalid Queries**: T-SQL specific constructs like OUTPUT clause, TOP with PERCENT, CROSS APPLY, MERGE statements, STRING_AGG function, etc.

## 2. T-SQL to Spark SQL Conversion

A Streamlit application that provides an end-to-end pipeline for converting T-SQL to Spark SQL using LLMs and validation mechanisms.

### Key Features

1. **Multiple LLM Provider Support**: Can use OpenRouter or Azure OpenAI
2. **Retrieval-Augmented Generation (RAG)**: Retrieves similar conversion examples to guide the LLM
3. **Multi-step Validation**: Combines LLM-based validation with syntax checking
4. **Automatic Error Correction**: Fixes identified issues in the generated Spark SQL
5. **Parallel Processing**: Runs validation and semantic judgment in parallel

### LangGraph Workflow

The conversion follows a directed graph workflow:

```
[Initial Conversion] → [Validate & Judge] → [Fix (if needed)] → [Validate & Judge] → ...
```

1. **Initial Conversion**: Convert the T-SQL query to Spark SQL using an LLM
2. **Parallel Validation & Judgment**: Check for syntax errors and assess semantic equivalence simultaneously
3. **Fix Errors**: If issues are found, fix the conversion and re-validate (up to 3 attempts)

### TODO: Retrieval-Augmented Generation (RAG)

To improve conversion quality, the system can use a RAG system that retrieves relevant examples of past successful conversions:

```python
def initialize_rag():
    if st.session_state.get("use_rag", False) and "vector_store" not in st.session_state:
        # Initialize embeddings and retriever
        embeddings = OpenAIEmbeddings(...)
        docs = load_rag_data()
        if docs:
            st.session_state.vector_store = FAISS.from_documents(docs, embeddings)
            st.session_state.retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
```

The RAG system retrieves up to 3 similar previous conversions from `rag_data/conversions.jsonl` to help guide the LLM in making the current conversion.

## Usage

### Running the Syntax Checker

```python
from test_sql_with_parser import check_spark_sql_syntax

# Check if a query is valid
is_valid, message = check_spark_sql_syntax("SELECT * FROM users WHERE active = true")
print(f"Valid: {is_valid}, Message: {message}")
```

### Running the Converter Application

```bash
# Start the Streamlit app
streamlit run tsql_to_spark.py
```

In the web interface:

1. Select the LLM provider (OpenRouter or Azure)
2. Toggle RAG and syntax checking as needed
3. Enter your T-SQL query
4. View the converted Spark SQL, validation results, and feedback

## Configuration

The application supports configuration for different LLM providers:

```python
PLATFORM_CONFIG = {
    "OpenRouter": {
        "converter": {
            "base_url": "https://openrouter.ai/api/v1",
            "api_key": "your-openrouter-api-key",
            "model": "openai/gpt-4o-mini-2024-07-18"
        },
        # Other configurations...
    },
    "Azure": {
        "converter": {
            "base_url": "your-azure-endpoint",
            "api_key": "your-azure-api-key",
            "model": "gpt-4o-mini"
        },
        # Other configurations...
    }
}
```

## Docker Setup for Spark SQL Validation

To use the syntax checker, you need to set up the Docker container:

```bash
# Run the container
docker run spark:python3

# The script will run the container once to make sure it's locally available to be called by the shell script
```

## Dependencies

- Python 3.12
- streamlit
- langgraph
- openai
- langchain
- faiss-cpu (for RAG)
- dotenv
- Docker (for syntax checking)

## Implementation Details

### Key Files

- `test_sql_with_parser.py`: Implements the Spark SQL syntax validation
- `tsql_to_spark.py`: Main Streamlit application for T-SQL to Spark SQL conversion
- `tsql_to_spark_directory.py`: The script to perform batch T-SQL to Spark SQL conversion doing the I/O on json files
- `Spark_Container/run-spark-sql.sh`: Shell script for running queries in Docker and format the log 

### Architecture

The application uses a LangGraph workflow to manage the conversion process:

```python
def build_graph():
    workflow = StateGraph(ConversionState)
    workflow.add_node("convert", initial_conversion)
    workflow.add_node("validate_and_judge", parallel_validate_and_judge)
    workflow.add_node("fix", fix_conversion)
    
    workflow.set_entry_point("convert")
    workflow.add_edge("convert", "validate_and_judge")
    
    # Decide if we need to fix and retry
    workflow.add_conditional_edges("validate_and_judge", should_rejudge, 
                                   {True: "fix", False: END})
    workflow.add_edge("fix", "validate_and_judge")
    
    return workflow.compile()
```

## Future Improvements

1. **Develop RAG System**: Improve example selection with fine-tuned embeddings
2. **Conversion Rules Database** (Potentially): Maintain a database of specific conversion rules for edge cases
