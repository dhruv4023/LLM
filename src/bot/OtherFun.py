from fastapi import UploadFile
import asyncio
from src.bot.main import Main
from src.config.appConfig import LOG


def delete_chain_after_delay(model: Main, chain_name: str):
    async def delete_chain():
        try:
            await asyncio.sleep(7200)  # Sleep for 2 hours
            if chain_name in model.qa_chains:
                del model.qa_chains[chain_name]
                # Log deletion
                LOG.info(f"Chain '{chain_name}' deleted after 2 hours")
        except Exception as e:
            LOG.error(f"An error occurred while deleting chain '{chain_name}': {e}")

    return delete_chain


async def process_file(model: Main, collection_name: str, file: UploadFile):
    try:
        contents = await file.read()

        file_extension = file.filename.split(".")[-1]

        if file_extension == "pdf":
            response = model.generate_embedding(
                contents, file.filename, collection_name)
        elif file_extension == "txt":
            response = contents.decode("utf-8")
        else:
            raise ValueError(f"Unsupported file format for {file.filename}")

        return response
    except Exception as e:
        LOG.error(f"An error occurred while processing file '{file.filename}': {e}")
        return f"Error processing file '{file.filename}': {e}"
