def extract_data_from_response(response):
    # Iterate through the documents
    src_data=[]
    src_pg_nms=[]
    for idx, doc in enumerate(response["source_documents"]):
        # Access page content
        src_data.append(str(doc.page_content).replace('\n', ''))
        # Access metadata
        metadata = doc.metadata
        # Access specific metadata fields
        source = metadata.get('source', 'N/A')
        page_number = metadata.get('page', 'N/A')
        src_pg_nms.append("- Source:"+source+", Page Number:"+str(page_number))
    result=response["result"]
    return result,src_data,src_pg_nms