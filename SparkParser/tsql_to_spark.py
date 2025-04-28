import streamlit as st
from openai import OpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
import json
import os
from test_sql_with_parser import check_spark_sql_syntax
from dotenv import load_dotenv
import requests
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

# Configuration for platforms
PLATFORM_CONFIG = {
    "OpenRouter": {
        "converter": {
            "base_url": os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            "api_key": os.getenv("OPENROUTER_API_KEY"),
            "model": os.getenv("OPENROUTER_CONV_MODEL", "openai/gpt-4o-mini-2024-07-18")
        },
        "judge": {
            "base_url": os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            "api_key": os.getenv("OPENROUTER_API_KEY"),
            "model": os.getenv("OPENROUTER_JUDGE_MODEL", "anthropic/claude-3.5-haiku")
        },
        "embeddings": {
            "base_url": os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            "api_key": os.getenv("OPENROUTER_API_KEY"),
            "model": os.getenv("OPENROUTER_EMBED_MODEL", "text-embedding-ada-002")
        }
    },
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
        },
        "embeddings": {
            "base_url": os.getenv("AZURE_BASE_EMBED_URL", "https://kian-m7ws0x3z-swedencentral.openai.azure.com/openai/deployments/gpt-4o-test/embeddings?api-version=2024-10-21"),
            "api_key": os.getenv("AZURE_API_KEY"),
            "model": os.getenv("AZURE_BASE_EMBED_MODEL", "text-embedding-ada-002")
        }
    }
}

# Platform selection dropdown
selected_platform = st.selectbox(
    "Select Platform",
    options=["OpenRouter", "Azure"],
    index=0  # Default to OpenRouter
)

# Initialize clients based on selected platform
config = PLATFORM_CONFIG[selected_platform]
if selected_platform == "OpenRouter":
    converter_client = OpenAI(base_url=config["converter"]["base_url"], api_key=config["converter"]["api_key"])
    judge_client = OpenAI(base_url=config["judge"]["base_url"], api_key=config["judge"]["api_key"])
else:
    converter_client = None
    judge_client = None

