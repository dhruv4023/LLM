import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceHubEmbeddings,HuggingFaceInstructEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from appConfig import *

class CreateChunks:
    def get_pdf_text(self, pdf_docs):
        texts = []
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                texts.append(page.extract_text())
        return "\n".join(texts)

    def get_text_chunks(self, files):
        text = self.get_pdf_text(files)
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        return text_splitter.split_text(text)

    def split_docs(self, pdf_file_path, chunk_size=1000, chunk_overlap=20):
        docs = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap).split_documents(PyPDFLoader(pdf_file_path).load_and_split())
        return docs
    
class EmbeddingGenerater:
    def __init__(self):
        self.chunkObj = CreateChunks()
        self.HFIembeddings = HuggingFaceHubEmbeddings(repo_id="sentence-transformers/all-MiniLM-L6-v2")
        # self.HFIembeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small", cache_folder="./Models/",model_kwargs={"device": DEVICE})

    def process_uploaded_file_and_make_temp_vectors(self, files, current_vector_store: FAISS):
        for file in files:
            texts = self.chunkObj.get_text_chunks(files)
            current_vector_store.merge_from(FAISS.from_texts(texts, embedding=self.HFIembeddings))
            print("Vectors merged of:", file)
        return current_vector_store

    def create_vectores_and_store_locally(self, vector_store_folder_name: str, folder_path: str):
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
        print("FAISS Vector files loaded")
        return current_vector_store
