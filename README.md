# IDQuest
IDQuest is a powerful username availability checker that scans hundreds of social, gaming, programming, and other platforms to help you find if your desired username is taken or available.

---

## Features
- Asynchronous requests for fast and efficient username checks.
- Checks across multiple categories: Social Media, Programming, Gaming, Finance, and more.
- Clear status output with "Available," "Taken," "Warning," or "Timeout".
- Dynamic spinner animation during scanning to show progress.
- Easy customization by updating the JSON platform list.

## Installation
- download / clone this repository
- use `pip install -r requirements.txt`
- after installing dependencies use `python idquest.py`
- and you're good to go!

## Preview
```bash
─────────────────────────────────────────────
Platform               | Status
─────────────────────────────────────────────
Facebook               | ❌ Taken or Unknown
GitHub                 | ✅ Available
Instagram              | ❌ Taken or Unknown
Twitter                | ✅ Available
... (more platforms)
─────────────────────────────────────────────
Summary: 15 taken, 20 available, 3 warnings/errors
─────────────────────────────────────────────
```
