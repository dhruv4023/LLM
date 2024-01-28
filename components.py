import streamlit as st
def print_history():
    # Scrollable box for chat history
    st.markdown(
        """
        <style>
        .scrollable-container {
            overflow-y: auto;
            max-height: 300px;  /* Adjust the max-height as needed */
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

def header():
    st.title("Chat LLB 👩‍⚖️")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            # {"q": "Initial question"},
            # {"a": "Initial answer"},
            # {"q": "Initial question"},
            # {"a": "Initial answer"},
            # {"q": "Initial question"},
            # {"a": "Initial answer"},
            # {"q": "Initial question"},
            # {"a": "Initial answer"},
            # {"q": "Initial question"},
            # {"a": "Initial answer"},
        ]