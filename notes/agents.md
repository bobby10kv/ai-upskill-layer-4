## What Are AI Agents?

An **AI agent** is an application powered by an LLM that can **perceive its environment, reason about a goal, and take actions** to achieve that goal. Unlike a simple chatbot that generates a single response, an agent can make decisions, use tools, observe results, and continue working until the task is complete.

The core idea is often summarized as the **Perceive → Reason → Act** loop.

```text
        User Goal
            │
            ▼
      ┌───────────┐
      │ Perceive  │
      └───────────┘
            │
            ▼
      ┌───────────┐
      │  Reason   │
      └───────────┘
            │
            ▼
      ┌───────────┐
      │    Act    │
      └───────────┘
            │
            ▼
     Observe Result
            │
            └──────────────┐
                           ▼
                     Reason Again
```

---

## 1. Perceive

The agent gathers information about the current situation.

This information may come from:

* User input
* Conversation history
* Retrieved documents (RAG)
* Database queries
* APIs
* File system
* Search engines
* Tool outputs

Think of this as the agent **understanding the current state**.

### Example

User asks:

> "Book a meeting with Alice tomorrow afternoon."

The agent perceives:

* User wants to schedule a meeting
* Participant: Alice
* Date: Tomorrow
* Time: Afternoon

---

## 2. Reason

The LLM analyzes the goal and decides **what should happen next**.

Typical reasoning includes:

* Do I have enough information?
* Which tool should I use?
* Should I search first?
* Do I need clarification?
* What sequence of actions is required?

This is where patterns like **ReAct (Reason + Act)** come into play.

### Internal reasoning (conceptual)

```text
Thought:
I need to check the user's calendar.

Thought:
I should use the Calendar API.

Thought:
If there is no available slot,
suggest alternatives.
```

> Note: Modern LLM APIs often perform this reasoning internally. You generally don't expose the model's private reasoning to users.

---

## 3. Act

The agent executes one or more actions using external tools.

Examples:

* Search the web
* Query a database
* Call an API
* Send an email
* Execute Python code
* Update a CRM
* Book a calendar event

Example:

```text
Action:
Call Calendar API

↓

Available:
3 PM - 4 PM

↓

Book Meeting

↓

Send Confirmation
```

---

## 4. Observe

After acting, the agent receives feedback.

Examples:

```text
Meeting booked successfully.
```

or

```text
Calendar API failed.
```

or

```text
No available slots found.
```

The observation becomes new input for the next reasoning step.

---

## The Complete Agent Loop

```text
User:
Book a meeting with Alice tomorrow.

        │
        ▼
Perceive
- Understand intent
- Extract date and attendee

        │
        ▼
Reason
- Need calendar availability

        │
        ▼
Act
- Call Calendar API

        │
        ▼
Observe
- 3 PM available

        │
        ▼
Reason
- Suitable slot found

        │
        ▼
Act
- Create meeting
- Send invitation

        │
        ▼
Observe
- Success

        │
        ▼
Respond to User
```

---

## Example: Weather Agent

**User:** *"Should I carry an umbrella today?"*

```text
Perceive
↓

User asks about today's weather

↓

Reason
↓

Need current weather data

↓

Act
↓

Call Weather API

↓

Observe
↓

Rain expected in the afternoon

↓

Reason
↓

Recommend carrying an umbrella

↓

Respond
```

---

## How This Differs from a Simple Chatbot

### Simple LLM

```text
User
   │
   ▼
LLM
   │
   ▼
Answer
```

* Single prompt → single response
* No tool usage
* No planning
* No execution

---

### Agent

```text
User
   │
   ▼
Perceive
   │
   ▼
Reason
   │
   ▼
Use Tool
   │
   ▼
Observe
   │
   ▼
Reason Again
   │
   ▼
Final Answer
```

* Can use external tools
* Can perform multiple steps
* Can adapt based on results
* Can recover from failures or request clarification

---

## Real-World Examples

| Application                                                | Agent?    | Why                                                                    |
| ---------------------------------------------------------- | --------- | ---------------------------------------------------------------------- |
| Translate text                                             | ❌         | Single LLM response                                                    |
| Summarize a PDF                                            | ❌         | Single inference                                                       |
| Chat with company documents (RAG)                          | Usually ❌ | Retrieves context, then answers                                        |
| GitHub Copilot Agent                                       | ✅         | Reads files, edits code, runs tests, iterates                          |
| Customer support bot that checks orders and issues refunds | ✅         | Uses APIs, reasons about next steps, performs actions                  |
| Travel booking assistant                                   | ✅         | Searches flights, compares options, books tickets, sends confirmations |

---

## Key Takeaways

* **Perceive**: Gather information from the user and the environment.
* **Reason**: Decide what needs to happen next.
* **Act**: Execute actions using tools or external systems.
* **Observe**: Evaluate the results and continue if necessary.

This iterative **Perceive → Reason → Act → Observe** cycle is what distinguishes an AI agent from a simple prompt-response application.
