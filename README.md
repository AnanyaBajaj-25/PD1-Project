# Traveler Insight CLI

A command-line tool that helps travelers prepare for a destination by combining **Wikipedia retrieval** with **LLM-powered synthesis** via [DSPy](https://github.com/stanfordnlp/dspy). Enter any country or city and receive concise, culturally grounded insights—plus thoughtful conversation starters you can use with locals.

## Features

- **Wikipedia-backed context** — Fetches and parses live Wikipedia pages, with automatic disambiguation when a query matches multiple articles.
- **Structured travel briefings** — Generates seven focused sections tailored to pre-trip research:
  - Cultural Etiquette
  - Language & Communication
  - Food & Dining Norms
  - Festivals & Holidays
  - Religion & Spiritual Sites
  - Heritage & Monuments
  - Conversation Starters
- **DSPy-optimized prompts** — Each section uses a dedicated [DSPy Signature](https://dspy.ai/) and `Predict` module, keeping outputs consistent and grounded in retrieved source material.
- **Interactive CLI** — Query multiple destinations in a single session; type `exit` to quit.

## How It Works

```
User input (destination)
        │
        ▼
┌───────────────────┐
│  Wikipedia RAG    │  Resolve page → extract overview + relevant sections
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  DSPy Predictors  │  Seven specialized signatures, each with custom guidelines
└─────────┬─────────┘
          │
          ▼
   Formatted CLI output
```

1. **Retrieve** — The agent looks up the destination on Wikipedia, resolves disambiguation when needed, and pulls an overview plus section text matched by keywords (e.g. *culture*, *cuisine*, *festival*).
2. **Synthesize** — Retrieved text is passed to seven DSPy predictors. Each predictor receives destination context, relevant Wikipedia excerpts, and section-specific writing guidelines.
3. **Display** — `main.py` prints the results in a readable, labeled format.

## Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys) (the project uses `gpt-4o-mini` by default)

## Installation

```bash
git clone https://github.com/<your-username>/dspy-wikipedia-mvp.git
cd dspy-wikipedia-mvp

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
```

The language model is configured in `config.py` (`gpt-4o-mini`, temperature `0.5`, max tokens `700`). Adjust these settings there if you want different model behavior.

## Usage

```bash
python main.py
```

Example session:

```
Welcome to the Traveler Insight CLI! Ask about any destination.
Enter a country or city (or 'exit' to quit): Kyoto

=== Kyoto ===

Cultural Etiquette:
...

Language & Communication:
...

Food & Dining Norms:
...

Festivals & Holidays:
...

Religion & Spiritual Sites:
...

Heritage & Monuments:
...

Conversation Starters:
...
```

## Project Structure

```
dspy-wikipedia-mvp/
├── main.py        # CLI entry point and output formatting
├── agent.py       # WikipediaAgent — retrieval, section extraction, DSPy orchestration
├── signature.py   # DSPy Signature definitions for each output category
├── config.py      # OpenAI / DSPy language model configuration
└── requirements.txt
```

## Tech Stack

| Component | Role |
|-----------|------|
| [DSPy](https://github.com/stanfordnlp/dspy) | Structured LLM prompting and module composition |
| [Wikipedia](https://pypi.org/project/Wikipedia/) | Live article retrieval and section parsing |
| OpenAI (`gpt-4o-mini`) | Text synthesis via DSPy LM backend |
| Python | CLI and orchestration |

## Limitations

- Output quality depends on Wikipedia coverage for the destination; obscure places may have sparse articles.
- Section extraction uses keyword matching against Wikipedia headings—some topics may fall back to the page overview.
- Requires a network connection and a valid OpenAI API key for each query.

## License

This project is provided as-is for educational and personal use.
