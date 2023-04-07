# Imports
import time
from random import random

from audio_recorder_streamlit import audio_recorder
import openai
import streamlit as st
import streamlit.components.v1


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

    st.subheader("How would you like to interact?")
    interaction = st.radio("", ("Text", "Speech", "Test"), label_visibility="collapsed")
    st.title("")

    if interaction == "Text":
        st.subheader("Provide a clear description of your business.")
        st.write('*line of work, key activities, time-consuming, repetitive or error-prone processes, etc.*')
        description = st.text_area(label="description",
                                   placeholder="I am a car salesperson. Our company targets the luxurious market segment. We sell premier, high-quality cars in our physical stores, as well as online via our website. We mostly...",
                                   label_visibility="collapsed",
                                   height=300)
        if st.button("Generate", type="primary"):
            if description:
                with st.spinner('Processing your response...'):
                    st.markdown("""---""")
                    st.write(get_advice(description))
            else:
                st.markdown("""---""")
                st.write("I need a description before I can generate advice.")

    if interaction == "Speech":
        stt = None

        # initialize questions
        questions = [
            "What line of work are you in?",
            "What are the key operating activities of your business?",
            "Are there any processes that are time-consuming or error-prone?",
            "Are there any areas of your business that you think could benefit from AI?",
            "What kind of AI tools or technologies are you most interested in exploring?"
        ]

        # initialize session states
        if "idx" not in st.session_state:
            st.session_state.idx = 0
        if "responses" not in st.session_state:
            st.session_state.responses = [None] * 5

        question_placeholder = st.empty()
        question_placeholder.subheader(questions[st.session_state.idx])
        st.title("")
        c1, c2, c3 = st.columns([1, 7, 2])
        with c1:
            audio_bytes = audio_recorder(
                            pause_threshold=10.0,
                            text="",
                            recording_color="#F63366",
                            neutral_color="#000000",
                            icon_name="fa-solid fa-microphone",
                            icon_size="3x")

        with c2:
            transcript_placeholder = st.empty()
            if audio_bytes:
                with open('response.wav', mode='bw') as audio_file:
                    audio_file.write(audio_bytes)
                response = open("response.wav", "rb")
                stt = openai.Audio.transcribe("whisper-1", response)
                st.session_state.responses[st.session_state.idx] = stt["text"]
                transcript_placeholder.write(stt["text"])

        with c3:
            button_placeholder = st.empty()
            if stt:
                clicked = button_placeholder.button("Submit", type="primary")
                if clicked:
                    if st.session_state.idx < len(questions)-1:
                        st.session_state.idx += 1
                    else:
                        st.session_state.idx = 0
                    transcript_placeholder.empty()
                    button_placeholder.empty()
                    question_placeholder.subheader(questions[st.session_state.idx])

        st.markdown("""---""")

        advice_placeholder = st.empty()
        if None not in st.session_state.responses and clicked:
            with st.spinner('Processing your responses...'):
                description = ', '.join(st.session_state.responses)
                advice_placeholder.write(get_advice(description))
                st.session_state.responses = [None] * 5
                question_placeholder.subheader(questions[st.session_state.idx])
        else:
            advice_placeholder.empty()

    if interaction == "Test":
        
        # Ask for a username
        if "username" not in st.session_state:
            st.session_state.username = ""
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
                "What line of work are you in?",
                "What are the key operating activities of your business?",
                "Are there any processes that are time-consuming or error-prone?",
                "Are there any areas of your business that you think could benefit from AI?",
                "What kind of AI tools or technologies are you most interested in exploring?"
            ]

            if "responses" not in st.session_state:
                st.session_state.responses = [None] * 5

            q1 = st.empty()
            r1 = st.empty()
            q2 = st.empty()
            r2 = st.empty()
            q3 = st.empty()
            r3 = st.empty()
            q4 = st.empty()
            r4 = st.empty()
            q5 = st.empty()
            r5 = st.empty()

            # Response area
            st.markdown("""___""")
            if "session" not in st.session_state:
                st.session_state["session"] = True
                st.session_state.input_message_key = str(random())
            c1, c2 = st.columns([25, 2])
            with c1:
                message_placeholder = st.empty()
                message = message_placeholder.text_input(label="Me",
                                        label_visibility="collapsed",
                                        placeholder="Send a message...",
                                        key=st.session_state.input_message_key)
            with c2:
                audio_container = st.container()
                with audio_container:
                    bytes = audio_recorder(
                        pause_threshold=10.0,
                        text="",
                        recording_color="#F63366",
                        neutral_color="#000000",
                        icon_name="fa-solid fa-microphone",
                        icon_size="2xl")
            submit_placeholder = st.empty()
            submit = submit_placeholder.button("Submit", type="primary")

            # Question processing
            if "index" not in st.session_state:
                st.session_state.index = 0

            if st.session_state.index == 0:
                q1.text_area(label="BART", value=questions[0], key='q1.0')
            if st.session_state.index == 1:
                q1.text_area(label="BART", value=questions[0], key='q1.1')
                r1.text_area(label=username, value=st.session_state.responses[0], key='r1.1')
                q2.text_area(label="BART", value=questions[1], key='q2.1')
            if st.session_state.index == 2:
                q1.text_area(label="BART", value=questions[0], key='q1.2')
                r1.text_area(label=username, value=st.session_state.responses[0], key='r1.2')
                q2.text_area(label="BART", value=questions[1], key='q2.2')
                r2.text_area(label=username, value=st.session_state.responses[1], key='r2.2')
                q3.text_area(label="BART", value=questions[2], key='q3.2')
            if st.session_state.index == 3:
                q1.text_area(label="BART", value=questions[0], key='q1.3')
                r1.text_area(label=username, value=st.session_state.responses[0], key='r1.3')
                q2.text_area(label="BART", value=questions[1], key='q2.3')
                r2.text_area(label=username, value=st.session_state.responses[1], key='r2.3')
                q3.text_area(label="BART", value=questions[2], key='q3.3')
                r3.text_area(label=username, value=st.session_state.responses[2], key='r3.3')
                q4.text_area(label="BART", value=questions[3], key='q4.3')
            if st.session_state.index == 4:
                q1.text_area(label="BART", value=questions[0], key='q1.4')
                r1.text_area(label=username, value=st.session_state.responses[0], key='r1.4')
                q2.text_area(label="BART", value=questions[1], key='q2.4')
                r2.text_area(label=username, value=st.session_state.responses[1], key='r2.4')
                q3.text_area(label="BART", value=questions[2], key='q3.4')
                r3.text_area(label=username, value=st.session_state.responses[2], key='r3.4')
                q4.text_area(label="BART", value=questions[3], key='q4.4')
                r4.text_area(label=username, value=st.session_state.responses[3], key='r4.4')
                q5.text_area(label="BART", value=questions[4], key='q5.4')
            if st.session_state.index == 5:
                q1.text_area(label="BART", value=questions[0], key='q1.5')
                r1.text_area(label=username, value=st.session_state.responses[0], key='r1.5')
                q2.text_area(label="BART", value=questions[1], key='q2.5')
                r2.text_area(label=username, value=st.session_state.responses[1], key='r2.5')
                q3.text_area(label="BART", value=questions[2], key='q3.5')
                r3.text_area(label=username, value=st.session_state.responses[2], key='r3.5')
                q4.text_area(label="BART", value=questions[3], key='q4.5')
                r4.text_area(label=username, value=st.session_state.responses[3], key='r4.5')
                q5.text_area(label="BART", value=questions[4], key='q5.5')
                r5.text_area(label=username, value=st.session_state.responses[4], key='r5.5')
                message_placeholder.empty()
                button_placeholder.empty()
                audio_container.empty()

            if submit:
                st.write(st.session_state.index)
                st.session_state.responses[st.session_state.index] = message
                st.session_state.index += 1
                st.session_state.input_message_key = str(random())
                st.experimental_rerun()












        # if "q1" not in st.session_state:
        #     st.session_state.q1 = False
        # if "q2" not in st.session_state:
        #     st.session_state.q2 = False
        #
        # st.text_area(label="BART",
        #              value="What line of work are you in?")
        # textbox_placeholder_1 = st.empty()
        # textbox_placeholder_2 = st.empty()
        # textbox_placeholder_3 = st.empty()
        # textbox_placeholder_4 = st.empty()
        # textbox_placeholder_5 = st.empty()
        #
        # if "variables_setup" not in st.session_state:
        #     st.session_state["variables_setup"] = True
        #     st.session_state.input_message_key = str(random())
        # st.markdown("""___""")
        #
        # c1, c2 = st.columns([25, 2])
        # with c1:
        #     message = st.text_input(label="Me",
        #                             label_visibility="collapsed",
        #                             placeholder="Send a message...",
        #                             key=st.session_state.input_message_key)
        # with c2:
        #     test = audio_recorder(
        #         pause_threshold=10.0,
        #         text="",
        #         recording_color="#F63366",
        #         neutral_color="#000000",
        #         icon_name="fa-solid fa-microphone",
        #         icon_size="2xl")
        #
        # submit = st.button("Submit", type="primary")
        #
        # if submit:
        #     st.session_state.q1 = True
        #     st.session_state.q2 = True
        #     if "r1" not in st.session_state:
        #         st.session_state.r1 = message
        #     st.session_state.input_message_key = str(random())
        #     st.experimental_rerun()
        #
        # if st.session_state.q1:
        #     textbox_placeholder_1.text_area(label="Me", value=st.session_state.r1, key="response1")
        #
        # if st.session_state.q2:
        #     time.sleep(1)
        #     textbox_placeholder_2.text_area(label="BART", value="What are the key operating activities of your business?")


if __name__ == "__main__":
    main()
