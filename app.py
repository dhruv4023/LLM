import time
import streamlit as st
from components import *
from sidebarComponent import *
from FAISSRetrivalQA import FAISSRetrivalQA 

# API_ENDPOINT = 'http://127.0.0.1:8000/ask'

st.set_page_config(
    page_title="IPC Q&A App",
    page_icon="📘",
    layout="wide"
) 

def main(model: FAISSRetrivalQA): 
    """
    Main function to run the IPC Q&A App.
    
    Parameters:
        model (RetrievalQAWithLLMApp): The model for question answering.
    """
    header()
    add_your_documents(model)
    # user_history()

    col1, col2=st.columns([2,0.3],gap="small")
    with col1:
        question = st.text_input(
            label="Enter your query👇",
            key="question_input",
            placeholder="Ask a question about Indian Constitution...",
            label_visibility="collapsed",
        )
    btn = None
    with col2:
        btn = st.button("Send")
    if btn:
        with st.spinner("Thinking..."):
            st.session_state.chat_history.append({"q": question})
            start_time = time.time()
            ans = model.ask_question(question)
            end_time = time.time()
            st.session_state.chat_history.append({"a": ans})
            print_history()
            st.markdown("##### Time taken to generate answer: " + str(end_time - start_time) + " seconds")
            

if __name__ == "__main__":
    model = FAISSRetrivalQA()
    with st.spinner("Processing"):
        model.create_chain()
    main(model)
