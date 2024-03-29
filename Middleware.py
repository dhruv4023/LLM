from MongoChainGenerator import *
from MongoEmbeddingGenerator import *
from DATABASE import *
from appConfig import LOG


class Main:
    qa_chains = {}
    embedding_generator = None

    def __init__(self) -> None:
        DATABASE()
        self._initialize_embedding_generator()
        self._load_existing_qa_chains()

    def _initialize_embedding_generator(self):
        if Main.embedding_generator is None:
            Main.embedding_generator = MongoEmbeddingGenerator(repo_id=CONST_VAR.EMBEDDING_MODEL_REPO_ID)
            LOG.debug("Embedding generator initialized")

    def _load_existing_qa_chains(self):
        chats = DATABASE.client["chatData"]["chats"].find()
        for chat in chats:
            if chat["collectionName"] not in Main.qa_chains:
                self.create_exist_chains(chat)

    def create_exist_chains(self, chat):
        if chat["collectionName"] not in Main.qa_chains:
            qa_generator = MongoChainGenerator(
                embedding_model=Main.embedding_generator.embedding_model,
                db_collection_name=chat["collectionName"],
                template_context=chat["templateContext"]
            )
            Main.qa_chains[chat["collectionName"]] = qa_generator.generate_retrieval_qa_chain()
            LOG.debug("Chain created for collection " + chat["collectionName"])
        else:
            LOG.debug("Chain already exists for collection " + chat["collectionName"])

    def generate_embedding(self, content: str, file_name: str, collection_name: str):
        return Main.embedding_generator.generate_embeddings(content, file_name, collection_name)

    def generate_tmp_embedding_and_chain(self, contents: str, tmp_collection_name):
        qa_generator = MongoChainGenerator(
            embedding_model=Main.embedding_generator.embedding_model,
            template_context=CONST_VAR.TEMPLATE_CONTEXT,
            tmp_vector_embedding=Main.embedding_generator.generate_tmp_embeddings(pdf_bytes=contents)
        )
        Main.qa_chains[tmp_collection_name] = qa_generator.generate_retrieval_qa_chain()
        LOG.debug(tmp_collection_name + ' chain created')

    def ask_question(self, question: str, collection_name):
        if collection_name in Main.qa_chains:
            try:
                LOG.debug(collection_name + " answering")
                response = Main.qa_chains[collection_name]({"query": question, "early_stopping": True, "min_length": 2000, "max_tokens": 5000})
                return response["result"]
            except Exception as e:
                LOG.error("An error occurred while answering question: {}".format(str(e)))
                return "Retry to ask question! An error occurred: {}".format(str(e))
        else:
            LOG.warning("Chain for collection '{}' not found.".format(collection_name))
            return "Chain for collection '{}' not found.".format(collection_name)

    def check_collection_name(self, collection_name):
        return collection_name in self.qa_chains