# LLM call function
def llm_call(client, model, prompt, platform_config):
    if selected_platform == "OpenRouter":
        headers = {"Content-Type": "application/json", "X-Title": "TSQL to Spark SQL"}
        completion = client.chat.completions.create(
            extra_headers=headers,
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            temperature=1,
            top_p=1
        )
        return completion.choices[0].message.content.strip()
    elif selected_platform == "Azure":
        headers = {"Content-Type": "application/json", "api-key": platform_config["api_key"]}
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
            "temperature": 1,
            "top_p": 1,
            "model": model
        }
        response = requests.post(platform_config["base_url"], headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

# Setup RAG
def load_rag_data():
    rag_file = "rag_data/conversions.jsonl"
    if not os.path.exists(rag_file):
        return []
    documents = []
    with open(rag_file, "r") as f:
        for line in f:
            pair = json.loads(line.strip())
            doc = Document(
                page_content=f"T-SQL: {pair['tsql']}\nSparkSQL: {pair['sparksql']}",
                metadata={"tsql": pair["tsql"], "sparksql": pair["sparksql"]}
            )
            documents.append(doc)
    return documents

def initialize_rag():
    if st.session_state.get("use_rag", False) and "vector_store" not in st.session_state:
        embeddings_config = config["embeddings"]
        embeddings = OpenAIEmbeddings(
            openai_api_key=embeddings_config["api_key"],
            base_url=embeddings_config["base_url"].replace("/chat/completions", "/embeddings") if selected_platform == "Azure" else embeddings_config["base_url"],
            model=embeddings_config["model"]
        )
        docs = load_rag_data()
        if docs:
            st.session_state.vector_store = FAISS.from_documents(docs, embeddings)
            st.session_state.retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
        else:
            st.session_state.vector_store = None
            st.session_state.retriever = None

# SparkSQL syntax checker
def check_sparksql_syntax(query):
    is_valid, message = check_spark_sql_syntax(query)
    print(f"syntax check: {message}")
    return "VALID" if is_valid else message

# Define the state for LangGraph
class ConversionState(TypedDict):
    tsql_query: str
    sparksql_query: str
    validation_errors: List[str]
    judge_feedback: str
    syntax_feedback: str
    attempt_count: Annotated[int, operator.add]

# LangGraph nodes
def initial_conversion(state: ConversionState) -> ConversionState:
    examples = ""
    if st.session_state.get("use_rag", False) and "retriever" in st.session_state and st.session_state.retriever:
        retrieved_docs = st.session_state.retriever.get_relevant_documents(state["tsql_query"])
        examples = "\n\n".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else ""
    
    prompt = f"""Convert this T-SQL query to SparkSQL:
    {state['tsql_query']}
    {"Use these examples for guidance:" + examples if examples else ""}
    Provide only the converted SparkSQL query."""
    sparksql = llm_call(converter_client if selected_platform == "OpenRouter" else None, config["converter"]["model"], prompt, config["converter"])
    return {"sparksql_query": sparksql, "attempt_count": 1}

def validate_conversion(state: ConversionState) -> ConversionState:
    prompt = f"""Check if this SparkSQL query is valid:
    {state['sparksql_query']}
    Return 'VALID' if valid, or a list of errors if invalid."""
    validation_result = llm_call(converter_client if selected_platform == "OpenRouter" else None, config["converter"]["model"], prompt, config["converter"])
    errors = [] if validation_result == "VALID" else validation_result.split("\n")
    return {"validation_errors": errors}

def judge_conversion(state: ConversionState) -> ConversionState:
    syntax_feedback = ""
    if st.session_state.get("use_syntax_check", False):
        syntax_result = check_sparksql_syntax(state["sparksql_query"])
        syntax_feedback = "VALID" if syntax_result == "VALID" else f"Syntax error: {syntax_result}"
    
    prompt = f"""Compare this T-SQL query:
    {state['tsql_query']}
    
    With this SparkSQL query:
    {state['sparksql_query']}
    
    Provide very short feedback:
    - 'Semantically equivalent' or 'Not semantically equivalent'
    - Add 'Syntax error' if there's an obvious syntax error in the SparkSQL"""
    feedback = llm_call(judge_client if selected_platform == "OpenRouter" else None, config["judge"]["model"], prompt, config["judge"])
    return {"judge_feedback": feedback, "syntax_feedback": syntax_feedback}

def fix_conversion(state: ConversionState) -> ConversionState:
    if not state["validation_errors"] and "Not semantically equivalent" not in state["judge_feedback"]:
        return state
    examples = ""
    if st.session_state.get("use_rag", False) and "retriever" in st.session_state and st.session_state.retriever:
        retrieved_docs = st.session_state.retriever.get_relevant_documents(state["tsql_query"])
        examples = "\n\n".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else ""
    
    prompt = f"""Fix these errors and ensure semantic equivalence in the SparkSQL query:
    Original T-SQL: {state['tsql_query']}
    Current SparkSQL: {state['sparksql_query']}
    Syntax Errors: {', '.join(state['validation_errors']) if state['validation_errors'] else 'None'}
    Judge Feedback: {state['judge_feedback'] if state['judge_feedback'] else 'None'}
    {"Use these examples for guidance:" + examples if examples else ""}
    Provide only the fixed SparkSQL query."""
    fixed_sparksql = llm_call(converter_client if selected_platform == "OpenRouter" else None, config["converter"]["model"], prompt, config["converter"])
    return {"sparksql_query": fixed_sparksql, "attempt_count": state["attempt_count"] + 1}

# Parallel execution of validate and judge
def parallel_validate_and_judge(state: ConversionState) -> ConversionState:
    with ThreadPoolExecutor() as executor:
        future_validate = executor.submit(validate_conversion, state)
        future_judge = executor.submit(judge_conversion, state)
        validate_result = future_validate.result()
        judge_result = future_judge.result()
    return {**state, **validate_result, **judge_result}

# Define the graph
def build_graph():
    workflow = StateGraph(ConversionState)
    workflow.add_node("convert", initial_conversion)
    workflow.add_node("validate_and_judge", parallel_validate_and_judge)
    workflow.add_node("fix", fix_conversion)
    
    workflow.set_entry_point("convert")
    workflow.add_edge("convert", "validate_and_judge")
    
    def should_rejudge(state):
        syntax_issue = st.session_state.get("use_syntax_check", False) and "Syntax error" in state["syntax_feedback"]
        judge_issue = "Not semantically equivalent" in state["judge_feedback"] or "Syntax error" in state["judge_feedback"]
        validation_issue = len(state["validation_errors"]) > 0
        return (syntax_issue or judge_issue or validation_issue) and state["attempt_count"] < 3
    
    workflow.add_conditional_edges("validate_and_judge", should_rejudge, {True: "fix", False: END})
    workflow.add_edge("fix", "validate_and_judge")
    
    return workflow.compile()

# Compile the graph once
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

# Main Streamlit app
st.title("Advanced T-SQL to SparkSQL Converter with Optional RAG and Syntax Check")

# Toggles
st.session_state.use_rag = st.toggle("Use RAG (Example-Based Conversion)", value=False)
st.session_state.use_syntax_check = st.toggle("Use Syntax Checker", value=False)
initialize_rag()

tsql_input = st.text_area(
    "Enter your T-SQL query here:",
    height=200,
    placeholder="Example:\nSELECT TOP (10) * FROM dbo.table WITH (NOLOCK)\nWHERE date = GETDATE()"
)

if tsql_input:
    with st.spinner("Converting and evaluating..."):
        try:
            initial_state = {
                "tsql_query": tsql_input,
                "sparksql_query": "",
                "validation_errors": [],
                "judge_feedback": "",
                "syntax_feedback": "",
                "attempt_count": 0
            }
            result = st.session_state.graph.invoke(initial_state)
            
            st.subheader("Converted SparkSQL Query:")
            st.code(result["sparksql_query"], language="sql")
            
            if result["validation_errors"]:
                st.warning(f"Validation issues: {', '.join(result['validation_errors'])}")
            if result["judge_feedback"]:
                st.info(f"LLM Judge Feedback: {result['judge_feedback']}")
            if st.session_state.use_syntax_check and result["syntax_feedback"]:
                st.info(f"Syntax Checker Feedback: {result['syntax_feedback']}")
            st.write(f"Conversion attempts: {result['attempt_count']}")
            if st.session_state.use_rag and "vector_store" not in st.session_state:
                st.warning("RAG is enabled but no conversion examples found in rag_data/conversions.jsonl")
                
        except Exception as e:
            st.error(f"Error in process: {str(e)}")

with st.expander("Conversion Notes"):
    st.write(f"""
    This converter (using {selected_platform}):
    1. Converts T-SQL to SparkSQL ({config["converter"]["model"]})
    2. Validates syntax and judges semantics in parallel
    3. Fixes errors and ensures equivalence (up to 3 attempts)
    4. Optionally uses RAG with example pairs (toggle above)
    5. Optionally checks syntax with a parser (toggle above)
    """)

if st.button("Clear"):
    st.rerun()