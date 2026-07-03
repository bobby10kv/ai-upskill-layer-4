import re
import sys
from typing import Literal, NotRequired, TypedDict

from langgraph.graph import END, StateGraph


Op = Literal["+", "-", "*", "/"]


class CalcState(TypedDict):
    expression: str
    a: NotRequired[float]
    b: NotRequired[float]
    op: NotRequired[Op]
    result: NotRequired[float]
    error: NotRequired[str]
    answer: NotRequired[str]


_EXPR_RE = re.compile(
    r"^\s*(?P<a>-?\d+(?:\.\d+)?)\s*(?P<op>[+\-*/])\s*(?P<b>-?\d+(?:\.\d+)?)\s*$"
)


def parse_expression(state: CalcState) -> CalcState:
    m = _EXPR_RE.match(state["expression"])
    if not m:
        return {
            **state,
            "error": "Unsupported expression. Use a simple binary form like: 12 * 3",
        }
    return {
        **state,
        "a": float(m.group("a")),
        "b": float(m.group("b")),
        "op": m.group("op"),  # type: ignore[typeddict-item]
    }


def compute(state: CalcState) -> CalcState:
    if state.get("error"):
        return state

    a = state["a"]
    b = state["b"]
    op = state["op"]

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        if b == 0:
            return {**state, "error": "Division by zero."}
        result = a / b
    else:
        return {**state, "error": f"Unknown operator: {op!r}"}

    return {**state, "result": result}


def format_answer(state: CalcState) -> CalcState:
    if state.get("error"):
        return {**state, "answer": f"Error: {state['error']}"}
    return {**state, "answer": f"{state['expression'].strip()} = {state['result']}"}


def build_graph():
    g = StateGraph(CalcState)
    g.add_node("parse", parse_expression)
    g.add_node("compute", compute)
    g.add_node("format", format_answer)

    g.set_entry_point("parse")
    g.add_edge("parse", "compute")
    g.add_edge("compute", "format")
    g.add_edge("format", END)

    return g.compile()


def main() -> None:
    expr = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""
    if not expr:
        expr = input("Enter expression (e.g., 452 * 198): ").strip()

    graph = build_graph()
    out = graph.invoke({"expression": expr})
    print(out["answer"])


if __name__ == "__main__":
    main()

