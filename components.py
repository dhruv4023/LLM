import streamlit as st
def print_history():
    # Scrollable box for chat history
    st.markdown(
        """
        <style>
        .scrollable-container {
            overflow-y: auto;
            max-height: 50vh;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="scrollable-container">
        """,
        unsafe_allow_html=True
    )


    for message in st.session_state.chat_history:
        if "q" in message:
            print_chat(message["q"], is_user=True)
        elif "a" in message:
            print_chat(message["a"], is_user=False)

    # Close the scrollable container div
    st.markdown("</div>", unsafe_allow_html=True)

def print_chat(message, is_user=True):
    if is_user:
        # User's question
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                margin-bottom: 8px;
            ">
                <div style="
                    background-color: #354747;
                    color: white;
                    padding: 8px;
                    border-radius: 8px;
                    max-width: 70%;
                    text-align: right;
                ">
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Bot's answer
        st.markdown(
            f"""
            <div style="
                display: flex;
                margin-bottom: 8px;
            ">
                <div style="
                    background-color: #454443;
                    padding: 8px;
                    border-radius: 8px;
                    max-width: 70%;
                    text-align: left;
                ">
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# List of questions
questions = [
    "What is the punishment for robbery?",
    "One person has committed defamation, what should be the punishment for it?",
    "Rioting has happened in the neighboring society. Who will be responsible and what is the punishment for it?",
    "What is punishment for robbery and also murder?",
    "A person is selling adulterated drugs which is harmful to the health of people. The person has also sold drug to the children below the age of 15. What will be punishment for it?",
    "Explain all laws related to marriage"
]

# Display questions using st.markdown
def header():
    st.title("Chatbot for Question Answering on Legal Documents 👩‍⚖️")
    st.markdown("Greetings! 🌐 I'm your Indian Constitution Chat Bot, ready to navigate through legal intricacies. Explore acts like the Companies Act 2013 or Code of Civil Procedure 1908. Ask away! 📚⚖️")
    st.markdown("##### Here are some sample Questions\n" + "\n".join([f"- \"{question}\"" for question in questions]))
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []