# Imports
from random import random
from audio_recorder_streamlit import audio_recorder
import openai
import streamlit as st
from streamlit_chat import message as chat

# Page Config
st.set_page_config(page_title="AI Consulting by BART")
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


# API Credentials
openai.organization = st.secrets["OPENAI_ORG"]
openai.api_key = st.secrets["OPENAI_API_KEY"]


def get_advice(description):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Given the information given here: '"
                                        + description
                                        + "'. Express enthusiasm about the business that has been described above... "
                                          "What are typical tasks performed in this business that are potentially "
                                          "at risk of being automated by (generative) AI? List these task by increasing "
                                          "difficulty of automation. Next, recommend AI tools and technologies that could"
                                          "support automation of these tasks. Lastly, for each task, what are useful "
                                          "tricks, tips or pitfalls in terms of automating them."
                                          "If the information given above is unrelated to the description of a business, "
                                          "say that you cannot provide valuable input."}
        ]
    )
    return response['choices'][0]['message']['content']


def main():
    st.title("Empower your business with AI:red[.]")
    st.title("")

    stt = None
    message = None
    submit = None

    if "username" not in st.session_state:
        st.session_state.username = ""
    if "index" not in st.session_state:
        st.session_state.index = 0
    if "responses" not in st.session_state:
        st.session_state.responses = []
    if "session" not in st.session_state:
        st.session_state["session"] = True
        st.session_state.input_message_key = str(random())

    questions = [
        "what line of work are you in?",
        "What are the key operating activities of your business?",
        "Are there any processes that are time-consuming or error-prone?",
        "Are there any areas of your business that you think could benefit from AI?",
        "What kind of AI tools or technologies are you most interested in exploring?"
    ]

    # Ask for a username
    username_header = st.empty()
    username_header.subheader("Enter a username")
    username_input = st.empty()
    username = username_input.text_input(label="username", label_visibility="collapsed")
    start_button = st.empty()
    start_button.button("Get started", type="primary")

    # Initialize Q&A
    if username:
        st.session_state.username = username
        username_header.empty()
        username_input.empty()
        start_button.empty()

        # Question processing
        chat(f"Hello {username}, " + questions[0], avatar_style="bottts", seed="Buster")
        test = st.empty()
        c1, c2 = st.columns([9, 1])
        with c1:
            input = st.text_area(label=f"{username}",
                                 label_visibility="collapsed",
                                 placeholder="record your message...",
                                 disabled=True)
        with c2:
            st.header("")
            audio_bytes = audio_recorder(pause_threshold=10.0,
                                         text="",
                                         recording_color="#F63366",
                                         neutral_color="#000000",
                                         icon_name="fa-solid fa-microphone",
                                         icon_size="2xl",
                                         key=st.session_state.input_message_key + '1')

        if audio_bytes:
            with open('response.wav', mode='bw') as audio_file:
                audio_file.write(audio_bytes)
            recording = open("response.wav", "rb")
            stt = openai.Audio.transcribe("whisper-1", recording)
            st.session_state.responses[st.session_state.index] = stt["text"]
            submit = st.button("Send", type="primary")

        if submit:
            if stt:
                st.session_state.responses[st.session_state.index] = stt["text"]
            st.session_state.index += 1
            st.session_state.input_message_key = str(random())
            st.experimental_rerun()


if __name__ == "__main__":
    main()
