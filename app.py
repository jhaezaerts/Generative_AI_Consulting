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
    produce = None

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
        bart1 = st.empty()
        q1 = st.empty()
        line1 = st.empty()
        user1 = st.empty()
        r1 = st.empty()
        line2 = st.empty()
        bart2 = st.empty()
        q2 = st.empty()
        line3 = st.empty()
        user2 = st.empty()
        r2 = st.empty()
        line4 = st.empty()
        bart3 = st.empty()
        q3 = st.empty()
        line5 = st.empty()
        user3 = st.empty()
        r3 = st.empty()
        line6 = st.empty()
        bart4 = st.empty()
        q4 = st.empty()
        line7 = st.empty()
        user4 = st.empty()
        r4 = st.empty()
        line8 = st.empty()
        bart5 = st.empty()
        q5 = st.empty()
        line9 = st.empty()
        user5 = st.empty()
        r5 = st.empty()

        # Response area
        # st.markdown("""___""")
        c1, c2 = st.columns([25, 2])
        # Message display
        with c1:
            message_placeholder = st.empty()
            message_placeholder.text_area(label="Me",
                                           label_visibility="collapsed",
                                           placeholder="Record your response...",
                                           disabled=True,
                                           key=st.session_state.input_message_key)
        # Record button
        with c2:
            audio_placeholder = st.empty()
            with audio_placeholder:
                bytes = audio_recorder(pause_threshold=10.0,
                                       text="",
                                       recording_color="#F63366",
                                       neutral_color="#000000",
                                       icon_name="fa-solid fa-microphone",
                                       icon_size="2xl",
                                       key=st.session_state.input_message_key + '1')
        # Submit button
        submit_placeholder = st.empty()
        # submit = submit_placeholder.button("Submit", type="primary")

        if bytes:
            with open('response.wav', mode='bw') as audio_file:
                audio_file.write(bytes)
            recording = open("response.wav", "rb")
            stt = openai.Audio.transcribe("whisper-1", recording)
            st.session_state.responses[st.session_state.index] = stt["text"]
            message = message_placeholder.text_input(label="Me",
                                                     label_visibility="collapsed",
                                                     value=st.session_state.responses[st.session_state.index],
                                                     key=st.session_state.input_message_key + '0')

        if message:
            if st.session_state.index == 4:
                produce = submit_placeholder.button("Generate advice", type="primary")
            else:
                submit = submit_placeholder.button("Submit", type="primary")

        if submit or produce:
            if stt:
                st.session_state.responses[st.session_state.index] = stt["text"]
            st.session_state.index += 1
            st.session_state.input_message_key = str(random())
            st.experimental_rerun()

        # Question processing
        if st.session_state.index == 0:
            bart1.write("**BART**")
            q1.write(questions[0])
        if st.session_state.index == 1:
            bart1.write("**BART**")
            q1.write(questions[0])
            line1.markdown("""---""")
            user1.write("**" + username + "**")
            r1.write(st.session_state.responses[0])
            line2.markdown("""---""")
            bart2.write("**BART**")
            q2.write(questions[1])
        if st.session_state.index == 2:
            bart1.write("**BART**")
            q1.write(questions[0])
            line1.markdown("""---""")
            user1.write("**" + username + "**")
            r1.write(st.session_state.responses[0])
            line2.markdown("""---""")
            bart2.write("**BART**")
            q2.write(questions[1])
            line3.markdown("""---""")
            user2.write("**" + username + "**")
            r2.write(st.session_state.responses[1])
            line4.markdown("""---""")
            bart3.write("**BART**")
            q3.write(questions[2])
        if st.session_state.index == 3:
            bart1.write("**BART**")
            q1.write(questions[0])
            line1.markdown("""---""")
            user1.write("**" + username + "**")
            r1.write(st.session_state.responses[0])
            line2.markdown("""---""")
            bart2.write("**BART**")
            q2.write(questions[1])
            line3.markdown("""---""")
            user2.write("**" + username + "**")
            r2.write(st.session_state.responses[1])
            line4.markdown("""---""")
            bart3.write("**BART**")
            q3.write(questions[2])
            line5.markdown("""___""")
            user3.write("**" + username + "**")
            r3.write(st.session_state.responses[2])
            line6.markdown("""___""")
            bart4.write("**BART**")
            q4.write(questions[3])
        if st.session_state.index == 4:
            bart1.write("**BART**")
            q1.write(questions[0])
            line1.markdown("""---""")
            user1.write("**" + username + "**")
            r1.write(st.session_state.responses[0])
            line2.markdown("""---""")
            bart2.write("**BART**")
            q2.write(questions[1])
            line3.markdown("""---""")
            user2.write("**" + username + "**")
            r2.write(st.session_state.responses[1])
            line4.markdown("""---""")
            bart3.write("**BART**")
            q3.write(questions[2])
            line5.markdown("""___""")
            user3.write("**" + username + "**")
            r3.write(st.session_state.responses[2])
            line6.markdown("""___""")
            bart4.write("**BART**")
            q4.write(questions[3])
            line7.markdown("""___""")
            user4.write("**" + username + "**")
            r4.write(st.session_state.responses[3])
            line8.markdown("""___""")
            bart5.write("**BART**")
            q5.write(questions[4])
        if st.session_state.index == 5:
            bart1.write("**BART**")
            q1.write(questions[0])
            line1.markdown("""---""")
            user1.write("**" + username + "**")
            r1.write(st.session_state.responses[0])
            line2.markdown("""---""")
            bart2.write("**BART**")
            q2.write(questions[1])
            line3.markdown("""---""")
            user2.write("**" + username + "**")
            r2.write(st.session_state.responses[1])
            line4.markdown("""---""")
            bart3.write("**BART**")
            q3.write(questions[2])
            line5.markdown("""___""")
            user3.write("**" + username + "**")
            r3.write(st.session_state.responses[2])
            line6.markdown("""___""")
            bart4.write("**BART**")
            q4.write(questions[3])
            line7.markdown("""___""")
            user4.write("**" + username + "**")
            r4.write(st.session_state.responses[3])
            line8.markdown("""___""")
            bart5.write("**BART**")
            q5.write(questions[4])
            line9.markdown("""___""")
            user5.write("**" + username + "**")
            r5.write(st.session_state.responses[4])

            message_placeholder.empty()
            audio_placeholder.empty()
            submit_placeholder.empty()
            st.title("BART")
            advice_placeholder = st.empty()
            with st.spinner('Processing your responses...'):
                description = ', '.join(st.session_state.responses)
                advice_placeholder.write(get_advice(description))


if __name__ == "__main__":
    main()

