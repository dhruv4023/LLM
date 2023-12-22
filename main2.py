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
files=["Bharatiya_Nyaya_Sanhita,_2023.pdf"]
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

HFIembeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small")
vectorstore = FAISS.from_documents(pages,embedding=HFIembeddings)



from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub

chain_type_kwargs = {"prompt": prompt}
chain = RetrievalQA.from_chain_type(
    llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.5, "max_length":512}),
    chain_type="stuff",
    # retriever=vectorstore.as_retriever(search_kwargs={"k": 1}),    
    retriever=vectorstore.as_retriever(),    
    chain_type_kwargs=chain_type_kwargs,
)

def print_response(response: str):
    import textwrap
    print("\n".join(textwrap.wrap(response, width=100)))
    
response = chain.run("what is penalty for robbery?")
print_response(response)
# response = chain.run("what is penalty for robbery?")
# print_response(response)