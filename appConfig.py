import os
import logging
from dotenv import load_dotenv

load_dotenv()


class ENV_VAR():
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
    HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    MONGO_DB_NAME_CACHE = os.environ.get("MONGO_DB_NAME_CACHE")
    JWT_SECRET = os.environ.get("JWT_SECRET")


class CONST_VAR():
    TEXT_GENERATOR_MODEL_REPO_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    EMBEDDING_MODEL_REPO_ID = "sentence-transformers/all-MiniLM-L6-v2"
    TEMPLATE_CONTEXT = """
        Use the following pieces of context to answer the question at the end.
        You should prefer information which are more related to asked question.
        Make sure to rely on information from text only and not on questions to provide accurate responses.
        When you find particular answer in given text, display its context useful, make sure to cite it in the your answer.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        You can only use the given to you to answer the question.
        Generate concise answers and relevant data related to the asked question.
        You must represent the answer in proper format such as make points highlight some major information.
        don't attach your created quetions. if you don't get answer from the given text just say i don't know and terminate answering.
        if you get answer from the text than write all about the asked quetion and relevant data related to it.    
        don't use your own knowledge just use the provided text to answer the question.  
    """


class LOG:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def configure_logging(level=logging.INFO):
        logging.basicConfig(level=level)  # Set the logging level
        
    @staticmethod
    def debug(msg):
        logging.debug(msg)
        
    @staticmethod
    def info(msg):
        logging.info(msg)
        
    @staticmethod
    def warning(msg):
        logging.warning(msg)
        
    @staticmethod
    def error(msg):
        logging.error(msg)
        
    @staticmethod
    def critical(msg):
        logging.critical(msg)

LOG.configure_logging()  # Set logging level to INFO
