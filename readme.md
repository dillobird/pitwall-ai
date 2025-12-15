# Pitwall AI

Pitwall AI is a terminal-based Formula 1 statistics assistant powered by OpenAI and the [OpenF1 API](https://openf1.org). It can answer natural-language questions about F1 sessions, meetings, drivers, locations (telemetry), and session results by dynamically calling OpenF1 endpoints.

The project is intentionally lightweight and modular, making it easy to extend with additional tools, agents, or interfaces (e.g. Discord bot, web API).

---

## Features

* Natural language F1 queries via OpenAI
* Tool-based access to OpenF1 endpoints:

  * Sessions
  * Meetings
  * Drivers
  * Session results
  * Car location / telemetry data
* Modular architecture (tools, prompts, agent loop separated)
* Simple terminal interface

---

## Requirements

* Python **3.10+** (3.11 recommended)
* An OpenAI API key
* Internet access (for OpenF1 API calls)

---

## Project Structure

```text
pitwall-ai/
├── main.py              # CLI entry point
├── agent.py             # Agent orchestration logic
├── openai_client.py     # OpenAI client initialization
├── prompts.py           # System prompts
├── tool_registry.py     # Tool definitions + dispatcher
├── tools/               # OpenF1 tool implementations
│   ├── sessions.py
│   ├── meetings.py
│   ├── drivers.py
│   ├── location.py
│   └── session_results.py
├── .env.example
├── .gitignore
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:dillobird/pitwall-ai.git
cd pitwall-ai
```

---

### 2. Create and activate a virtual environment

On macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you do not yet have a `requirements.txt`, you can generate one after installing dependencies:

```bash
pip install openai python-dotenv requests
pip freeze > requirements.txt
```

---

### 4. Configure environment variables

#### Option A: Using a `.env` file (recommended for local development)

1. Copy the example file:

```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

> **Important:** `.env` is ignored by Git and should never be committed.

---

#### Option B: Export the variable directly

```bash
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxx"
```

---

## Running the Agent

Start the terminal agent with:

```bash
python main.py
```

You should see:

```text
F1 Agent ready. Type 'exit' to quit.
```

Example queries:

```text
>>> What sessions are available for the 2024 Monaco GP?
>>> Who finished on the podium in the latest race?
>>> Show me the drivers in the most recent qualifying session
>>> Where was driver 44 on track during FP2?
```

Type `exit` to quit.

---

## Notes on the OpenF1 API

* Data is sourced from the public OpenF1 API
* Some endpoints support special values such as:

  * `session_key=latest`
  * date filters (`date_gt`, `date_lt`)
* Availability depends on session timing and OpenF1 coverage

See the official documentation for details:
[https://openf1.org/#api-endpoints](https://openf1.org/#api-endpoints)

---

## Development Tips

* Tool logic lives in `tools/` and should remain OpenAI-agnostic
* To add a new OpenF1 endpoint:

  1. Create a new file in `tools/`
  2. Add a tool definition in `tool_registry.py`
  3. Register it in the dispatcher
* The agent loop in `agent.py` can be reused for other interfaces

---

## Security

* Never commit your OpenAI API key
* Use GitHub’s `users.noreply.github.com` email for commits
* Review `.gitignore` before adding new data outputs or caches

---

## License

This project is provided as-is for personal and educational use. No affiliation with Formula 1, the FIA, or OpenF1 is implied.
