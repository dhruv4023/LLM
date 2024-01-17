
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Load the tokenizer and model
model_name = "./Models//distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Create a summarization pipeline
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
def generate_legal_notice(source_data):

    chunks,src_pg_nms=extractData(source_data)
 
    # summaries = ""
    # for chunk in chunks:
    #     print("summerizing...","chunk size: ",len(chunk))
    #     summary = summarizer(chunk, max_length=300, min_length=50, length_penalty=2.0, num_beams=5, early_stopping=True)
    #     summaries += "\n-"+summary[0]['summary_text']
    # print("data summerized")
    # return summaries,src_pg_nms
    return source_data,src_pg_nms

def extractData(docs):
    # Iterate through the documents
    page_content=[]
    src_pg_nms=[]
    for idx, doc in enumerate(docs):
        # Access page content
        page_content.append(str(doc.page_content).replace('\n', ''))
        # Access metadata
        metadata = doc.metadata
        # Access specific metadata fields
        source = metadata.get('source', 'N/A')
        page_number = metadata.get('page', 'N/A')
        src_pg_nms.append("Source:"+source+", Page Number:"+str(page_number))
    return page_content,src_pg_nms