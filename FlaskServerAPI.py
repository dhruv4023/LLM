#
from dotenv import load_dotenv
load_dotenv()

def make_model(files):
    def load_pdf_files(files):
        from langchain.document_loaders import PyPDFLoader
        loader = PyPDFLoader(files[0])
        pages = loader.load_and_split()
        for i in range(1,len(files)): 
            loader = PyPDFLoader(files[i])
            pages += loader.load_and_split()
        return pages


    # files=["IPC_186045.pdf","Bharatiya_Nyaya_Sanhita,_2023.pdf"]
    pages=load_pdf_files(files)
    print("Pages: ",len(pages))


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
    HFIembeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small")
    vectorstore = FAISS.from_documents(pages,embedding=HFIembeddings)
    print("vectorstore created ----------------------------------------------------------------------")


    from langchain.chains import RetrievalQA
    from langchain.llms import HuggingFaceHub

    chain_type_kwargs = {"prompt": prompt}
    chain = RetrievalQA.from_chain_type(
        llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.9, "max_length":4096,"max_new_tokens":4096}),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),    
        # retriever=vectorstore.as_retriever(),    
        chain_type_kwargs=chain_type_kwargs,
    )
    print("model is ready !")
    return chain
    # response = chain.run("a person has done robbery ")
    # print_response(response)
from flask import Flask, render_template, request
app = Flask(__name__)
files=["IPC_186045.pdf"]
chain=make_model(files)
app.config['TIMEOUT'] = 60*5

from doxGenerator import generate_docx_with_bullets
from Generate_more_text import generate_legal_notice
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Access data from the POST request
        q = str(request.json["q"])
        response = chain.run(q+" in which section it is mentioned")
        generated_file_path=generate_docx_with_bullets(content=generate_legal_notice(response),output_folder="./Outputs/")
        return f'Q:{q}:\n A: {response}\n\n -> {generated_file_path}'
    else: 
        return 'Hello, welcome to the Flask server! pdf loaded send POST method with your question'

@app.route('/about')
def about():
    return 'This is a simple Flask server.'

if __name__ == '__main__':
    pdf_docs = ["parts.pdf"] 
    app.run(debug=True)
