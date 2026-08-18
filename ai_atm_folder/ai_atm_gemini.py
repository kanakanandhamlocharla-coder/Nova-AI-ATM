import base64
import io
import json
import os
import wave

from dotenv.main import load_dotenv
from google import genai
from sarvamai import SarvamAI

from ai_atm_functions import (get_information_by_name, get_transactions_by_name, get_branch_details_by_name)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
api_key_2 = os.getenv("SARVAMAI_API_KEY")

client = genai.Client(api_key=api_key)
client_2 = SarvamAI(api_subscription_key=api_key_2)


system_instruction = """
You are an AI banking assistant for an ATM application.

Your job is to help the user with information about their bank account
using the available banking functions.

STRICT RULES:

1. Never invent, guess, assume, or fabricate banking information.

2. For account-related information such as:
   - customer name
   - account number
   - account type
   - IFSC code
   - phone number
   - balance
   - transactions
   - last transaction
   - any other information stored in the bank database

   ALWAYS use the appropriate function.

3. Only use information returned by the banking functions.
   The database and function results are the only source of truth.

4. Never use your general knowledge to fill in missing banking information.

5. If a function returns that the requested information is unavailable,
   clearly tell the user that the information is not available.

6. Never make up account numbers, balances, transaction amounts,
   dates, names, IFSC codes, or any other banking details.

7. Do not modify, create, or delete banking information.

8. Do not perform banking transactions. You can only provide information
   that the available functions allow you to retrieve.

9. You can answer general questions about how the ATM application works,
   but do not provide information about a user's account unless it comes
   from the appropriate function.

10. If the user asks something completely unrelated to banking, such as:
    "How do I make egg fried rice?"
    politely tell them that you can only help with banking and ATM-related
    questions.

11. Do not provide recipes, entertainment, general knowledge, medical
    advice, or unrelated information.

12. If you don't know something or there is no function available to
    retrieve it, say that you don't have that information rather than
    guessing.

13. Keep answers clear and concise.

14. If the user asks a question that requires multiple pieces of banking
    information, use the appropriate functions to obtain the information
    before answering.
"""

customer_information_tool = {
    "type": "function",
    "name": "get_customer_information_by_name",
    "description": "Returns the customer information by customer name",
    "parameters": {
        "type": "object",
        "properties": {
            "customer_name": {
                "type": "string",
                "description": "Customer name"
            }
        },
        "required": ["customer_name"]
    }
}

customer_transactions_tool = {
    "type": "function",
    "name": "get_customer_transactions_by_name",
    "description": "Returns the customer transactions by customer name",
    "parameters": {
        "type": "object",
        "properties": {
            "customer_name": {
                "type": "string",
                "description": "Customer name"
            }
        },
        "required": ["customer_name"]
    }
}




branch_details_tool = {
    "type": "function",
    "name": "get_branch_details_by_name",
    "description": "Returns the branch details by branch name",
    "parameters": {
        "type": "object",
        "properties": {
            "branch_name": {
                "type": "string",
                "description": "Branch name"
            }
        },
        "required": ["branch_name"]
    }
}

tools = [customer_information_tool, customer_transactions_tool, branch_details_tool]

def generate_tts_audio(text: str) -> bytes:
    response = client.interactions.create(
        model="gemini-3.1-flash-tts-preview",
        input=text,
        response_format={"type": "audio"},
        generation_config={
            "speech_config": [
                {
                    "voice": "Zephyr"
                }
            ]
        }
    )
    pcm_data = base64.b64decode(response.output_audio.data)

    wav_buffer = io.BytesIO()

    with wave.open(wav_buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(pcm_data)

    wav_buffer.seek(0)

    return wav_buffer.read()

def bytes_to_wav(audio):
    wav_buffer = io.BytesIO()
    audio.export(wav_buffer, format="wav")
    wav_buffer.seek(0)
    wav_buffer.name = "recording.wav"
    return wav_buffer

def stt(file, language_code = "en-IN"):
    try:
        response = client_2.speech_to_text.transcribe(
            file=file,
            model="saaras:v3",
            mode="transcribe",
            language_code=language_code
        )
        return response.transcript
    except Exception as e:
        return f"ST ERROR: {e}"

def ask_gemini_text(prompt, interaction_id) -> dict:
    if interaction_id is None:
        interaction = client.interactions.create(
            model="gemini-3.1-flash-lite",
            input=prompt,
            tools=tools,
            system_instruction=system_instruction
        )

    else:
        interaction = client.interactions.create(
            model="gemini-3.1-flash-lite",
            input=prompt,
            tools=tools,
            system_instruction=system_instruction,
            previous_interaction_id=interaction_id
        )


    for step in interaction.steps:
        if step.type == "function_call":

            fc_response = handle_function_calls(step.name, step.arguments, step.id, interaction.id)
            return {
                "text" : fc_response["text"],
                "interaction_id" : fc_response["interaction_id"],
                "audio": fc_response["audio"]
            }
        elif step.type == "model_output":
            response_text = step.content[0].text
            audio_bytes = generate_tts_audio(response_text)
            return {
                "text": response_text,
                "interaction_id": interaction.id,
                "audio": audio_bytes
            }


def handle_function_calls(function_name: str, function_parameters: dict, step_id, interaction_id):
    if function_name == "get_customer_information_by_name":
        customer_name = function_parameters.get("customer_name")
        method_response = get_information_by_name(customer_name)
    elif function_name == "get_customer_transactions_by_name":
        customer_name = function_parameters.get("customer_name")
        method_response = get_transactions_by_name(customer_name)
    elif function_name == "get_branch_details_by_name":
        branch_name = function_parameters.get("branch_name")
        method_response = get_branch_details_by_name(branch_name)

    final_interaction = client.interactions.create(
        model="gemini-3.1-flash-lite",
        input=[
            {
                "type": "function_result",
                "name": function_name,
                "call_id": step_id,
                "result": [{"type": "text", "text": json.dumps(method_response)}],
            }
        ],
        tools=tools,
        system_instruction=system_instruction,
        previous_interaction_id=interaction_id,
    )
    final_text = ""
    for step in final_interaction.steps:
        if step.type == "model_output":
            final_text = step.content[0].text
            break
    audio_bytes = generate_tts_audio(final_text)
    return {
        "text": final_text,
        "interaction_id": final_interaction.id,
        "audio": audio_bytes
    }