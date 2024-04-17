from src.config.appConfig import ENV_VAR, CONST_VAR, LOG
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain.vectorstores.faiss import FAISS
from huggingface_hub import login

login(
    token=ENV_VAR.HUGGINGFACEHUB_API_TOKEN, 
    write_permission=True,
    add_to_git_credential=True,
)


class MongoChainGenerator:
    LLM = None

    def __init__(
        self,
        embedding_model,
        template_context,
        db_collection_name=None,
        tmp_vector_embedding=None,
    ):
        if db_collection_name:
            self._load_vectors(embedding_model, db_collection_name)
        else:
            self._create_tmp_retriever(tmp_vector_embedding)

        self._initialize_prompt(template_context)

        if MongoChainGenerator.LLM is None:
            self._initialize_llm()

    def _create_tmp_retriever(self, tmp_vector_embedding: FAISS):
        self.qa_retriever = tmp_vector_embedding.as_retriever(
            search_type="similarity", search_kwargs={"k": 7}
        )
        LOG.debug("Temporary retriever created")

    def _load_vectors(self, embedding_model, db_collection_name):
        self.qa_retriever = MongoDBAtlasVectorSearch.from_connection_string(
            connection_string=ENV_VAR.MONGO_DB_URL,
            namespace=ENV_VAR.MONGO_DB_NAME + "." + db_collection_name,
            embedding=embedding_model,
        ).as_retriever(search_type="similarity", search_kwargs={"k": 7})
        LOG.debug("Retriever loaded from MongoDB Atlas")

    def _initialize_prompt(self, template_context):
        template = (
            template_context
            + """
        {context}
        
        Question: {question} all related details.
        Answer:"""
        )
        self.prompt = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )
        LOG.debug("Prompt template initialized")

    def _initialize_llm(self):
        MongoChainGenerator.LLM = HuggingFaceEndpoint(
            repo_id=CONST_VAR.TEXT_GENERATOR_MODEL_REPO_ID,
            temperature=0.8,
            max_new_tokens=4096,
        )
        # MongoChainGenerator.LLM = HuggingFaceHub(repo_id=CONST_VAR.TEXT_GENERATOR_MODEL_REPO_ID, model_kwargs={"temperature": 0.85, "return_full_text": False, "max_length": 4096, "max_new_tokens": 4096})
        LOG.info("LLM initialized")

    def generate_retrieval_qa_chain(self):
        chain = RetrievalQA.from_chain_type(
            llm=MongoChainGenerator.LLM,
            retriever=self.qa_retriever,
            chain_type_kwargs={"prompt": self.prompt},
        )
        LOG.debug("Retrieval QA chain generated")
        return chain
