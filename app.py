# Imports
from random import random
from audio_recorder_streamlit import audio_recorder
import openai
import streamlit as st
import streamlit.components.v1 as components

# Page Config
st.set_page_config(page_title="AI Consulting App")
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
    st.title("Empower your business with AI.")
    st.title("")

    stt = None
    message = None
    submit = None

    if "username" not in st.session_state:
        st.session_state.username = ""
    if "index" not in st.session_state:
        st.session_state.index = 0
    if "responses" not in st.session_state:
        st.session_state.responses = [None] * 5
    if "session" not in st.session_state:
        st.session_state["session"] = True
        st.session_state.input_message_key = str(random())

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

        questions = [
            f"Hello {username}, what line of work are you in?",
            "What are the key operating activities of your business?",
            "Are there any processes that are time-consuming or error-prone?",
            "Are there any areas of your business that you think could benefit from AI?",
            "What kind of AI tools or technologies are you most interested in exploring?"
        ]

        # Set containers for Q&A
        q1_col1, q1_col2 = st.columns([1, 11])
        with q1_col1:
            bart1 = st.empty()
        with q1_col2:
            q1 = st.empty()
        r1_col1, r1_col2 = st.columns([11, 2])
        with r1_col1:
            message1 = st.empty()
        with r1_col2:
            whitespace1 = st.empty()
            audio1 = st.empty()
        submit1 = st.empty()
        q2_col1, q2_col2 = st.columns([1, 11])
        with q2_col1:
            bart2 = st.empty()
        with q2_col2:
            q2 = st.empty()
        r2_col1, r2_col2 = st.columns([11, 2])
        with r2_col1:
            message2 = st.empty()
        with r2_col2:
            whitespace2 = st.empty()
            audio2 = st.empty()
        submit2 = st.empty()
        q3_col1, q3_col2 = st.columns([1, 11])
        with q3_col1:
            bart3 = st.empty()
        with q3_col2:
            q3 = st.empty()
        r3_col1, r3_col2 = st.columns([11, 2])
        with r3_col1:
            message3 = st.empty()
        with r3_col2:
            whitespace3 = st.empty()
            audio3 = st.empty()
        submit3 = st.empty()
        q4_col1, q4_col2 = st.columns([1, 11])
        with q4_col1:
            bart4 = st.empty()
        with q4_col2:
            q4 = st.empty()
        r4_col1, r4_col2 = st.columns([11, 2])
        with r4_col1:
            message4 = st.empty()
        with r4_col2:
            whitespace4 = st.empty()
            audio4 = st.empty()
        submit4 = st.empty()
        q5_col1, q5_col2 = st.columns([1, 11])
        with q5_col1:
            bart5 = st.empty()
        with q5_col2:
            q5 = st.empty()
        r5_col1, r5_col2 = st.columns([11, 2])
        with r5_col1:
            message5 = st.empty()
        with r5_col2:
            whitespace5 = st.empty()
            audio5 = st.empty()
        submit5 = st.empty()

        # Write down questions
        bart1.write("**BART**")
        q1.write(questions[0])
        bart2.write("**BART**")
        q2.write(questions[1])
        bart3.write("**BART**")
        q3.write(questions[2])
        bart4.write("**BART**")
        q4.write(questions[3])
        bart5.write("**BART**")
        q5.write(questions[4])

        if st.session_state.index == 0:
            message1.text_area(label=f"{username}",
                                          label_visibility="collapsed",
                                          placeholder="Record your response...",
                                          disabled=True,
                                          height=25,
                                          key=st.session_state.input_message_key)
            # Record button
            whitespace1.header("")
            with audio1:
                bytes = audio_recorder(pause_threshold=10.0,
                                       text="",
                                       recording_color="#F63366",
                                       neutral_color="#000000",
                                       icon_name="fa-solid fa-microphone",
                                       icon_size="2xl",
                                       key=st.session_state.input_message_key + '1')

            if bytes:
                with open('response.wav', mode='bw') as audio_file:
                    audio_file.write(bytes)
                recording = open("response.wav", "rb")
                stt = openai.Audio.transcribe("whisper-1", recording)
                st.session_state.responses[st.session_state.index] = stt["text"]
                message = message1.text_area(label="Me",
                                             label_visibility="collapsed",
                                             value=st.session_state.responses[st.session_state.index],
                                             key=st.session_state.input_message_key + '0')

            if message:
                submit = submit1.button("Send", type="primary")

            if submit:
                if stt:
                    st.session_state.responses[st.session_state.index] = stt["text"]
                st.session_state.index += 1
                st.session_state.input_message_key = str(random())
                message1.write(st.session_state.responses[0])
                whitespace1.empty()
                audio1.empty()
                st.experimental_rerun()

        #if st.session_state.index == 5:
         #   message_placeholder.empty()
         #   audio_placeholder.empty()
         #   submit_placeholder.empty()
         #   st.title("BART")
         #   advice_placeholder = st.empty()
         #   with st.spinner('Processing your responses...'):
         #       description = ', '.join(st.session_state.responses)
         #       advice_placeholder.write(get_advice(description))


if __name__ == "__main__":
    main()

