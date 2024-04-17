from io import BytesIO
import PyPDF2
from src.config.appConfig import *
from src.config.databaseConfig import DATABASE

from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain.embeddings.huggingface_hub import HuggingFaceHubEmbeddings

class MongoEmbeddingGenerator:

    def __init__(self, repo_id):
        self.embedding_model = HuggingFaceHubEmbeddings(repo_id=repo_id, huggingfacehub_api_token=ENV_VAR.HUGGINGFACEHUB_API_TOKEN)
        LOG.info("Embedding model initialised")

    def _extract_text_from_pdf(self, pdf_bytes):
        pdf_file = BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        return [pdf_reader.pages[page_num].extract_text() for page_num in range(len(pdf_reader.pages))]

    def generate_tmp_embeddings(self, pdf_bytes):
        texts = self._extract_text_from_pdf(pdf_bytes)
        return FAISS.from_texts(texts=texts, embedding=self.embedding_model)

    def generate_embeddings(self, pdf_bytes, file_name: str, collection_name: str):
        client = DATABASE.client
        if client[ENV_VAR.MONGO_DB_NAME_CACHE][collection_name].find_one({"src_file_name": file_name}):
            LOG.debug(f"Vectors already exist in MongoDB for file {file_name}")
            return f"Vectors already exist in MongoDB for file {file_name}"
        else:
            texts = self._extract_text_from_pdf(pdf_bytes)
            client[ENV_VAR.MONGO_DB_NAME_CACHE][collection_name].insert_one({"src_file_name": file_name})
            MongoDBAtlasVectorSearch.from_texts(texts=texts, embedding=self.embedding_model, collection=client[ENV_VAR.MONGO_DB_NAME][collection_name])
            LOG.debug(f"Vectors stored in MongoDB for file {file_name}")
            return f"Vectors stored in MongoDB for file {file_name}"
