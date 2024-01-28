import streamlit as st
from components import *
from RetrievalQAWithLLMApp import RetrievalQAWithLLMApp 
# API_ENDPOINT = 'http://127.0.0.1:8000/ask'

RetrievalQAWithLLMApp.files=["D:/Files/LLM/Project/DataSourceFiles/IPC_186045.pdf","D:\Files\LLM\Src_docs\special_marriage_act.pdf","D:\Files\LLM\Src_docs\THE_CODE_OF_CIVIL_PROCEDURE_1908.pdf","D:\Files\LLM\Src_docs\THE_LAND_ACQUISITION_ACT.pdf"]

model = RetrievalQAWithLLMApp()
if model.chain is None:
    with st.spinner("Processing"):
        model.create_chain()

def main():
    header()

    # Container for sticky title and input box
    input_container = st.container()

    # Set a class for the sticky container
    input_container.markdown(
        f"""
        <div style="
            position: sticky;
            top: 0;
            background-color: #f4f4f4;  /* Adjust the background color as needed */
            z-index: 100;
        ">
        """,
        unsafe_allow_html=True
    )

    # Input box inside the sticky container
    question = input_container.text_input(
        label="Enter your query👇",
        key="question_input",
        placeholder="Ask a question about Indian Penal Code",
        label_visibility="collapsed"
    )

    if question:
        with st.spinner("Thinking..."):
            st.session_state.chat_history.append({"q": question})
            ans = model.ask_question(question)
            st.session_state.chat_history.append({"a": ans})
            print_history()

    # Close the sticky container div
    input_container.markdown("</div>", unsafe_allow_html=True)
    
if __name__ == "__main__":
    # st.set_page_config(
    #     page_title="IPC Q&A App",
    #     page_icon="📘",
    #     layout="centered"
    # ) 
    main()

