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
                                        + ". Express enthusiasm about the description before listing the opportunities"}
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
                icon_size="2xl",
                key=key)


def whisper(bytes, responses, idx):
    if bytes:
        with open('response.wav', mode='bw') as audio_file:
            audio_file.write(bytes)
        response = open("response.wav", "rb")
        stt = None
        while stt is None:
            try:
                stt = openai.Audio.transcribe("whisper-1", response)
            except openai.InvalidRequestError:
                pass
        responses[idx] = stt["text"]
    return responses


def set_question(title, key, idx, responses):
    st.title("")
    st.subheader(title)
    st.write("")
    c1, c2, c3 = st.columns([1, 7, 2])
    with c1:
        audio_bytes = record(key)
    with c2:
        responses = whisper(audio_bytes, responses, idx)
        if responses[idx]:
            st.write(responses[idx])
        else:
            st.write("")
    with c3:
        if responses[idx]:
            st.write(":heavy_check_mark:")


def main():
    st.title("Discover what AI can mean for your business.")
    st.title("")

    st.header("How would you like to interact?")
    interaction = st.radio("", ("Text", "Speech"), label_visibility="collapsed")
    st.title("")

    if interaction == "Text":
        st.header("Provide a clear description of your business.")
        st.write('*line of work, key activities, desirable activities, time-consuming, repetitive or error-prone processes, etc.*')
        description = st.text_area(label="",
                                   placeholder="I am a car salesperson. Our company targets the luxurious market segment. We sell premier, high-quality cars in our physical stores, as well as online via our website. We mostly...",
                                   label_visibility="collapsed",
                                   height=300)
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

        set_question("What line of work are you in?", "q1", 0, responses)
        set_question("What are the key operating activities of your business?", "q2", 1, responses)
        set_question("Are there any processes that are time-consuming or error-prone?", "q3", 2, responses)
        set_question("Are there any areas of your business that you think could benefit from AI?", "q4", 3, responses)
        set_question("What kind of AI tools or technologies are you most interested in exploring?", "q5", 4, responses)

        st.title("")
        if None not in responses:
            with st.spinner('Processing your responses...'):
                description = ', '.join(responses)
                get_advice(description)
            st.title("")
            st.success('You can always resubmit responses if you want to provide additional information.  \n  '
                       'Good luck with your AI endeavours!')


if __name__ == "__main__":
    main()
