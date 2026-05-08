# Moody Chatbot

A small mood-based AI chatbot that supports both a terminal interface and a styled Streamlit web UI. The bot can respond in different tones, making it easy to switch between playful, calm, intense, or cheerful conversations.

Deployed Link: https://moodychatbot-bknrewlrteokopyeyp2mtc.streamlit.app/

## Tech Stack

| Layer | Stack |
| --- | --- |
| Language | Python |
| LLM Provider | Mistral AI |
| Model Integration | LangChain, langchain-mistralai, langchain-core |
| UI | Streamlit |
| Environment Management | python-dotenv |
| Supporting Packages | requests, tiktoken, FAISS, FastAPI, Uvicorn, langgraph, langchain-community, langchain-openai, langchain-google-genai, langchain-groq, langchain-huggingface |

## What It Does

- Lets the user choose a mood before chatting.
- Supports four moods: Happy, Sad, Angry, and Funny.
- Runs as a CLI chatbot in the terminal.
- Runs as a polished Streamlit app in the browser.
- Uses a Mistral chat model to generate responses.

## Project Layout

- [chatbot.py](chatbot.py) - terminal-based chatbot entry point.
- [ui.py](ui.py) - Streamlit-based chatbot interface.
- [requirements.txt](requirements.txt) - Python dependencies.
- [README.md](README.md) - project overview and usage guide.
- [babel.json](babel.json) - local configuration file used by the workspace.

## Screens And Flow

The project has two ways to interact with the assistant:

1. CLI mode through [chatbot.py](chatbot.py), where you pick a mood and type messages directly in the terminal.
2. Web mode through [ui.py](ui.py), where you select a mood from the Streamlit interface and continue the conversation in a richer visual layout.

Both entry points rely on the same mood logic and the same underlying Mistral-powered chat model.

## Features

- Mood-based prompting for personality changes.
- Persistent conversation flow during a session.
- Streamlit UI with custom gradients and mood cards.
- Graceful handling for API or network errors in the UI.
- Simple local setup for development and testing.

## Requirements

- Python 3.10 or newer is recommended.
- A valid Mistral API key.
- Internet access for model requests.

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment.

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your API key:

```env
MISTRAL_API_KEY=your_api_key_here
```

## Run The CLI Chatbot

```bash
python chatbot.py
```

When the CLI starts, choose a mood from the menu and then keep chatting until you enter `0`.

## Run The Streamlit App

```bash
streamlit run ui.py
```

The web app shows mood cards, a styled chat area, and a guided sidebar so you can switch tones quickly.

## How It Works

1. The app loads environment variables with `python-dotenv`.
2. A mood selection sets the system prompt for the conversation.
3. User messages are sent to the Mistral model through LangChain.
4. The assistant response is added back into the conversation history.
5. The Streamlit UI reruns to keep the chat view updated after each message.

## Configuration

- `MISTRAL_API_KEY` is required for model access.
- The model currently used in both entry points is `mistral-small-2506`.
- If you want to change tone behavior, update the mood system prompts in [chatbot.py](chatbot.py) and [ui.py](ui.py).

## Troubleshooting

- If the app cannot reach the model, verify the API key inside `.env`.
- If Streamlit does not start, confirm the virtual environment is activated and dependencies are installed.
- If the CLI appears to ignore the selected mood, check the mood prompt logic in [chatbot.py](chatbot.py).

## Version Control Notes

- Keep [README.md](README.md), [chatbot.py](chatbot.py), [ui.py](ui.py), and [requirements.txt](requirements.txt) in source control.
- Do not commit `.env` or `.venv/`.

## Notes

- [chatbot.py](chatbot.py) is for terminal use.
- [ui.py](ui.py) is the browser-based interface.
- The Streamlit interface is designed to reset the chat when a new mood is selected.
