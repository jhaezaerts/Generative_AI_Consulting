# Imports
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
        q2 = False

        st.text_area(label="BART",
                     value="What line of work are you in?")
        textbox_placeholder_1 = st.empty()
        textbox_placeholder_2 = st.empty()
        textbox_placeholder_3 = st.empty()
        textbox_placeholder_4 = st.empty()
        textbox_placeholder_5 = st.empty()

        message = st.text_input(label="Me",
                                    placeholder="Send a message...",
                                    key="text_input")

        c1, c2, c3 = st.columns([4, 2, 20])
        with c1:
            submit = st.button("Submit", type="primary")
        with c2:
            test = audio_recorder(
                pause_threshold=10.0,
                text="",
                recording_color="#F63366",
                neutral_color="#000000",
                icon_name="fa-solid fa-microphone",
                icon_size="2xl")

        if submit and message:
            textbox_placeholder_1.text_area(label="Me", value=message)
            q2 = True

        if q2:
            textbox_placeholder_2.text_area(label="BART", value="What are the key operating activities of your business?")


if __name__ == "__main__":
    main()
