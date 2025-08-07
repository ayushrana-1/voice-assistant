# main_bot.py

## Overview

`main_bot.py` is an advanced, modular Python bot that acts as a multi-modal AI assistant. It can:
- Listen to your voice (audio input)
- Respond with audio (speech output)
- Use Google Gemini for AI chat and tool use
- Generate images, search Google, open websites, control system apps, set reminders, and more
- Integrate with custom tools and APIs

## Features

- **Audio Input/Output:** Uses your microphone and speakers for real-time conversation.
- **Google Gemini Integration:** Connects to Gemini for chat, tool use, and function calling.
- **Tool Functions:** Supports image generation, Google search, website/app opening, system control, anime streaming, reminders, and more.
- **Extensible:** Add your own tools/functions easily.
- **Camera/Screen Support:** Can send camera frames or screenshots to the AI.
- **Reminders:** Set and stop reminders with voice.
- **Robust Error Handling:** Handles exceptions and task groups for async operations.

## Requirements

- Python 3.11+
- `pyaudio`, `opencv-python`, `Pillow`, `mss`, `pywhatkit`, `google-generativeai`, `exceptiongroup`, and other dependencies
- Google Gemini API key (set in `API.py` as `tp2`)
- (Optional) Custom modules: `img2.py`, `saasta_automation.py`, `remember_me.py`

## Usage

```bash
python main_bot.py --mode camera   # Use camera frames
python main_bot.py --mode screen   # (If implemented) Use screen frames
python main_bot.py                 # Default: audio only
```

## How It Works

- **AudioLoop**: Main class that manages audio/video input, output, and AI session.
- **Tools**: Defined as function declarations, called by Gemini as needed.
- **Session**: Connects to Gemini, streams audio/video, receives responses, and handles tool calls.
- **Function Calls**: When Gemini calls a tool, the bot executes the function and returns the result.

## Extending

- Add new tools by editing the `TOOLS` list and implementing the function in the tool call handler.
- Add new system actions or website handlers in the relevant sections.

## Example Tool Call

- **Generate Image:**  
  User: "Draw a cat in a spacesuit."  
  Gemini calls `generate_image`, bot runs `img2.generate_image(prompt)`, returns image.

- **Set Reminder:**  
  User: "Remind me to call mom at 5pm."  
  Gemini calls `set_reminder`, bot runs `remember_me.create_reminder(reminder_text)`.

## File Structure

- `main_bot.py` — Main bot logic
- `img2.py` — Image generation
- `API.py` — API keys/config
- `saasta_automation.py` — Custom automation tools
- `remember_me.py` — Reminder logic

## Troubleshooting

- Make sure all dependencies are installed.
- Ensure your microphone and speakers are working.
- Set your Gemini API key in `API.py`.
- For custom tools, ensure the relevant Python files exist.

