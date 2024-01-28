from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceHubEmbeddings,HuggingFaceInstructEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub

class RetrivalQAModel:
    # Class attributes for static variables
    files = ["IPC_186045.pdf"]
    # hfi_embeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small",cache_folder="../Models/")
    hfi_embeddings = HuggingFaceHubEmbeddings(repo_id="sentence-transformers/all-mpnet-base-v2")

    chain = None

    def __init__(self):
        # Initialize instance variables
        self.vectorstore = None
        template = """
            You'r helpful AI assisant given the task to help people seeking law advise.
            You have to help person to use the Indian laws in legal manner.
            Answer in step by step in points by highlighting the sections of indian laws & constitution.
            Refuse to answer if it is not helping in legal affairs, also donot concoat anything.
            {context}


            Question: {question}
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
        if RetrivalQAModel.chain is None:
            pages = self.load_pdf_files(RetrivalQAModel.files)

            vectorstore = FAISS.from_documents(pages, embedding=RetrivalQAModel.hfi_embeddings)

            RetrivalQAModel.chain = RetrievalQA.from_chain_type(
                llm=HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature": 0.8, "max_length": 4096, "max_new_tokens": 4096}),
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={"k": 7}),
                # return_source_documents=True,
                chain_type_kwargs={"prompt": self.prompt, "verbose": True},
            )

    def ask_question(self, question: str):
        # Ensure the chain is created
        self.create_chain()

        # Use the chain to ask the question
        response = RetrivalQAModel.chain({"query": question, "early_stopping": True, "min_length": 1000, "max_tokens": 5000})

        # Assuming you have a function to extract data from the response
        # result, src_data, src_pg_nms = extract_data_from_response(response)

        return response["result"]

# # Example usage:
# model = RetrivalQAModel()
# print(model.ask_question("who is judge ?"))
