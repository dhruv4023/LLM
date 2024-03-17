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
        You're helpful AI assistant given the task to help people seeking advice.
        You have to help a person to use the texts in a legal manner.
        Answer in step by step points by highlighting the main points.
        Deny to answer the question if it is not provided in the text.
        do not make your quetions and answers. just answer the quetion asked to you.
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
