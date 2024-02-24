import os
from firebase_admin import credentials, initialize_app, storage
cred = credentials.Certificate("chat_llb_ferebaser_serviceAccountKey.json")
initialize_app(cred, {'storageBucket': "chatbot-llb.appspot.com"})

bucket = storage.bucket()
def store_file(fileName):
    # Put your local file path 
    blob = bucket.blob("dhruv/"+os.path.basename(fileName))
    blob.upload_from_filename(fileName)
    blob.make_public()
    return blob.public_url

# print("your file url", blob.public_url)
# fileName = "D:\Files\LLM\Project\FAISS_db\IPC_186045.faiss"
# # fileName = "D:\Files\LLM\Project\FAISS_db\IPC_186045.pkl"


blob = bucket.blob("dhruv/IPC_186045.faiss")
content = blob.download_as_string()
# Now you can use the content of the file
print(content)
