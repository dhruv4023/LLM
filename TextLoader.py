from langchain.document_loaders import TextLoader, UnstructuredPDFLoader, YoutubeLoader



pages = TextLoader("output.txt", encoding="utf8").load()

from langchain.vectorstores import FAISS
from langchain.embeddings import  HuggingFaceInstructEmbeddings

HFIembeddings = HuggingFaceInstructEmbeddings(model_name="thenlper/gte-small")
vectorstore = FAISS.from_documents(pages,embedding=HFIembeddings)
# docs=pages.load()
# from langchain.indexes import VectorstoreIndexCreator
# vectorStore =  #.from_loaders([pages])
# print(vectorStore)
print(vectorstore)