#
from dotenv import load_dotenv
load_dotenv()

#
def load_pdf_files(files):
    from langchain.document_loaders import PyPDFLoader
    loader = PyPDFLoader(files[0])
    pages = loader.load_and_split()
    for i in range(1,len(files)): 
        loader = PyPDFLoader(files[i])
        pages += loader.load_and_split()
    return pages


# files=["IPC_186045.pdf","Bharatiya_Nyaya_Sanhita,_2023.pdf"]
files=["IPC_186045.pdf"]
pages=load_pdf_files(files)
print("PDF files: ",len(pages))


from langchain.prompts import PromptTemplate

# context="also write the page number accouding to file with file name"

# Answer with analogies from the files to the question with the page number accouding to file with file name
template = """

{context}


Question: {question}
Answer:"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])
# print(
#     prompt.format(
#         question="who is judge?",
#     )
# )



from langchain.vectorstores import FAISS
from langchain.embeddings import  HuggingFaceInstructEmbeddings

# HFIembeddings = HuggingFaceInstructEmbeddings(model_name="WhereIsAI/UAE-Large-V1")
HFIembeddings = HuggingFaceInstructEmbeddings(model_name="./Models/gte-small")
# HFIembeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small")
vectorstore = FAISS.from_documents(pages,embedding=HFIembeddings)
print("vectore store created")


from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub

    # llm = HuggingFaceHub(repo_id="HuggingFaceH4/zephyr-7b-beta", model_kwargs={"temperature":0.7}), # best
    
    # llm = HuggingFaceHub(repo_id="TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T", model_kwargs={"temperature":0.5, "max_length":"512"}),
    # llm = HuggingFaceHub(repo_id="meta-llama/Llama-2-7b-chat-hf", model_kwargs={"temperature":0.5, "max_length":"512"}),
    # llm = HuggingFaceHub(repo_id="cognitivecomputations/dolphin-2.5-mixtral-8x7b", model_kwargs={"temperature":0.5, "max_length":"512"}),
    # llm = HuggingFaceHub(repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", model_kwargs={"temperature":0.7, "max_length":"400"}),
    # llm = HuggingFaceTextGenInference(max_new_tokens=512,temperature= 0.8),
    # llm = HuggingFaceHub(repo_id="microsoft/phi-2", model_kwargs={"temperature":0.5, "max_length":"10000"},trust_remote_code=True),
llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.8,"max_length":4096,"min_length":1024}), # best
# llm=HuggingFaceHub(repo_id=)
chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 7}),    
    return_source_documents=True,
    kwargs={"max_length":4096,"min_length":1024},
    chain_type_kwargs={"prompt": prompt,"verbose": True},
)
    # retriever=vectorstore.as_retriever(),    

def print_response(response: str):
    print("-----------------------")
    print("Answer: ")
    # print("\n".join(textwrap.wrap(response, width=100)))
    print(response)
    print("-----------------------")

# response = chain.run("punishment for dacoit")
# print_response(response)
from doxGenerator import generate_docx_with_bullets
from Generate_more_text import generate_legal_notice
while(True):
    q = input("Enter your query: ")
    # q += "in which section"
    response = chain({"query":q, "early_stopping":True,"min_length":500})
    bullets,src_pg_nms=generate_legal_notice(response["source_documents"])
    print_response(response["result"])
    bullets=(response["result"])
    generate_docx_with_bullets(question=q,answer=response["result"],content=bullets,srcs=src_pg_nms ,output_folder="./tmp/")
