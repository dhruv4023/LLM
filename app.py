import time
import streamlit as st
from components import *
from RetrievalQAWithLLMApp import RetrievalQAWithLLMApp 
# API_ENDPOINT = 'http://127.0.0.1:8000/ask'

st.set_page_config(
    page_title="IPC Q&A App",
    page_icon="📘",
    layout="wide"
) 

reference_documents = {
    "Transfer of Property Act 1882": "https://www.indiacode.nic.in/bitstream/123456789/2338/1/A1882-04.pdf",
    "Indian Stamp Act": "https://registration.uk.gov.in/files/Stamp_Act_Eng.pdf",
    "The Land Acquisition Act": "https://dolr.gov.in/sites/default/files/THE%20LAND%20ACQUISITION%20ACT.pdf",
    "The Registration Act, 1908": "https://www.indiacode.nic.in/bitstream/123456789/13236/1/the_registration_act%2C_1908.pdf",
    "The Muslim Marriages Registration Act, 1981": "https://www.indiacode.nic.in/bitstream/123456789/5615/1/muslim_marriages_registration_act%2C_1981.pdf",
    "The Indian Evidence Act, 1872": "https://www.indiacode.nic.in/bitstream/123456789/2187/2/A187209.pdf",
    "Companies Act 2013": "https://www.icsi.edu/media/webmodules/companiesact2013/COMPANIES%20ACT%202013%20READY%20REFERENCER%2013%20AUG%202014.pdf",
    "Indian Evidence Act 1872": "https://www.indiacode.nic.in/bitstream/123456789/15351/1/iea_1872.pdf",
    "Indian Penal Code 1860": "https://www.iitk.ac.in/wc/data/IPC_186045.pdf",
    "Code of Criminal Procedure": "https://highcourtchd.gov.in/hclscc/subpages/pdf_files/4.pdf",
    "Information Technology Act 2000": "https://cdnbbsr.s3waas.gov.in/s380537a945c7aaa788ccfcdf1b99b5d8f/uploads/2023/05/2023050195.pdf",
    "Code of Civil Procedure 1908": "https://sclsc.gov.in/theme/front/pdf/ACTS%20FINAL/THE%20CODE%20OF%20CIVIL%20PROCEDURE,%201908.pdf",
    "The Indian Christian Marriage Act 1872": "https://ncwapps.nic.in/acts/TheIndianChristianMarriageAct1872-15of1872.pdf",
    "Negotiable Instruments Act 1881": "https://www.indiacode.nic.in/bitstream/123456789/2347/1/190907.pdf",
    "The Indian Partnership Act, 1932": "https://www.indiacode.nic.in/bitstream/123456789/2280/1/A1869-04.pdf",
    "Special Marriage Act 1954": "https://www.indiacode.nic.in/bitstream/123456789/15480/1/special_marriage_act.pdf"
}

# RetrievalQAWithLLMApp.files = [value for value in reference_documents.values()]
RetrievalQAWithLLMApp.files=["D:\Files\LLM\Project\DataSourceFiles\IPC_186045.pdf"]

model = RetrievalQAWithLLMApp()
if model.chain is None:
    with st.spinner("Processing"):
        model.create_chain()


def main(): 
    header()
    # Input box inside the sticky container
    question = st.text_input(
        label="Enter your query👇",
        key="question_input",
        placeholder="Ask a question about Indian Constitution...",
        label_visibility="collapsed"
    )
    if question:
        with st.spinner("Thinking..."):
            st.session_state.chat_history.append({"q": question})
            start_time = time.time()
            ans = model.ask_question(question)
            end_time = time.time()
            # ans="hello"
            st.session_state.chat_history.append({"a": ans})
            print_history()
            st.markdown("##### Time taken to generate answer: "+str(end_time-start_time)+" seconds)")
        
if __name__ == "__main__":
    main()