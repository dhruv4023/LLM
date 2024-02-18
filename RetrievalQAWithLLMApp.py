import os
import torch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceHubEmbeddings,HuggingFaceInstructEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub
from appConfig import *
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

class CreateChunks:
    def get_pdf_text(self,pdf_docs):
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        print("---------------------------------------------------------------------------------------------------------")
        print("Total size: ",len(text)," Bytes")
        print("---------------------------------------------------------------------------------------------------------")
        return text

    def get_text_chunks(self,files):
        text = self.get_pdf_text(files)
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks

    def split_docs(self, pdf_file_path, chunk_size=1000, chunk_overlap=20):
        docs = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap).split_documents(PyPDFLoader(pdf_file_path).load_and_split())
        return docs


class GenerateEmbeddingFromPdfFile:
    HFIembeddings=None
    def __init__(self) -> None:
        self.chunkObj= CreateChunks()
        DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
        if self.HFIembeddings is None:
            self.HFIembeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small", cache_folder="./Models/", model_kwargs={"device": DEVICE})
            
    def process_uploaded_file_and_make_temp_vectors(self,files,current_vector_store:FAISS):
        for file in files:
            texts = self.chunkObj.get_text_chunks(files)
            current_vector_store.merge_from(FAISS.from_texts(texts, embedding = self.HFIembeddings))
            print("Vectors merged of:", file)
        return current_vector_store
    
    def create_vectores_and_store_locally(self, vector_store_folder_name:str, folder_path:str):
        current_vector_files = set(file_name.split(".")[0] for file_name in os.listdir(vector_store_folder_name) if file_name.endswith(".faiss"))
        for file in [f for f in os.listdir(folder_path) if f.endswith(".pdf")]: 
            file_name = os.path.splitext(file)[0]
            if file_name not in current_vector_files:
                docs = self.chunkObj.split_docs(os.path.join(folder_path, file))
                FAISS.from_documents(docs, embedding=self.HFIembeddings).save_local(vector_store_folder_name, file_name)
                print("Vector file created for:", file)
            else:
                print("Vector file already exists for:", file)
    
    def load_vectore_stores(self,folder_path:str,current_vector_store:FAISS=None):
        flag = current_vector_store is not None
        for index in [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if file_name.endswith(".faiss")]: 
            if flag:
                current_vector_store.merge_from(FAISS.load_local("FAISS_db",self.HFIembeddings,os.path.basename(index).split(".")[0]))
            else:
                flag = True
                current_vector_store = FAISS.load_local("FAISS_db",self.HFIembeddings,os.path.basename(index).split(".")[0])
        return current_vector_store
                
    
                
   
class RetrievalQAWithLLMApp:
    # Class attributes for static variables
    files = ["IPC_186045.pdf"]
    # hfi_embeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small",cache_folder="../Models/")
    # hfi_embeddings = HuggingFaceHubEmbeddings(repo_id="sentence-transformers/all-MiniLM-L6-v2")#,huggingfacehub_api_token=st.secrets.env.HUGGINGFACEHUB_API_TOKEN)

    chain = None
    vectorstore = None

    def __init__(self):
        self.embedObj = GenerateEmbeddingFromPdfFile()
        # Initialize instance variables
        template = """
        You'r helpful AI assisant given the task to help people seeking advise.
        You have to help person by answering their question using provided documents only.
        Answer in step by step in points by highlighting major information.
        Refuse to answer if it is not provided in the provided documents also donot concoat anything.
        deny to answer the question if it is not provided in the text.
        {context}


        Question: {question}  including section number and all related details.
        Answer:"""

        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])
  
    def create_vectore_and_store(self,folder_path:str):
        self.embedObj.create_vectores_and_store_locally("FAISS_db",folder_path)
      
    def process_pdf_files(self,files):
        RetrievalQAWithLLMApp.vectorstore = self.embedObj.process_uploaded_file_and_make_temp_vectors(files,RetrievalQAWithLLMApp.vectorstore)
        self.chain =None
        self.create_chain()
        print("again ",end="")
        
    def create_chain(self):
        if RetrievalQAWithLLMApp.chain is None:
            RetrievalQAWithLLMApp.vectorstore = self.embedObj.load_vectore_stores("FAISS_db",RetrievalQAWithLLMApp.vectorstore)
            RetrievalQAWithLLMApp.chain = RetrievalQA.from_chain_type(
                llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.8, "max_length":4096,"max_new_tokens":4096}),
                chain_type="stuff",
                retriever=RetrievalQAWithLLMApp.vectorstore.as_retriever(search_kwargs={"k": 5}),    
                # return_source_documents=True,
                chain_type_kwargs={"prompt": self.prompt}, #"verbose": True},
            )
            print("chain created ------------------------------------")

    def ask_question(self, question: str):
        # Ensure the chain is created
        # Use the chain to ask the question
        try:
            response = RetrievalQAWithLLMApp.chain({"query":question, "early_stopping":True,"min_length":100,"max_tokens":1500})
            return response["result"]
        except Exception as e:
            return "Retry to ask question!, An error message: "+ str(e)
        