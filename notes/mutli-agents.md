# Multi-Agent Systems (Awareness Level)

> **Learning Objective**
>
> By the end of this section, you should understand:
>
> - What a multi-agent system is
> - Orchestrator vs. sub-agent patterns
> - Popular frameworks (CrewAI, AutoGen, OpenAI Swarm)
> - When multi-agent architectures are useful—and when they're unnecessary

---

# What is a Multi-Agent System?

A **multi-agent system (MAS)** is an AI application where **multiple specialized agents collaborate to solve a larger task**.

Instead of one "super agent" doing everything, work is divided among agents with specific responsibilities.

Think of it like a software development team:

- Product Manager
- Backend Engineer
- Frontend Engineer
- QA Engineer

Each has a specialized role, coordinated toward a common goal.

```text
            User Request
                 │
                 ▼
        ┌────────────────┐
        │ Orchestrator   │
        └────────────────┘
          │      │      │
          ▼      ▼      ▼
     Research  Coding  Review
       Agent    Agent   Agent
          │      │      │
          └──────┴──────┘
                 │
                 ▼
           Final Response
```

---

# Why Multiple Agents?

As applications become more complex, one agent may struggle to:

- Manage long reasoning chains
- Handle multiple domains
- Coordinate parallel work
- Maintain context across many tasks

Instead, specialized agents divide the work.

Example:

User asks:

> Research the latest AI trends, generate a presentation, and email it to my team.

Possible agents:

- Research Agent
- Content Writer Agent
- Presentation Generator
- Email Agent

Each focuses on one responsibility.

---

# Orchestrator vs Sub-Agent Pattern

The most common architecture is the **Orchestrator (Supervisor) Pattern**.

## Architecture

```text
               User
                 │
                 ▼
         Orchestrator Agent
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
 Research     Coding     Review
   Agent       Agent      Agent
      │          │          │
      └──────────┴──────────┘
                 │
                 ▼
          Final Response
```

---

## Orchestrator Responsibilities

The orchestrator:

- Understands the overall goal
- Breaks work into smaller tasks
- Chooses the appropriate agent
- Collects results
- Produces the final response

It usually doesn't perform specialized work itself.

Think of it as a **project manager**.

---

## Sub-Agent Responsibilities

Each sub-agent specializes in one capability.

Examples:

### Research Agent

- Web search
- Read documentation
- Summarize findings

---

### Coding Agent

- Generate code
- Fix bugs
- Explain implementation

---

### Review Agent

- Validate correctness
- Review generated code
- Check formatting
- Identify potential issues

Each agent has its own prompts, tools, and sometimes even different LLMs.

---

# Example Workflow

User:

> Build a REST API from this OpenAPI specification.

```text
User

↓

Orchestrator

↓

Research Agent
(Understand API)

↓

Coding Agent
(Generate Code)

↓

Review Agent
(Check Quality)

↓

Orchestrator

↓

Final Response
```

Notice how each agent contributes a specific part of the solution.

---

# Common Multi-Agent Patterns

## 1. Supervisor Pattern (Most Common)

```text
Supervisor

↓

Assign Tasks

↓

Workers

↓

Collect Results

↓

Answer
```

Simple and widely used.

---

## 2. Sequential Pipeline

Agents execute one after another.

```text
Research

↓

Planner

↓

Writer

↓

Reviewer
```

Useful when outputs naturally feed into the next stage.

---

## 3. Parallel Workers

Independent tasks execute simultaneously.

```text
              Supervisor
                    │
         ┌──────────┼──────────┐
         ▼          ▼          ▼
     Agent A    Agent B    Agent C
         └──────────┼──────────┘
                    ▼
              Merge Results
```

Reduces execution time when tasks are independent.

---

## 4. Handoff Pattern

One agent transfers responsibility to another based on expertise.

Example:

```text
General Assistant

↓

Travel Expert

↓

Payment Agent

↓

Booking Agent
```

This pattern is central to **OpenAI Swarm**.

---

# Popular Multi-Agent Frameworks (2026)

You don't need to master these—just understand what problems they solve.

---

## 1. CrewAI

CrewAI focuses on **role-based collaboration**.

Concepts:

- Agents
- Roles
- Goals
- Tasks
- Crew

