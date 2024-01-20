from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader   
from langchain.vectorstores import FAISS
from langchain.embeddings import  HuggingFaceInstructEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub

# from write_in_file import generate_docx_with_bullets
from data_extracter import extract_data_from_response


load_dotenv()


def make_model(files):

    def load_pdf_files(files):
        loader = PyPDFLoader(files[0])
        pages = loader.load_and_split()
        for i in range(1,len(files)): 
            loader = PyPDFLoader(files[i])
            pages += loader.load_and_split()
        return pages

    pages=load_pdf_files(files)
    print("pages in PDF files: ",len(pages))

    template = """

    {context}


    Question: {question}
    Answer:"""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # HFIembeddings = HuggingFaceInstructEmbeddings(model_name="WhereIsAI/UAE-Large-V1")
    HFIembeddings = HuggingFaceInstructEmbeddings(model_name="./Models/gte-small")
    # HFIembeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small")
    vectorstore = FAISS.from_documents(pages,embedding=HFIembeddings)
    print("vectore store created")

    chain = RetrievalQA.from_chain_type(
        llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.8, "max_length":4096,"max_new_tokens":4096}),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),    
        # retriever=vectorstore.as_retriever(),    
        return_source_documents=True,
        # kwargs={"max_length":4096,"min_length":1024},
        chain_type_kwargs={"prompt": prompt,"verbose": True},
    )
    print("model is ready")
    return chain
from flask import Flask, render_template, request
    
    
app = Flask(__name__)
app.config['TIMEOUT'] = 60*5

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':    
        q = str(request.json["q"])    
        # q="what is the punishmentf for robbery ?"
        # q="who is judge ?"
        # q="one person has commited defamation, what should be punishment for it?"
        # q="rioting has happened in neighbouring society. who will be responsible and what is the punishment for it"
        # q="what is punishment for robbery and also murder ?"
        # q="person is selling adulterated drugs which is harmful to the health of people. person has also sold drug to the children below age of 15 what will be punishment for it?"
        q+=" with section number. add all details"
        response = chain({"query":q, "early_stopping":True,"min_length":10000,"max_tokens":10000})

        result,src_data,src_pg_nms=extract_data_from_response(response)
        # generate_docx_with_bullets(heading=q,main_paragraph=result,srcs=src_pg_nms,output_folder="./tmp/")

        return {"result": result, "src_data": src_data, "src_pg_nms": src_pg_nms}
    else: 
        return 'Hello, welcome to the Flask server! pdf loaded send POST method with your question'

@app.route('/about')
def about():
    return 'This is a simple Flask server.'

if __name__ == '__main__': 
    files=["IPC_186045.pdf"]
    chain=make_model(files)
    app.run(debug=True)
