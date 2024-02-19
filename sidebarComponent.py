import streamlit as st
import RetrievalQAWithLLMApp

data=[
    {
        "_id":"1",
        "chat_title":"Robbery questions",
        "questions":[
            {"_id":"1","question":"What is the punishment for robbery?","answer":"answer"},
            {"_id":"2","question":"What is the punishment for robbery?","answer":"answer"}
        ]
    }
]
def user_history():
    with st.sidebar:
        st.header("Your History")
        for d in data:
                st.write(d["chat_title"])

def add_your_documents(model:RetrievalQAWithLLMApp):
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
               with st.spinner("Processing..."):
                    model.process_pdf_files(pdf_docs)