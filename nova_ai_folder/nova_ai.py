import base64

import time

import streamlit as st

from nova_gemini import ask_gemini


def load_css():
    st.markdown(
        """
        <style>
        .block-container{
            padding-top:1rem;
        }
        .hero-title{
            font-size:55px;
            font-weight:bold;
        }
        .feature-card{
            border:1px solid #dddddd;
            border-radius:16px;
            padding:10px 16px;
            margin-bottom:12px;
            cursor:pointer;
        }
        .feature-card h3{
            margin-bottom:6px;
            font-size: 22px;
        }
        .feature-card p{
            margin:0
             font-size:15px;
             color:#666666;
        }
        .stbutton > button{
            border-radius:12px, 
            height:45px;
            text-align:left;
        }
        .typing{
            display:flex;
            gap:6px;
            align-items:center;
        }
        .typing span{
            width:10px;
            height:10px;
            border-radius:50%;
            background:#888;
            animation:bounce 1.4s infinite ease-in-out;
        }
        .typing span:nth-child(1){
            animation-delay:0s;
        }

        .typing span:nth-child(2){
            animation-delay:0.2s;
        }

        .typing span:nth-child(3){
            animation-delay:0.4s;
        }
        @keyframes bounce{
            0%, 80%, 100%{
                transform: translateY(0);
            }

            40%{
                transform: translateY(-8px);
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(
    page_title="Nova AI",
    page_icon="🤖",
    layout="wide"
)

load_css()

def show_navbar():
    left, right = st.columns(2)
    with left:
        st.write("## 🤖 Nova AI")
    with right:
        st.write("⚙️   🌙   👤")

def show_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding:10px 0 18px 0;">
                <div style="font-size:42px;">🤖</div>
                <div style="
                    font-size:28px;
                    font-weight:700;
                    margin-top:6px;
                ">
                    Nova AI
                </div>
                <div style="
                    color:#808080;
                    font-size:14px;
                    margin-top:4px;
                ">
                    Your Intelligent Assistant
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.mode = "home"
            st.rerun()
        uploaded_file = st.file_uploader("📁 Upload File", type=["png", "jpg", "jpeg", "pdf"])

        st.markdown("---")

        st.markdown("#### 💬 Recent Chats")

        st.button("💭 Learn Python", use_container_width=True)
        st.button("💭 Resume Builder", use_container_width=True)
        st.button("💭 Streamlit Project", use_container_width=True)
        st.button("💭 Analyze CSV", use_container_width=True)

        st.divider()
        st.markdown("#### ⚙️ Settings")
        st.button("🌙 Theme", use_container_width=True)
        st.button("ℹ️ About Nova", use_container_width=True)

        return uploaded_file

def show_screen(selected_file):

    if st.session_state.mode == "home":
        show_homescreen()

    elif st.session_state.mode == "pdf":
        show_pdf()

    elif st.session_state.mode == "code":
        show_code()

    elif st.session_state.mode == "resume":
        show_resume()

    elif st.session_state.mode == "data":
        show_data()

    else:
        show_chat(selected_file)

def show_page_header(title, subtitle):
    if st.button("<- Home"):
        st.session_state.mode = "home"
        st.rerun()
    st.title(title)
    st.caption(subtitle)
    st.divider()

def show_pdf():
    show_page_header("📄 PDF Assistant", "Summarize and chat with your PDF")
    st.file_uploader("Upload a PDF", type=["pdf"], key="pdf_page_upload")
    st.button("📑Summarise", use_container_width=True)

def show_resume():
    show_page_header("Resume Maker", "Prepares resume instantly")

def show_code():
    show_page_header("💻 Explain Code", "Understand, debug and improve your code.")

def show_data():
    show_page_header("📊 Analyze Data", "Analyze CSV files and generate insights.")


def process_user_message(message):

    if message:

        st.session_state.mode = "chat"

        st.session_state.messages.append(
            {
                "role": "user",
                "text": message,
            }
        )

        st.rerun()


def show_chat(selected_file):
    for i, msg in enumerate(st.session_state.messages):

        with st.chat_message(msg["role"]):
            st.write(msg["text"])

        if (
            i == len(st.session_state.messages) - 1
            and msg["role"] == "user"
        ):

            with st.chat_message("assistant"):

                typing = st.empty()

                typing.markdown(
                    """
                    <div class="typing">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                base64_data = None
                mime_type = None

                if selected_file:
                    mime_type = selected_file.type
                    file_bytes = selected_file.read()
                    base64_data = base64.b64encode(file_bytes).decode("utf-8")

                gemini_response = ask_gemini(
                    msg["text"],
                    base64_data,
                    mime_type,
                )

                typing.empty()

                response = st.empty()

                for j in range(len(gemini_response)):
                    response.markdown(gemini_response[: j + 1])
                    time.sleep(0.02)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "text": gemini_response,
                }
            )

            st.rerun()

def show_homescreen():
    st.markdown(
        """
        <div style="text-align:center; padding-top:10px; margin-bottom: 25px">
            <h1 class="hero-title">Hello 👋</h1>
            <h3> Your Intelligent AI Assistant </h3>
            <p>Ask questions, analyze documents,
        write code, summarize PDFs and much more.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Summarize PDF\n\nQuickly summarize PDF documents", use_container_width=True):
            st.session_state.mode = "pdf"
            st.rerun()

        if st.button("💻 Explain Code\n\nUnderstand, debug and improve your code.", use_container_width=True):
            st.session_state.mode = "code"
            st.rerun()
    with col2:
        if st.button("Resume Maker\n\nPrepares resume instantly", use_container_width=True):
            st.session_state.mode = "resume"
            st.rerun()
        if st.button("📊 Analyze Data\n\nAnalyze CSV files and generate insights.", use_container_width=True):
            st.session_state.mode = "data"
            st.rerun()




if "messages" not in st.session_state:
        st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "home"

show_navbar()

selected_file = show_sidebar()

message = st.chat_input("Enter your prompt")

process_user_message(message)

show_screen(selected_file)
