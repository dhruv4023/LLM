
# from langchain.text_splitter import CharacterTextSplitter
# from PyPDF2 import PdfReader
# def get_pdf_text(pdf_docs):
#     text = ""
#     for pdf in pdf_docs:
#         i=0
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#             i+=1
#     print("---------------------------------------------------------------------------------------------------------")
#     print("Total size: ",len(text)," Bytes")
#     print("---------------------------------------------------------------------------------------------------------")
#     return (text)


# def get_text_chunks(text):
#     text_splitter = CharacterTextSplitter(
#         separator="\n",
#         chunk_size=1024,
#         chunk_overlap=200,
#         length_function=len
#     )
#     chunks = text_splitter.split_text(text)
#     return chunks

# # text=get_pdf_text(["parts.pdf"])
# # for i in (get_text_chunks(text)):
# #     print(i)

# # Assuming you have a text string named 'text_content'
# text_content = "Your long text here...\nLine 1\nLine 2\nLine 3\n..."

# # Create the CharacterTextSplitter
# text_splitter = CharacterTextSplitter(
#     separator="\n",
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=len
# )

# # Split the text into chunks
# chunks = text_splitter.split_text(text_content)

# # Process each chunk as needed
# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i + 1}: {chunk}")
import torch

# Check if GPU is available
x="GPU" if torch.cuda.is_available() else "CPU"
print(x)
