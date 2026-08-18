import streamlit as st
import time

from ai_atm_folder.utils import stt

st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display conversation
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["type"] == "text":
            st.markdown(message["content"])

        elif message["type"] == "audio":
            st.audio(message["audio"], format="audio/wav")


# Text input
if prompt := st.chat_input("Type your message..."):

    # User turn
    st.session_state.messages.append({
        "role": "user",
        "type": "text",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Model turn
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            time.sleep(1)

            response = f"I received your message: **{prompt}**"

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "type": "text",
        "content": response
    })


# Audio input
st.divider()

st.markdown("### 🎙️ Voice Input")

audio = st.audio_input("Record your message")

if audio is not None:

    # User audio turn
    st.session_state.messages.append({
        "role": "user",
        "type": "audio",
        "audio": audio.getvalue()
    })

    with st.chat_message("user"):
        st.audio(audio, format="audio/wav")

    # Here you can send audio to your STT / AI model
    with st.chat_message("assistant"):

        with st.spinner("Processing audio..."):
            time.sleep(1)

        response = stt(audio)

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "type": "text",
        "content": response
    })