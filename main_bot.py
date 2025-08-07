import asyncio
import base64
import io
import os
import sys
import traceback
from img2 import generate_image
import cv2
import pyaudio
import PIL.Image
import mss
from exceptiongroup import ExceptionGroup
import argparse
import pywhatkit as kit
from API import tp2 #API is a file in which all api stored
from google import genai
from google.genai.types import Tool, FunctionDeclaration, FunctionResponse
from saasta_automation import *
if sys.version_info < (3, 11, 0):
    import taskgroup, exceptiongroup
    asyncio.TaskGroup = taskgroup.TaskGroup
    asyncio.ExceptionGroup = exceptiongroup.ExceptionGroup

FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 12000
RECEIVE_SAMPLE_RATE = 25000
CHUNK_SIZE = 1024

MODEL = "models/gemini-2.0-flash-live-001"
DEFAULT_MODE = "audio"

client = genai.Client(api_key=tp2,http_options={"api_version": "v1beta"})

# Define tool functions
TOOLS = [
    Tool(
        function_declarations=[
            FunctionDeclaration(
                name="generate_image",
                description="Generate an image from prompt",
                parameters={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Prompt to generate image"
                        }
                    },
                    "required": ["prompt"]
                }
            ),
            FunctionDeclaration(
                name="google_search",
                description="Search on Google",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query to look up on Google"
                        }
                    },
                    "required": ["query"]
                }
            ),
            FunctionDeclaration(
                name="open_website",
                description="Open various websites and applications",
                parameters={
                    "type": "object",
                    "properties": {
                        "site": {
                            "type": "string",
                            "description": "Website or app to open (youtube, gmail, github, etc.)"
                        }
                    },
                    "required": ["site"]
                }
            ),
            FunctionDeclaration(
                name="system_control",
                description="Control system functions",
                parameters={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "System action to perform (refresh, notepad, cmd, etc.)"
                        }
                    },
                    "required": ["action"]
                }
            ),
            FunctionDeclaration(
                name="watch_anime",
                description="Open anime streaming website",
                parameters={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            FunctionDeclaration(
                name="set_reminder",
                description="Set a reminder with voice notification that plays until stopped",
                parameters={
                    "type": "object",
                    "properties": {
                        "reminder_text": {
                            "type": "string",
                            "description": "Reminder text with time (e.g. 'remind me to do homework at 10pm')"
                        }
                    },
                    "required": ["reminder_text"]
                }
            ),
            FunctionDeclaration(
                name="stop_reminder",
                description="Stop all currently playing reminders",
                parameters={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
    )
]

CONFIG ={
    "response_modalities": ["AUDIO"],
    "speech_config": {
        "voice_config": {"prebuilt_voice_config": {"voice_name": "Kore"}}
    },
}
# {
#     "response_modalities": ["AUDIO"],
#     "tools": TOOLS
# }

pya = pyaudio.PyAudio()

class AudioLoop:
    def __init__(self, video_mode=DEFAULT_MODE):
        self.video_mode = video_mode
        self.audio_in_queue = None
        self.out_queue = None
        self.session = None

    def _get_frame(self, cap):
        ret, frame = cap.read()
        if not ret:
            return None
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = PIL.Image.fromarray(frame_rgb)
        img.thumbnail([1024, 1024])
        image_io = io.BytesIO()
        img.save(image_io, format="jpeg")
        image_io.seek(0)
        return {"mime_type": "image/jpeg", "data": base64.b64encode(image_io.read()).decode()}

    async def get_frames(self):
        cap = await asyncio.to_thread(cv2.VideoCapture, 0)
        while True:
            frame = await asyncio.to_thread(self._get_frame, cap)
            if frame is None:
                break
            await asyncio.sleep(1.0)
            await self.out_queue.put(frame)
        cap.release()

    async def listen_audio(self):
        mic_info = pya.get_default_input_device_info()
        self.audio_stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )
        while True:
            data = await asyncio.to_thread(self.audio_stream.read, CHUNK_SIZE, exception_on_overflow=False)
            await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})

    async def send_realtime(self):
        while True:
            msg = await self.out_queue.get()
            await self.session.send(input=msg)

    async def receive_audio(self):
        while True:
            turn = self.session.receive()
            async for response in turn:
                if data := response.data:
                    self.audio_in_queue.put_nowait(data)
                    continue
                if text := response.text:
                    print(f"\n🧠 Gemini: {text}")

                if response.tool_call:
                    function_responses = []
                    for fc in response.tool_call.function_calls:
                        print(f"\n🛠 Tool Call: {fc.name}")
                        if fc.name == "generate_image":
                            prompt = fc.args.get("prompt", "default image")
                            print(f"🖼️ Generating image for: {prompt}")
                            result = generate_image(prompt)
                            function_responses.append(FunctionResponse(id=fc.id, name=fc.name, response={"result": result}))

                        elif fc.name == "google_search":
                            query = fc.args.get("query", "")
                            print(f"🔍 Searching Google for: {query}")
                            kit.search(query)
                            function_responses.append(FunctionResponse(id=fc.id, name=fc.name, response={"status": f"Searched Google for: {query}"}))

                        elif fc.name == "open_website":
                            site = fc.args.get("site", "youtube")
                            print(f"🌐 Opening website: {site}")
                            if site == "youtube":
                                youtube()
                            elif site == "gmail":
                                gmail()
                            elif site == "github":
                                github()
                            elif site == "spotify":
                                spotify()
                            elif site == "chatgpt":
                                chatgpt()
                            elif site == "whatsapp":
                                whatsapp()
                            elif site == "telegram":
                                telegram()
                            function_responses.append(FunctionResponse(id=fc.id, name=fc.name, response={"status": f"Opening website: {site}"}))

                        elif fc.name == "system_control":
                            action = fc.args.get("action", "refresh")
                            print(f"🖥️ Controlling system: {action}")
                            if action == "refresh":
                                refresh()
                            elif action == "notepad":
                                notepad()
                            elif action == "cmd":
                                cmd()
                            elif action == "paint":
                                paint()
                            elif action == "explorer":
                                file_explorer()
                            function_responses.append(FunctionResponse(id=fc.id, name=fc.name, response={"status": f"Controlling system: {action}"}))

                        elif fc.name == "watch_anime":
                            print(f"🎞️ Watching anime")
                            watch_anime()
                            function_responses.append(FunctionResponse(id=fc.id, name=fc.name, response={"status": "Watching anime"}))

                        elif fc.name == "set_reminder":
                            reminder_text = fc.args.get("reminder_text", "")
                            print(f"⏰ Setting reminder: {reminder_text}")
                            from remember_me import create_reminder
                            result = create_reminder(reminder_text)
                            function_responses.append(FunctionResponse(
                                id=fc.id, 
                                name=fc.name, 
                                response={
                                    "status": result,
                                    "instructions": "The reminder will play at the specified time. Say 'stop reminder' to stop the reminder when it plays."
                                }
                            ))

                        elif fc.name == "stop_reminder":
                            print("🔕 Stopping all reminders")
                            from remember_me import stop_reminders
                            result = stop_reminders()
                            function_responses.append(FunctionResponse(
                                id=fc.id,
                                name=fc.name,
                                response={"status": result}
                            ))

                    await self.session.send_tool_response(function_responses=function_responses)

            while not self.audio_in_queue.empty():
                self.audio_in_queue.get_nowait()

    async def play_audio(self):
        stream = await asyncio.to_thread(pya.open, format=FORMAT, channels=CHANNELS, rate=RECEIVE_SAMPLE_RATE, output=True)
        while True:
            bytestream = await self.audio_in_queue.get()
            await asyncio.to_thread(stream.write, bytestream)

    async def run(self):
        try:
            async with client.aio.live.connect(model=MODEL, config=CONFIG) as session, asyncio.TaskGroup() as tg:
                self.session = session
                self.audio_in_queue = asyncio.Queue()
                self.out_queue = asyncio.Queue(maxsize=5)
                tg.create_task(self.send_realtime())
                tg.create_task(self.listen_audio())
                if self.video_mode == "camera":
                    tg.create_task(self.get_frames())
                tg.create_task(self.receive_audio())
                tg.create_task(self.play_audio())

        except asyncio.CancelledError:
            pass
        except ExceptionGroup as EG:
            self.audio_stream.close()
            traceback.print_exception(EG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default=DEFAULT_MODE, choices=["camera", "screen", "none"])
    args = parser.parse_args()
    main = AudioLoop(video_mode=args.mode)
    asyncio.run(main.run())
