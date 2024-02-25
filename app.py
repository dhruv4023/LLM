import time
import streamlit as st
from components import *
from MongoDBRetrivalQA import Main 
# API_ENDPOINT = 'http://127.0.0.1:8000/ask'

st.set_page_config(
    page_title="IPC Q&A App",
    page_icon="📘",
    layout="wide"
) 

model = Main()

def main(): 
    header()
    # Input box inside the sticky container
    question = st.text_input(
        label="Enter your query👇",
        key="question_input",
        placeholder="Ask a question about Indian Constitution...",
        label_visibility="collapsed"
    )
    if question:
        with st.spinner("Thinking..."):
            st.session_state.chat_history.append({"q": question})
            start_time = time.time()
            ans = model.ask_question(question)
            end_time = time.time()
            # ans="hello"
            st.session_state.chat_history.append({"a": ans})
            print_history()
            st.markdown("##### Time taken to generate answer: "+str(end_time-start_time)+" seconds)")
        
if __name__ == "__main__":
    main()