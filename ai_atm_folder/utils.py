import base64
import os
from io import BytesIO

from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

api_key = os.getenv("SARVAMAI_API_KEY")

client = SarvamAI(api_subscription_key=api_key)

def stt(file):
    try:
        audio_base64 = base64.b64encode(file.getvalue()).decode("utf-8")
        audio_bytes = base64.b64decode(audio_base64)
        audio_file = BytesIO(audio_bytes)
        audio_file.name = "recording.wav"

        response = client.speech_to_text.transcribe(
            file=audio_file,
            model="saaras:v3",
            mode="transcribe",
        )
        return response.transcript

    except Exception as e:
        print(f"Error: {e}")