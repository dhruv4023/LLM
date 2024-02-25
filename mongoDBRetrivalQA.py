import os
from langchain.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain.embeddings.huggingface_hub import HuggingFaceHubEmbeddings
from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from appConfig import *
from pymongo import MongoClient
from langchain.document_loaders.pdf import PyPDFLoader

class EmbeddingGenerator:
    client = None
    def __init__(self, repo_id):
        if EmbeddingGenerator.client is None: EmbeddingGenerator.client = MongoClient(MONGO_DB_URL)
        self.embedding_model = HuggingFaceHubEmbeddings(repo_id=repo_id)
    
    def generate_embeddings(self,file_path,collection_name:str):
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        if EmbeddingGenerator.client[MONGO_DB_NAME_CACHE][collection_name].find_one({"src_file_name":os.path.basename(file_path)}):
            print("vectors already exist in mongodb")
        else:
            EmbeddingGenerator.client[MONGO_DB_NAME_CACHE][collection_name].insert_one({"src_file_name":os.path.basename(file_path)})
            MongoDBAtlasVectorSearch.from_documents(documents=pages, embedding=self.embedding_model, collection=EmbeddingGenerator.client[MONGO_DB_NAME][collection_name])
            print("vectors stored in mongodb")

class RetrievalQAGenerator:
    def __init__(self, EMBEDDING_MODEL, DB_COLLECTION_NAME="general"):
        load_vectors = MongoDBAtlasVectorSearch.from_connection_string(
            connection_string = MONGO_DB_URL,
            namespace = MONGO_DB_NAME + "." + DB_COLLECTION_NAME,
            embedding = EMBEDDING_MODEL,
        )
        self.qa_retriever = load_vectors.as_retriever(search_type="similarity",search_kwargs={"k": 25})
        
        template = """
        You're helpful AI assistant given the task to help people seeking law advice.
        You have to help a person to use the Indian laws in a legal manner.
        Answer in step by step points by highlighting the sections of Indian laws & constitution.
        Refuse to answer if it is not helping in legal affairs, also do not conceal anything.
        Deny to answer the question if it is not provided in the text.
        {context}
        
        Question: {question} including section number and all related details.
        Answer:"""
        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        self.llm = HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.8, max_new_tokens=4096)

    def generate_retrieval_qa_chain(self):
        print("creating chain")
        chain= RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.qa_retriever,
            chain_type_kwargs={"prompt": self.prompt},
        )
        print('chain creating')
        return chain

class Main:
    qa_chain = None
    embedding_generator = None
    def __init__(self) -> None:
        if Main.embedding_generator is None:
            Main.embedding_generator = EmbeddingGenerator(repo_id="sentence-transformers/all-MiniLM-L6-v2")
        if Main.qa_chain is None:
            qa_generator = RetrievalQAGenerator(EMBEDDING_MODEL=Main.embedding_generator.embedding_model)
            Main.qa_chain = qa_generator.generate_retrieval_qa_chain()
    
    def generate_new_chain(self,collection_name:str):
            qa_generator = RetrievalQAGenerator(EMBEDDING_MODEL=Main.embedding_generator.embedding_model,DB_COLLECTION_NAME=collection_name)
            Main.qa_chain = qa_generator.generate_retrieval_qa_chain()
    
    def generate_embedding(self,file_path:str,collection_name="general"):
        Main.embedding_generator.generate_embeddings(file_path,collection_name)

    def ask_question(self, question: str):
        try:
            response = Main.qa_chain({"query":question, "early_stopping":True,"min_length":2000,"max_tokens":5000})
            return response["result"]
        except Exception as e:
            return "Retry to ask question!, An error message: "+ str(e)
