# AI-bot project

An free tier Gemini2.0 based AI-bot with the read/write/execute functionality withing the working directory. Is generally restricted to the workdir, but, if you actually want to use it, be careful. And maybe a bit afraid.

The code is heavily commented by me, in case you need to know how things work. If there are typos, it's code fault, not mine. Printing the candidates ("the thinking proccess of the LLM", more or less) is enabled by default; if you need to turn it off, there's an easily spotted commented block in main.py, that I will totally move to config one day.

## Installation

```bash
git clone https://github.com/HalfCodedPrince/ai-bot.git
cd ai-bot
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## config.py

Config file, located in root.

```python
# maximum amount of character the app will allow the LLM to read
MAX_CHARS = 10000

# working directory, where the LLM is contained
WORKING_DIR = "./calculator"

# maximum amount of times the LLM refines the answer:
MAX_ITER = 20

# current system prompt
SYSTEM_PROMPT = """ """
```

## tools.py

A dictionary of all the function LLM can "see" and "use".

## Usage

After installing, run:

```bash
python main.py "Explain my code in the calculator folder"
```

First argument: user prompt
Additional arguments (optional): parameters passed into process\_response

## architecture 

```
ai-bot/
├── config.py          ← Constants and optional `AppConfig`
├── tools.py           ← Tool schemas + FUNCTION_DICT central registry
├── main.py            ← CLI entrypoint + loop orchestration
└── functions/         ← Tool implementations and file I/O
    ├── get_files_info.py
    ├── get_file_content.py
    ├── write_file
    ├── run_python_file.py
    ├── call_function.py
    └── process_response.py
```