# %%
from dotenv import load_dotenv
load_dotenv()

# %%
def load_pdf_files(files):
    from langchain.document_loaders import PyPDFLoader
    loader = PyPDFLoader(files[0])
    pages = loader.load_and_split()
    for i in range(1,len(files)): 
        loader = PyPDFLoader(files[i])
        pages += loader.load_and_split()
    return pages

# %%
files=["IPC_186045.pdf"]
pages=load_pdf_files(files)
print("PDF files: ",len(pages))

# %%
from langchain.prompts import PromptTemplate
template = """

{context}


Question: {question}
Answer:"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# %%
from langchain.vectorstores import FAISS
from langchain.embeddings import  HuggingFaceInstructEmbeddings

# HFIembeddings = HuggingFaceInstructEmbeddings(model_name="WhereIsAI/UAE-Large-V1")
HFIembeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small",cache_folder="./Models/")
vectorstore = FAISS.from_documents(pages,embedding=HFIembeddings)
print("vectore store created")

# %%

from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub
chain = RetrievalQA.from_chain_type(
    llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.8, "max_length":4096,"max_new_tokens":4096}),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),    
    # retriever=vectorstore.as_retriever(),    
    return_source_documents=True,
    # kwargs={"max_length":4096,"min_length":1024},
    chain_type_kwargs={"prompt": prompt,"verbose": True},
)

# %%
# q="what is the punishmentf for robbery ?"
# q="who is judge ?"
q="one person has commited defamation, what should be punishment for it?"
# q="rioting has happened in neighbouring society. who will be responsible and what is the punishment for it"
# q="what is punishment for robbery and also murder ?"
# q="person is selling adulterated drugs which is harmful to the health of people. person has also sold drug to the children below age of 15 what will be punishment for it?"
q+="with section number. add all details"
response = chain({"query":q, "early_stopping":True,"min_length":5000,"max_tokens":5000})

from write_in_file import generate_docx_with_bullets
from data_extracter import extract_data_from_response
result,src_data,src_pg_nms=extract_data_from_response(response)
generate_docx_with_bullets(heading=q,main_paragraph=result,srcs=src_pg_nms,output_folder="./tmp/")

# %%


# %%
# def write_in_notepad(response):
#     from write_in_file import open_in_notepad
#     open_in_notepad(response["result"])





