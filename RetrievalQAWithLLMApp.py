import os
import streamlit as st

from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceHubEmbeddings,HuggingFaceInstructEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub


os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["env"]["HUGGINGFACEHUB_API_TOKEN"]

class RetrievalQAWithLLMApp:
    # Class attributes for static variables
    files = ["IPC_186045.pdf"]
    # hfi_embeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small",cache_folder="../Models/")
    hfi_embeddings = HuggingFaceHubEmbeddings(repo_id="sentence-transformers/all-MiniLM-L6-v2")#,huggingfacehub_api_token=st.secrets.env.HUGGINGFACEHUB_API_TOKEN)

    chain = None

    def __init__(self):
        # Initialize instance variables
        self.vectorstore = None
        template = """
            - You're a helpful AI assistant assigned to assist individuals seeking legal advice within the framework of Indian laws and the constitution.
            - Your role is to guide users through legal processes and provide information in a lawful manner.
            - Use the given text to answer the question in atleast 1000 words, give all accurate information.
            - Answer questions step by step, highlighting relevant sections of Indian laws and the constitution, use bulleting to display more pretty and readable answer.
            - Refrain from responding to queries that may not contribute to legal affairs, and provide accurate and relevant information without distortion.
            - deny to give answers if its not available into provided text.
        {context}


        Question: {question}  including section number and all related details.
        Answer:"""

        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        
    @classmethod
    def load_pdf_files(self, files):
        # Assuming the provided 'files' list contains URLs
        pdf_url = files[0]

        # Read PDF content from the URL
        pdf_loader = PyPDFLoader(pdf_url)
        pages = pdf_loader.load_and_split()

        # If there are more files in the list, process them
        for i in range(1, len(files)):
            pdf_url = files[i]
            pdf_loader = PyPDFLoader(pdf_url)
            pages += pdf_loader.load_and_split()

        return pages
    
    def create_chain(self):
        if RetrievalQAWithLLMApp.chain is None:
            pages = self.load_pdf_files(RetrievalQAWithLLMApp.files)

            vectorstore = FAISS.from_documents(pages, embedding=RetrievalQAWithLLMApp.hfi_embeddings)

            RetrievalQAWithLLMApp.chain = RetrievalQA.from_chain_type(
                llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.8, "max_length":4096,"max_new_tokens":4096}),
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),    
                # return_source_documents=True,
                chain_type_kwargs={"prompt": self.prompt}, #"verbose": True},
            )
            print("chain created ------------------------------------")

    def ask_question(self, question: str):
        # Ensure the chain is created
        # Use the chain to ask the question
        try:
            response = RetrievalQAWithLLMApp.chain({"query":question, "early_stopping":True,"min_length":2000,"max_tokens":5000})
            return response["result"]
        except Exception as e:
            return "Retry to ask question!, An error message: "+ str(e)
        