Tenka AI

Tenka is a Windows desktop voice assistant starter that listens for a wake word, understands a small set of commands, and can perform safe PC actions.

Project structure:

- `main.py`: assistant loop
- `brain/logic.py`: command routing
- `brain/actions.py`: safe desktop actions
- `speech/listen.py`: microphone input and wake-word listening
- `speech/speak.py`: Piper offline voice output with Windows fallback

Current skills:

- Wake word: `hello`
- Open apps: `notepad`, `calculator`, `paint`, `cmd`, `powershell`, `explorer`
- Open folders: `desktop`, `documents`, `downloads`, `pictures`
- Open websites: `google`, `youtube`, `gmail`, `github`, `spotify`, or a full URL
- Search the web: `search for python tutorials`
- Basic answers: time, date, who it is, help, and system info

Safety:

- High-risk commands like shutdown, restart, and destructive operations are blocked by default.
- Piper is the preferred offline voice engine.
- If Piper is not installed or a model is not configured, Tenka falls back to the built-in Windows voice when possible.

Microphone selection:

- By default Tenka uses the system default microphone.
- To force a specific mic, set `TENKA_MICROPHONE_NAME` to part of the microphone name shown at startup.
- Example:

```powershell
$env:TENKA_MICROPHONE_NAME = "C-Media"
.\venv\Scripts\python.exe main.py
```

Run:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
.\venv\Scripts\python.exe main.py
```

Then edit `.env` and set your Piper model path.

Recommended offline female voice setup:

- Install Piper so `piper` is available on your system, or set `PIPER_COMMAND` to `piper.exe`
- Download a voice model and its matching config file
- Put them in a local folder such as `voices/`
- Set `PIPER_MODEL` in `.env` to the `.onnx` file path

Example:

```env
PIPER_COMMAND=piper
PIPER_MODEL=E:\Tenka-AI\voices\en_US-lessac-medium.onnx
```

Piper notes:

- Piper needs both the `.onnx` model file and the matching `.onnx.json` config file in the same location.
- The Piper project documents running the CLI with text on standard input and `--model ... --output_file ...`, which is the pattern this project uses.
- A good starting English voice is `en_US-lessac-medium`.

Run tests:

```powershell
.\venv\Scripts\python.exe -m unittest
```
