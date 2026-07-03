# LangChain for Chains, Tools, and Retrieval Integration

> **Learning Objective**
>
> By the end of this section, you should understand:
>
> - What LangChain is
> - Its core building blocks
> - How to build a simple chain
> - How to add tools
> - How retrieval (RAG) fits into LangChain

---

# What is LangChain?

**LangChain** is an orchestration framework for building LLM applications.

Instead of manually writing prompt formatting, API calls, tool execution, and retrieval logic, LangChain provides reusable abstractions.

Think of it as:

```text
Spring Boot
        for
LLM Applications
```

It doesn't replace the LLM—it helps organize everything around it.

---

# LangChain Core Components

```text
          User
            │
            ▼
      PromptTemplate
            │
            ▼
        Chat Model
            │
     ┌──────┴────────┐
     ▼               ▼
   Tools         Retriever
     │               │
     └──────┬────────┘
            ▼
        Final Answer
```

The components you'll use most are:

- Chat Models
- Prompt Templates
- Chains (LCEL)
- Tools
- Retrievers
- Output Parsers

---

# 1. Chains

A **chain** connects multiple steps together.

Example:

```text
Prompt
    │
    ▼
LLM
    │
    ▼
Parser
```

LangChain uses the **LangChain Expression Language (LCEL)**.

---

## Example: Simple Chain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms."
)

chain = prompt | llm | StrOutputParser()

response = chain.invoke({"topic": "Vector Databases"})

print(response)
```

The `|` operator pipes the output of one component into the next.

---

# 2. Prompt Templates

Instead of building prompts manually:

```python
prompt = f"Explain {topic}"
```

Use templates.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful teacher.

    Explain {topic} in simple language.
    """
)
```

Benefits:

- Reusable
- Cleaner
- Parameterized
- Easier to maintain

---

# 3. Tools

A tool is simply a Python function with metadata that the LLM can use.

## Define a Tool

```python
from langchain_core.tools import tool

@tool
def calculator(a: int, b: int):
    """Multiply two integers."""
    return a * b
```

The docstring is important—it helps the LLM decide when to use the tool.

---

## Bind Tools to the Model

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

llm_with_tools = llm.bind_tools([calculator])
```

---

## Invoke

```python
response = llm_with_tools.invoke(
    "Multiply 452 by 198"
)

print(response)
```

The model can decide to call the calculator instead of trying to compute the answer itself.

---

# Multiple Tools

```python
@tool
def weather(city: str):
    """Get weather for a city."""
    return f"Sunny in {city}"

@tool
def calculator(a: int, b: int):
    """Multiply numbers."""
    return a * b

llm_with_tools = llm.bind_tools(
    [weather, calculator]
)
```

The model chooses the appropriate tool based on the user's request.

---

# 4. Retrieval (RAG)

Retrieval allows the model to answer questions using your own documents instead of relying only on its training data.

Workflow:

```text
PDF

↓

Split

↓

Embeddings

↓

Vector Store

↓

Retriever

↓

LLM

↓

Answer
```

---

## Load Documents

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("company_handbook.pdf")
docs = loader.load()
```

---

## Split Documents

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)

chunks = splitter.split_documents(docs)
```

---

## Create Embeddings

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
```

---

## Store in a Vector Database

```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)
```

---

## Create a Retriever

```python
retriever = vectorstore.as_retriever()
```

---

## Retrieve Relevant Documents

```python
results = retriever.invoke(
    "What is the leave policy?"
)

print(results)
```

The retriever returns only the most relevant document chunks.

---

# Retrieval + LLM

Now combine retrieval with the LLM.

```python
context = retriever.invoke(
    "What is the leave policy?"
)

prompt = ChatPromptTemplate.from_template(
"""
Answer the question using only the context.

Context:
{context}

Question:
{question}
"""
)

chain = prompt | llm | StrOutputParser()

response = chain.invoke({
    "context": context,
    "question": "What is the leave policy?"
})

print(response)
```

This is the essence of a **Retrieval-Augmented Generation (RAG)** pipeline.

---

# End-to-End Architecture

```text
                  User
                    │
                    ▼
               PromptTemplate
                    │
                    ▼
               Chat Model
              /           \
             /             \
         Tools         Retriever
             \             /
              \           /
                    ▼
              Final Response
```

LangChain makes it straightforward to combine these components into a single application.

---

# When to Use Each Component

| Component       | Use Case                                          |
| --------------- | ------------------------------------------------- |
| Prompt Template | Reusable prompts                                  |
| Chain           | Connect multiple processing steps                 |
| Tool            | Execute external actions (APIs, DBs, calculators) |
| Retriever       | Fetch relevant documents                          |
| Output Parser   | Convert model output into structured formats      |

---

# Key Takeaways

- **Chains** connect prompts, models, and parsers into reusable pipelines.
- **Tools** allow LLMs to interact with external systems and perform actions.
- **Retrievers** fetch relevant information from your own knowledge base, enabling RAG.
- LangChain provides a consistent programming model for composing these building blocks, making it easier to build production-ready LLM applications.
