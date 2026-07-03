# ReAct Pattern — Reasoning + Acting

## Learning Objective

By the end of this section, you should understand:

- What the ReAct pattern is
- Why it was introduced
- How it works
- How it differs from simple prompting
- Why it is the foundation of modern AI agents

---

# What is ReAct?

**ReAct** stands for **Reason + Act**.

It is a prompting and agent design pattern where an LLM **alternates between reasoning about a problem and taking actions** (such as calling tools), using the results of those actions to continue reasoning until it reaches a final answer.

Instead of trying to solve everything in one step, the model works iteratively.

```text
Question
    │
    ▼
Reason
    │
    ▼
Action
    │
    ▼
Observation
    │
    ▼
Reason Again
    │
    ▼
Final Answer
```

The pattern was introduced in the paper **ReAct: Synergizing Reasoning and Acting in Language Models (2022)** and has become the conceptual foundation for many modern agent frameworks.

---

# Why Do We Need ReAct?

Consider the question:

> What is the current weather in Kochi?

A standard LLM might answer from its training data, which could be outdated or incorrect.

Instead, a ReAct-style agent reasons:

```text
I don't know today's weather.

I should use the Weather API.

I'll use the result to answer.
```

This enables the model to combine **reasoning** with **real-world actions**.

---

# The ReAct Loop

The loop consists of four stages:

```text
Question

↓

Thought

↓

Action

↓

Observation

↓

Thought

↓

Answer
```

Let's look at each step.

---

## 1. Thought (Reason)

The model analyzes the problem.

It asks itself questions like:

- What information do I need?
- Do I already know the answer?
- Should I use a tool?
- What should I do next?

Example:

```text
Thought:
The user is asking for today's weather.
I need current weather information.
```

---

## 2. Action

The model chooses an external tool.

Example:

```text
Action:
Weather API(city="Kochi")
```

Notice that the model **doesn't execute the tool itself**—it requests the application to execute it.

---

## 3. Observation

The application executes the tool and returns the result.

```text
Observation:

Temperature: 28°C

Condition: Rain
```

The observation becomes new information for the model.

---

## 4. Reason Again

Now the model has enough information.

```text
Thought:

It is raining.

Recommend carrying an umbrella.
```

---

## Final Answer

```text
It is currently 28°C with rain expected.
You should carry an umbrella today.
```

---

# Complete Example

User asks:

> What is 452 × 198?

```text
Question

↓

Thought

I should use the calculator.

↓

Action

Calculator(452,198)

↓

Observation

89496

↓

Thought

I have the result.

↓

Answer

89,496
```

---

# Example: Booking a Meeting

User:

> Schedule a meeting with Alice tomorrow afternoon.

```text
User

↓

Thought

Need calendar availability.

↓

Action

Check Calendar

↓

Observation

3 PM is available.

↓

Thought

Book meeting.

↓

Action

Create Meeting

↓

Observation

Meeting created.

↓

Answer

Your meeting has been scheduled for 3 PM tomorrow.
```

Notice that multiple reasoning and action steps are involved before reaching the final response.

---

# Visualizing the Loop

```text
                 User Goal
                     │
                     ▼
               ┌──────────┐
               │  Reason  │
               └──────────┘
                     │
                     ▼
               ┌──────────┐
               │    Act   │
               └──────────┘
                     │
                     ▼
               ┌──────────┐
               │ Observe  │
               └──────────┘
                     │
                     └──────────► Back to Reason
```

This cycle continues until the task is complete.

---

# ReAct vs Traditional Prompting

### Traditional Prompting

```text
User

↓

LLM

↓

Answer
```

Characteristics:

- Single inference
- No tool usage
- No intermediate decisions
- Limited to the model's knowledge

---

### ReAct

```text
User

↓

Reason

↓

Tool

↓

Observe

↓

Reason

↓

Answer
```

Characteristics:

- Multi-step reasoning
- Dynamic tool usage
- Can adapt based on observations
- Handles more complex tasks

---

# ReAct and Agents

ReAct is the reasoning strategy behind many AI agents.

The agent repeatedly:

1. Understands the goal
2. Decides the next action
3. Uses a tool if needed
4. Observes the result
5. Continues until the goal is achieved

This aligns closely with the **Perceive → Reason → Act → Observe** agent loop.

---

# Where ReAct Fits

```text
LLM

↓

Tool Calling

↓

ReAct

↓

Agent

↓

Workflow (LangGraph)

↓

Multi-Agent
```

- **Tool Calling** gives the model capabilities.
- **ReAct** tells the model _how to use those capabilities effectively_.
- **Agents** use ReAct (or similar strategies) to accomplish goals.
- **LangGraph** provides structured workflows around these interactions.

---

# Does Every Agent Use ReAct?

No.

ReAct is one of the most influential reasoning patterns, but modern agent systems may use:

- Planning before execution
- Workflow graphs
- Reflection and self-correction
- Multi-agent collaboration
- Deterministic routing

Many frameworks, including LangChain and LangGraph, can implement ReAct-like behavior, but they are not limited to it.

---

# Advantages of ReAct

- Combines reasoning with external actions
- Reduces hallucinations by using real data
- Handles tasks requiring multiple steps
- Enables dynamic decision-making
- Forms the basis of many production AI agents

---

# Limitations

- More LLM calls increase latency and cost.
- Poor tool descriptions can lead to incorrect tool selection.
- Long reasoning loops can become inefficient.
- Not every problem requires iterative reasoning.

For simple tasks like translation or summarization, a single prompt is often sufficient.

---

# Key Takeaways

- **ReAct** stands for **Reason + Act**.
- It alternates between **reasoning**, **taking actions**, and **observing results**.
- It allows LLMs to solve problems that require external tools or multiple steps.
- ReAct is a foundational concept behind modern AI agents, enabling them to make decisions, use tools, and adapt based on observations.
- Use ReAct when tasks involve planning, tool usage, or iterative decision-making—not for simple, single-step prompts.
