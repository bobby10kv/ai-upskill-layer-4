# Tool Use and Tool Calling Patterns

## Learning Objective

By the end of this section, you should understand:

- What tool calling is
- Why LLMs need tools
- How tool calling works
- Common tool calling patterns
- When to use each pattern

---

# Why Do LLMs Need Tools?

An LLM is excellent at reasoning and generating text, but it **cannot reliably interact with the outside world on its own**.

Without tools, an LLM:

- Cannot fetch live weather
- Cannot query a database
- Cannot send an email
- Cannot execute code
- Cannot perform calculations accurately
- Cannot update business systems

Tools extend an LLM's capabilities by allowing it to interact with external systems.

---

# What is Tool Calling?

**Tool calling** is the ability for an LLM to decide that it needs external information or an action, request a tool invocation with structured arguments, receive the result, and continue generating a response.

Think of the LLM as the **decision-maker**, not the executor.

```text
                User
                  │
                  ▼
               LLM
                  │
      "I need a calculator"
                  ▼
          Calculator Tool
                  │
          Returns 89496
                  ▼
               LLM
                  │
                  ▼
          Final Response
```

---

# Tool Calling Workflow

```text
User Question

↓

LLM understands request

↓

LLM decides whether a tool is needed

↓

Generate tool call

↓

Application executes tool

↓

Tool returns result

↓

LLM uses result

↓

Final Answer
```

Notice that **the application executes the tool**, not the LLM itself.

---

# Example 1 – Calculator

User:

> What is 452 × 198?

Without a tool:

```text
LLM
↓

Attempts mental math

↓

May produce incorrect result
```

With a calculator tool:

```text
User

↓

LLM

↓

Calculator Tool

↓

89496

↓

LLM

↓

"The answer is 89,496."
```

---

# Example 2 – Weather

User:

> What's the weather in Kochi today?

```text
User

↓

LLM

↓

Weather API

↓

27°C, Rain

↓

LLM

↓

"It is currently 27°C with rain expected."
```

The model knows **it doesn't know** the answer and asks for a tool instead.

---

# Example 3 – Database Lookup

User:

> What is the status of Order #12345?

```text
User

↓

LLM

↓

Database Tool

↓

Processing

↓

LLM

↓

"Your order is currently being processed."
```

---

# Tool Definition

A tool consists of:

- Name
- Description
- Input schema
- Implementation

Example:

```python
from langchain_core.tools import tool

@tool
def calculator(a: int, b: int):
    """Multiply two integers."""
    return a * b
```

The LLM doesn't see the Python code—it sees the **tool metadata**, including the name, description, and expected inputs.

---

# Structured Arguments

Instead of natural language, the LLM generates structured arguments.

Example:

```json
{
  "tool": "calculator",
  "arguments": {
    "a": 452,
    "b": 198
  }
}
```

Your application executes the function and returns the result.

---

# Tool Execution Loop

```text
User

↓

LLM

↓

Tool Call

↓

Application Executes Tool

↓

Tool Result

↓

LLM

↓

Final Answer
```

This loop is the foundation of most AI agents.

---

# Common Tool Calling Patterns

## 1. Single Tool Call

One question → one tool.

Example:

> Calculate 89 × 11.

```text
User

↓

LLM

↓

Calculator

↓

979

↓

LLM

↓

Answer
```

**Use when:** Only one external action is needed.

---

## 2. Sequential Tool Calls

The output of one tool becomes the input to another.

Example:

> Find today's weather and email me a summary.

```text
User

↓

Weather API

↓

Weather Data

↓

Email Tool

↓

Email Sent

↓

LLM Response
```

Multiple steps executed in order.

---

## 3. Conditional Tool Calling

The LLM first decides whether a tool is necessary.

```text
User Question

↓

Need Tool?

├── No → Answer Directly
│
└── Yes
      │
      ▼
   Call Tool
      │
      ▼
Answer
```

Example:

- "Explain recursion." → No tool
- "What's the weather?" → Weather tool

---

## 4. Parallel Tool Calling

Independent tools can run simultaneously.

Example:

> Compare today's weather in Kochi and Bengaluru.

```text
              User
                │
                ▼
               LLM
                │
        ┌───────┴────────┐
        ▼                ▼
 Weather API       Weather API
   (Kochi)          (Bengaluru)
        └───────┬────────┘
                ▼
               LLM
                ▼
         Comparison
```

This reduces latency when tool calls don't depend on each other.

---

## 5. Agentic Tool Loop

The LLM repeatedly reasons, calls tools, and observes results until the goal is achieved.

```text
Question

↓

Reason

↓

Tool

↓

Observe

↓

Need Another Tool?

↓

Yes

↓

Reason Again

↓

Final Answer
```

Example:

Book a meeting:

- Check calendar
- Find free slot
- Create meeting
- Notify attendees

---

# Tool Calling vs Function Calling

These terms are often used interchangeably.

| Function Calling                                     | Tool Calling                                                            |
| ---------------------------------------------------- | ----------------------------------------------------------------------- |
| Originally referred to calling application functions | Broader concept including APIs, databases, search, code execution, etc. |
| Typically local functions                            | Any external capability                                                 |
| Older terminology                                    | More common modern terminology                                          |

Think of **function calling** as a specific implementation of the broader **tool calling** concept.

---

# Tool Calling in LangChain

Define a tool:

```python
from langchain_core.tools import tool

@tool
def calculator(a: int, b: int):
    """Multiply two integers."""
    return a * b
```

Bind the tool to the model:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

llm_with_tools = llm.bind_tools([calculator])
```

Invoke:

```python
response = llm_with_tools.invoke(
    "Multiply 452 by 198"
)
```

LangChain handles exposing the tool schema to the model and parsing tool calls. Your application is still responsible for executing the tool and passing the results back to the model.

---

# Best Practices

- **Keep tools focused**: Each tool should perform one clear task.
- **Write descriptive docstrings**: The LLM relies on them to choose the right tool.
- **Use structured inputs**: Prefer typed parameters over free-form strings.
- **Validate inputs**: Never assume the model generates perfect arguments.
- **Handle failures gracefully**: Return meaningful errors so the agent can retry or explain the issue.
- **Limit available tools**: Expose only the tools relevant to the current task to improve accuracy and reduce unnecessary tool calls.

---

# Key Takeaways

- Tool calling enables an LLM to interact with external systems.
- The LLM **decides** when a tool is needed; your application **executes** it.
- Structured arguments make tool invocation reliable and machine-readable.
- Common patterns include **single**, **sequential**, **conditional**, **parallel**, and **agentic** tool calling.
- Tool calling is the foundational capability behind modern AI agents and orchestration frameworks like LangChain and LangGraph.
