# Layer 4 — Agents & Orchestration

---

## What is an Agent?

An **AI agent** is an LLM-powered system that can **perceive**, **reason**, and **act** using tools, then **observe** results and continue until a goal is met.

**Core loop** (from `notes/react-pattern.md` + agent fundamentals):

- User goal
- Perceive (inputs, history, retrieved docs, tool outputs)
- Reason (decide next step)
- Act (call tool / API / DB / run code)
- Observe (result or error)
- Repeat until done

### Chatbot vs Agent (practical difference)

- A **simple chatbot** is usually “single prompt → single response”.
- An **agent** can do multiple steps and can recover from failures (retry, alternate tool, ask for missing data).

---

## Tool calling: definition, workflow, and patterns

From `notes/tool.md` (summarized):

### What tool calling is

**Tool calling** is when the model decides it needs an external capability, emits a **structured** request (tool + arguments), your **application executes** it, and the model uses the result.

**Workflow**:

- User question
- LLM decides “need tool?”
- LLM emits tool name + structured args
- App executes tool (LLM does **not** run code)
- Tool result returned to LLM
- Final answer

### Common patterns

- **Single**: one question → one tool
- **Sequential**: tool A output feeds tool B
- **Conditional**: sometimes no tool needed
- **Parallel**: run independent tools concurrently (latency reduction)
- **Agentic loop**: repeat reason → tool → observe until done

### Best practices (engineering)

- Keep tools **focused** and inputs **typed/structured**
- Validate tool arguments and handle failures with **structured errors**
- Expose only the **minimum** toolset needed per task
- If the output must be exact, require **tool provenance** and validate results

---

## ReAct: Reason + Act (foundation of many agents)

From `notes/react-pattern.md` (summarized):

**ReAct** is a design/prompting pattern where the model alternates between **reasoning** and **acting** (tool calls), using observations to continue until it reaches a final answer.

**Loop shape**:

- Question → Thought → Action → Observation → Thought → … → Answer

### When ReAct is a good fit

- Multi-step tasks
- Tasks requiring tools/APIs/DBs
- Anything where intermediate results must inform the next step

### Trade-offs

- More model calls → higher latency/cost
- Weak tool descriptions → wrong tool selection
- Unbounded loops → cap steps and define “done” conditions

## Choosing the right pattern: API vs RAG vs Agent

Adapted from `notes/api-rag-agent.md`:

- **Use a plain model/API call** when the task is self-contained:
  - translation, summarization, rewriting, classification
- **Use RAG** when you need *knowledge* from documents you control:
  - “answer questions from company docs”
- **Use an Agent** when you need *actions* or multi-step tool usage:
  - DB lookups + decisions, refunds, booking meetings, Slack/email workflows

**Decision tree (mental model)**:

- Need an LLM?
  - Need external knowledge from your docs? → **RAG**
  - Need actions (tools/APIs/DB/code)? → **Agent**
  - Otherwise → **Single LLM call**

---

## LangChain / LangGraph: practical mental model

- **LangChain**: building blocks for models, tools, and “agent-like” loops.
- **LangGraph**: explicit **stateful workflows** (nodes + edges + checkpoints). Great when the process is known and you want predictable control.

**Design rule of thumb**:

- Put **deterministic work** in normal code/tooling.
- Use the LLM for **routing, planning, interpretation, and user-facing text**.

### Checkpointing / memory

Checkpointing helps with:

- debug/replay (“what happened?”)
- resumability
- isolating runs by conversation thread (e.g., `thread_id`)

---

## Multi-agent systems (awareness level)

From `notes/mutli-agents` (summarized):

A **multi-agent system** is multiple specialized agents collaborating on a larger task.

### Common patterns

- **Supervisor/orchestrator**: delegates to specialist sub-agents and merges outputs
- **Sequential pipeline**: research → plan → write → review
- **Parallel workers**: independent tasks in parallel, then merge
- **Handoffs**: control transfers to the most appropriate specialist (Swarm-style concept)

### When multi-agent adds value

- Tasks are complex and naturally separable (research vs coding vs review)
- Different expertise is genuinely required
- Parallel execution reduces wall-clock time

### When it adds unnecessary complexity

- Simple Q&A
- Basic RAG
- Single tool invocation
- Deterministic business workflows (a workflow graph is usually simpler)

### Challenges to call out

- Higher latency/cost
- Harder debugging and evaluation
- Context-sharing complexity and coordination failures

Principle: **start single-agent**; add specialization only when you can name the bottleneck.

---

## Production checklist (minimum viable)

### Reliability

- Cap steps / define “done” conditions
- Validate tool args and outputs
- Enforce structured outputs (JSON) and retry on parse errors
- Separate deterministic computation from LLM narration

### Observability

- Trace model calls + tool calls (inputs/outputs, latency, cost)
- Capture tool errors and timeouts
- Isolate runs by thread and checkpoint state

### Safety

- Treat retrieved text/tool outputs as untrusted input (prompt injection awareness)
- Avoid sending secrets/PII to external APIs
- Prefer rule-based/deterministic systems when they are clearly sufficient