Example:

```text
Crew

↓

Researcher

↓

Writer

↓

Reviewer
```

Good for:

- Research
- Report generation
- Content creation
- Business workflows

Think of it as creating a team of specialists.

---

## 2. AutoGen

Developed by Microsoft, AutoGen emphasizes **conversations between agents**.

Example:

```text
Planner Agent

↓

Coder Agent

↓

Tester Agent

↓

Planner

↓

User
```

Suitable for:

- Software engineering
- Iterative debugging
- Collaborative problem solving

One agent can critique or refine another's work.

---

## 3. OpenAI Swarm (Concept)

Swarm explores **lightweight orchestration** based on **handoffs**.

Instead of one controller managing everything, agents can transfer control directly to the most appropriate agent.

Example:

```text
General Assistant

↓

Travel Agent

↓

Payment Agent

↓

Booking Agent
```

Key idea:

> **The conversation moves to the expert, rather than the expert being called as a tool.**

While Swarm itself is experimental, the handoff concept has influenced modern agent orchestration.

---

# Comparison

| Framework    | Primary Focus                      | Best For                                       |
| ------------ | ---------------------------------- | ---------------------------------------------- |
| CrewAI       | Role-based collaboration           | Business workflows, research, reporting        |
| AutoGen      | Conversational agent collaboration | Coding, debugging, iterative tasks             |
| OpenAI Swarm | Lightweight agent handoffs         | Simple multi-agent routing and experimentation |

---

# When Does Multi-Agent Add Value?

Multi-agent architectures are valuable when:

### Complex tasks

Example:

Research → Write → Review

---

### Different expertise

Example:

Legal Agent

Financial Agent

Medical Agent

---

### Parallel execution

Several independent tasks can execute simultaneously.

---

### Large workflows

Many coordinated steps involving different systems.

---

### Long-running business processes

Example:

Approve invoice

↓

Validate vendor

↓

Check budget

↓

Generate payment

↓

Notify finance

---

# When Does It Add Unnecessary Complexity?

Avoid multi-agent systems when:

### Simple Q&A

One LLM is sufficient.

---

### Basic RAG

Retrieval plus one LLM call usually works well.

---

### Single tool invocation

Example:

Calculator

Weather

Database lookup

No need for multiple agents.

---

### Deterministic workflows

If every step is already known, a workflow engine (e.g., LangGraph) is often simpler and more predictable than coordinating multiple autonomous agents.

---

### Small applications

A single well-designed agent is easier to build, test, and maintain.

---

# Decision Guide

```text
Need LLM?

↓

Simple Prompt?

↓

YES → Single LLM

↓

Need Documents?

↓

YES → RAG

↓

Need Tool Calling?

↓

YES → Agent

↓

Need Stateful Workflow?

↓

YES → LangGraph

↓

Need Specialized Independent Experts?

↓

YES → Multi-Agent
```

Move to multi-agent only when there is a clear need for specialization or parallel coordination.

---

# Challenges of Multi-Agent Systems

As the number of agents grows, so do the challenges:

- Increased latency
- Higher token and API costs
- More complex debugging
- Context sharing between agents
- Coordination failures
- Error propagation
- Harder evaluation and testing

This is why observability tools such as LangSmith become increasingly important.

---

# Best Practices

- Start with a **single-agent** design.
- Introduce specialized agents only when one agent becomes a bottleneck.
- Keep each agent focused on a single responsibility.
- Define clear interfaces and responsibilities between agents.
- Prefer deterministic workflows for well-defined business processes.

---

# Key Takeaways

- A **multi-agent system** is a collection of specialized agents collaborating on a common goal.
- The **orchestrator (supervisor)** coordinates work, while **sub-agents** perform specialized tasks.
- **CrewAI** emphasizes role-based teams, **AutoGen** focuses on collaborative conversations, and **OpenAI Swarm** introduced lightweight handoff-based orchestration concepts.
- Multi-agent systems are valuable for complex, specialized, or parallel workflows—but they also increase cost, latency, and operational complexity.
- **Use the simplest architecture that meets your requirements.** In many production systems, a single agent or a LangGraph workflow is sufficient; reserve multi-agent designs for problems that genuinely benefit from specialization and delegation.
