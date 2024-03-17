# https://www.youtube.com/watch?v=dXxQ0LR-3Hg
import streamlit as st
from dotenv import load_dotenv
from HTMLfiles.htmlTemplates import css, bot_template, user_template
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS

# # Open AI ------------- start
# from langchain.chat_models import ChatOpenAI
# from langchain.embeddings import OpenAIEmbeddings
# # Open AI ------------- end

# Hugging Face ---------- start
from langchain.embeddings import  HuggingFaceInstructEmbeddings
from langchain.llms import HuggingFaceHub
# HuggingFace ------------- end

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    print("---------------------------------------------------------------------------------------------------------")
    print("Total size: ",len(text)," Bytes")
    print("---------------------------------------------------------------------------------------------------------")
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    # embeddings = ChatOpenAI()
    # HFIembeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small",cache_folder="./Models/")
    embeddings = HuggingFaceInstructEmbeddings(model_name="WhereIsAI/UAE-Large-V1")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            
def process_pdf_files(pdf_docs):
    with st.spinner("Processing"):
        # get pdf text
        raw_text = get_pdf_text(pdf_docs)
        print("from ",pdf_docs," text extracted...............................................................")
        
        # get the text chunks
        text_chunks = get_text_chunks(raw_text)
        # st.write(text_chunks)
        print("chunk created..................................................................................")

        # create vector store
        vectorstore = get_vectorstore(text_chunks)
        print("vector store created...........................................................................")

        # create conversation chain
        st.session_state.conversation = get_conversation_chain(vectorstore)

def main(pdf_docs):
    load_dotenv()
    # # default pdf 
    st.set_page_config(page_title="CHAT",page_icon=":books")
    if st.button("Load LAW PDF"):
        process_pdf_files(pdf_docs=pdf_docs)
    st.header("Chat With PDFs")
    user_question=st.text_input("Enter Your query")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    if user_question:
        handle_userinput(user_question)
    

if __name__ =="__main__":
    pdf_docs = ["parts.pdf"]  
    main(pdf_docs=pdf_docs)