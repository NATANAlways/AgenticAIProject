# LangGraph Agentic AI

A configurable, multi-agent chatbot platform built with [LangGraph](https://langchain-ai.github.io/langgraph/) and [Streamlit](https://streamlit.io/). Pick an LLM provider and a use case from the sidebar, and the app builds and runs a different agent graph behind the scenes — from a simple chatbot to a tool-using web search agent to a fully autonomous news-fetching pipeline.

## Features

- **Basic Chatbot** — a single-node conversational agent for direct Q&A.
- **Chatbot with Web** — a tool-using agent that conditionally routes between the LLM and a [Tavily](https://tavily.com/) search tool, letting the model decide when it needs live web results before answering.
- **AI News** — an autonomous `fetch → summarize → save` pipeline that pulls the latest AI news for a chosen time frame (daily/weekly/monthly), summarizes it into Markdown with the LLM, and saves it under `AINews/`.
- **Config-driven UI** — LLM providers, models, and use cases are defined in a single `.ini` file, so the sidebar can be extended without touching UI code.

## Requirements

- Python 3.10+
- A [Groq API key](https://console.groq.com/keys) (free tier available)
- A [Tavily API key](https://app.tavily.com/keys) — only needed for the "Chatbot with web" and "AI News" use cases

## Setup

```bash
# 1. Clone and enter the project
git clone <this-repo-url>
cd AgenticAI

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Running the app

```bash
streamlit run app.py
```

This starts the app at `http://localhost:8501`.

## Usage

1. **Select LLM** — currently supports Groq.
2. **Select Model** — choose a Groq-hosted model (e.g. `llama-3.1-8b-instant`).
3. **Enter your Groq API key** — required to initialize the model; entered per-session, never stored on disk.
4. **Select usecase**:
   - `Basic Chatbot` — type a message in the chat box at the bottom and press enter.
   - `Chatbot with web` — also requires a Tavily API key (a field appears once selected). The agent decides on its own whether to search the web before responding.
   - `AI News` — also requires a Tavily API key. Pick a time frame (Daily/Weekly/Monthly) and click **Fetch Latest AI News**. The summarized digest is displayed in the app and saved to `AINews/<timeframe>_summary.md`.

## Architecture

### Overview

```
app.py
  └─ main.load_langgraph_agentic_app()
       ├─ LoadStreamlitUI          → renders sidebar, collects user selections
       ├─ GroqLLM                  → initializes the chosen LLM
       ├─ GraphBuilder             → builds a LangGraph StateGraph for the selected use case
       └─ DisplayResultStreamlit   → runs the graph and renders output as chat messages
```

The app is driven by a single shared `State` (a `TypedDict`, see `src/langgraphagenticai/state/state.py`) that flows through each graph's nodes. Every use case is modeled as its own **LangGraph `StateGraph`**, built independently in `GraphBuilder`, so adding a new agent behavior means adding a new node/edge configuration rather than modifying a shared prompt chain.

### Project structure

```
app.py                                  Entry point — launches the Streamlit app
requirements.txt                        Python dependencies
AINews/                                 Saved AI News summaries (generated at runtime)

src/langgraphagenticai/
├── main.py                             Orchestrates UI → LLM → graph → display
├── llm/
│   └── groqllm.py                      Groq LLM client initialization
├── graph/
│   └── graph_builder.py                Builds the LangGraph StateGraph per use case
├── nodes/
│   ├── basic_chatbot_node.py           Node for the Basic Chatbot graph
│   ├── chatbot_with_Tool_node.py       Node(s) for the web-search chatbot graph
│   └── ai_news_node.py                 Nodes for the AI News fetch/summarize/save graph
├── tools/
│   └── search_tool.py                  Tavily search tool + tool node factory
├── state/
│   └── state.py                        Shared graph State schema
└── ui/
    ├── uiconfig.py                     Reads uiconfig.ini
    ├── uiconfig.ini                    LLM options, models, and use cases (edit to extend)
    └── streamlitui/
        ├── loadui.py                   Renders the sidebar and collects user input
        └── displayresult.py            Runs the graph and renders results in the chat UI
```

### Graphs per use case

**Basic Chatbot** (`graph_builder.basic_chatbot_build_graph`)

```
START → chatbot → END
```

A single node that invokes the LLM directly on the conversation history.

**Chatbot with web** (`graph_builder.chatbot_with_tools_build_graph`)

```
START → chatbot ⇄ tools
           │
           └─→ END
```

The LLM is bound to the Tavily search tool. After each `chatbot` step, `tools_condition` inspects the model's response: if it requested a tool call, the graph routes to the `tools` node (which executes the search and returns results to `chatbot`); otherwise it routes straight to `END`.

**AI News** (`graph_builder.ai_news_builder_graph`)

```
START → fetch_news → summarize_news → save_result → END
```

A linear, fully autonomous pipeline:
1. `fetch_news` — queries Tavily for recent AI news within the selected time range.
2. `summarize_news` — prompts the LLM to summarize the articles into a structured Markdown digest.
3. `save_result` — writes the digest to `AINews/<timeframe>_summary.md`.

### Configuration

Sidebar options are driven by `src/langgraphagenticai/ui/uiconfig.ini`:

```ini
[DEFAULT]
PAGE_TITLE = LangGraph: Build Sequetial Agentic AI graph
LLM_OPTIONS = Groq
USECASE_OPTIONS = Basic Chatbot, Chatbot with web, AI News
GROQ_MODEL_OPIONS = llama-3.1-8b-instant, openai/gpt-oss-120b, qwen/qwen3.6-27b, whisper-large-v3-turbo
```

To add a new model or use case, add it to the relevant comma-separated list — no UI code changes required for the dropdown itself (though a new use case still needs a corresponding graph in `graph_builder.py` and a branch in `displayresult.py`).

## Notes

- API keys are entered per-session through the UI and are not persisted to disk.
- The `AINews/` directory is created automatically on first use of the AI News feature.
