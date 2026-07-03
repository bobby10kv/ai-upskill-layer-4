import time
import urllib
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_litellm import ChatLiteLLM

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

def get_time(city: str) -> str:
    """Get time for a given city."""
    return f"It's 1'o clock in {city}!"

SYSTEM_PROMPT = """You are a literary data assistant.

## Capabilities

- `fetch_text_from_url`: loads document text from a URL into the conversation.
Do not guess line counts or positions—ground them in tool results from the saved file."""

@tool
def fetch_text_from_url(url: str) -> str:
    """Fetch the document from a URL.
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; quickstart-research/1.0)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.URLError as e:
        return f"Fetch failed: {e}"
    text = raw.decode("utf-8", errors="replace")
    return text


agent = create_agent(
    model=ChatLiteLLM(model="openai/gpt-4o-mini"),
    tools=[get_weather, get_time, fetch_text_from_url],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the time in kerala?"}]}
)
print(result["messages"][-1].content_blocks)