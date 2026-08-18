import streamlit as st

from ai_atm_gemini import ask_gemini_text, bytes_to_wav, stt


from audiorecorder import audiorecorder

st.set_page_config(page_title="ATM Simulator", layout="wide", initial_sidebar_state="collapsed")



def load_css():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 100% !important
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )


load_css()



if "messages" not in st.session_state:
    st.session_state.messages = []

if "interaction_id" not in st.session_state:
    st.session_state.interaction_id = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

        if "audio" in msg and msg["audio"]:
            st.audio(msg["audio"], format="audio/wav")

transcribed_text = None
audio_bytes = audiorecorder()
if audio_bytes:
    wav_file = bytes_to_wav(audio_bytes)
    transcribed_text = stt(wav_file, language_code="en-IN")

    if transcribed_text:
        st.session_state["pending_transcript"] = transcribed_text

if "pending_transcript" in st.session_state and st.session_state["pending_transcript"]:
    transcribed_text = st.session_state["pending_transcript"]
    


prompt = st.chat_input("Ask anything...")

message = prompt or transcribed_text

if message:
    if "pending_transcript" in st.session_state:
        st.session_state["pending_transcript"] = None
    with st.chat_message("user"):
        st.write(message)
    st.session_state.messages.append(
        {
            "role": "user",
            "text": message,
        }
    )

    with st.chat_message("assistant"):
        with st.spinner("AI's Replying"):
            gemini_response = ask_gemini_text(message, st.session_state.interaction_id)
        st.session_state.interaction_id = gemini_response["interaction_id"]
        st.write(gemini_response["text"])

        if "audio" in gemini_response:
            st.audio(gemini_response["audio"], format="audio/wav")


    st.session_state.messages.append(
        {
            "role": "assistant",
            "text": gemini_response["text"],
            "audio": gemini_response.get("audio")
        }
    )
    # st.rerun()


#streamlit run ai_atm_app.py

#after stop recording, chat_input is slowly vanishing and getting back. Even after sent a message.
#record button vanished after gemini repied.