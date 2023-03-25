# Imports
from audio_recorder_streamlit import audio_recorder
import openai
import streamlit as st


# API Credentials
openai.organization = st.secrets["OPENAI_ORG"]
openai.api_key = st.secrets["OPENAI_API_KEY"]


def get_advice(description):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What are 5 key opportunities for AI that can be leveraged based on the "
                                        "following information: "
                                        + description
                                        + ". Express enthusiasm about the description before listing the opportunities"},
        ]
    )
    return st.write(response['choices'][0]['message']['content'])


def record(key):
    return audio_recorder(
                pause_threshold=10.0,
                text="",
                recording_color="#cd0000",
                neutral_color="#000000",
                icon_name="fa-solid fa-microphone",
                icon_size="3x",
                key=key)


def whisper(bytes, responses, idx):
    if bytes:
        with open('response.wav', mode='bw') as audio_file:
            audio_file.write(bytes)
        response = open("response.wav", "rb")
        stt = openai.Audio.transcribe("whisper-1", response)
        responses[idx] = stt["text"]
    return responses


# Main page
st.title("Uncovering AI in your business.")
st.title("")

st.write("**Hello there, my name is Bart (Business AI Readiness Tool). How would you like to interact with me?**")
interaction = st.radio("", ("Text", "Speech"), label_visibility="collapsed")
st.title("")


if interaction == "Text":
    st.subheader("Provide a clear description of your business.")
    st.write('*line of work, key activities, desirable activities, time-consuming or error-prone processes, etc.*')
    description = st.text_area(label="", label_visibility="collapsed", height=300)
    if st.button("Generate advice"):
        if description:
            with st.spinner('Processing your response...'):
                st.title("")
                get_advice(description)
            st.title("")
            st.success('You can always edit your text if you want to provide additional information.  \n  '
                       'Good luck with your AI endeavours!')
        else:
            st.title("")
            st.write("I need a description before I can generate advice.")

if interaction == "Speech":
    responses = [None] * 5

    # Question 1
    c1, c2 = st.columns([1, 7])
    with c1:
        audio_bytes = record("q1")
    with c2:
        st.subheader("What line of work are you in?")
        responses = whisper(audio_bytes, responses, 0)
        if responses[0]:
            st.write("*Response submitted :white_check_mark:*")

    # Question 2
    st.title("")
    c1, c2 = st.columns([1, 7])
    with c1:
        audio_bytes = record("q2")
    with c2:
        st.subheader("What are the key operating activities of your business?")
        responses = whisper(audio_bytes, responses, 1)
        if responses[1]:
            st.write("*Response submitted :white_check_mark:*")

    # Question 3
    st.title("")
    c1, c2 = st.columns([1, 7])
    with c1:
        audio_bytes = record("q3")
    with c2:
        st.subheader("Are there any processes that are time-consuming or error-prone?")
        responses = whisper(audio_bytes, responses, 2)
        if responses[2]:
            st.write("*Response submitted :white_check_mark:*")

    # Question 4
    st.title("")
    c1, c2 = st.columns([1, 7])
    with c1:
        audio_bytes = record("q4")
    with c2:
        st.subheader("Are there any areas of your business that you think could benefit from AI?")
        responses = whisper(audio_bytes, responses, 3)
        if responses[3]:
            st.write("*Response submitted :white_check_mark:*")

    # Question 5
    st.title("")
    c1, c2 = st.columns([1, 7])
    with c1:
        audio_bytes = record("q5")
    with c2:
        st.subheader("What kind of AI tools or technologies are you most interested in exploring?")
        responses = whisper(audio_bytes, responses, 4)
        if responses[4]:
            st.write("*Response submitted :white_check_mark:*")

    st.title("")
    if None not in responses:
        with st.spinner('Processing your responses...'):
            description = ', '.join(responses)
            get_advice(description)
        st.title("")
        st.success('You can always resubmit responses if you want to provide additional information.  \n  '
                   'Good luck with your AI endeavours!')

