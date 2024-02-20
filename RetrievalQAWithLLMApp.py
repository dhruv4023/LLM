from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub
from appConfig import *
from GenerateEmbeddingFromPdfFile import *

class RetrievalQAWithLLMApp:
    chain = None
    vectorstore = None
    embedObj = GenerateEmbeddingFromPdfFile()
    def __init__(self):
        template = """
        You'r helpful AI assisant given the task to help people seeking advise.
        You have to help person by answering their question using provided documents only.
        Answer in step by step in points by highlighting major information.
        Refuse to answer if it is not provided in the provided documents also donot concoat anything.
        deny to answer the question if it is not provided in the text.
        do not include your created questions. just give answer of asked question.
        {context}

        Question: {question}  including all related details.
        Answer:"""


        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    def create_vector_and_store(self, folder_path: str):
        RetrievalQAWithLLMApp.embedObj.create_vectores_and_store_locally("FAISS_db", folder_path)

    def process_pdf_files(self, files):
        RetrievalQAWithLLMApp.vectorstore = RetrievalQAWithLLMApp.embedObj.process_uploaded_file_and_make_temp_vectors(files, RetrievalQAWithLLMApp.vectorstore)
        self.chain = None
        self.create_chain()
        print("again ", end="")

    def create_chain(self):
        if RetrievalQAWithLLMApp.chain is None:
            if RetrievalQAWithLLMApp.vectorstore is None:
                RetrievalQAWithLLMApp.vectorstore = RetrievalQAWithLLMApp.embedObj.load_vectore_stores("FAISS_db", RetrievalQAWithLLMApp.vectorstore)
            RetrievalQAWithLLMApp.chain = RetrievalQA.from_chain_type(
                llm=HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature": 0.8, "max_length": 4096, "max_new_tokens": 4096}),
                chain_type="stuff",
                retriever=RetrievalQAWithLLMApp.vectorstore.as_retriever(search_kwargs={"k": 5}),
                chain_type_kwargs={"prompt": self.prompt},
            )
            print("chain created ------------------------------------")

    def ask_question(self, question: str):
        try:
            response = RetrievalQAWithLLMApp.chain({"query": question, "early_stopping": True, "min_length": 100, "max_tokens": 1500})
            return response["result"]
        except Exception as e:
            return "Retry to ask question!, An error message: " + str(e)
