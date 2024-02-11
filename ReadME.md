# Chatbot for Question Answering on Legal Documents

## Requirements
### Python Version
- Python 3.9.10

### Huggingface API
- Generate your API key and place it in the .streamlit/secrets.toml file:
    ```
    [env]
    HUGGINGFACEHUB_API_TOKEN="your_huggingfacehub_api_key"
    ```

## Setup Environment

### Steps
- Create a virtual environment:
    ```bash
    python -m venv venv
    ```
- Activate virtual environment:
    ```bash
    venv\Scripts\Activate.ps1
    ```
- Install Python modules:
    ```bash
    python -m pip install -r "requirements.txt"
    ```

## References

### Reference documents and videoes
- [YouTube Video Reference](https://www.youtube.com/watch?v=dXxQ0LR-3Hg&t=123s)
- [GitHub](https://github.com/curiousily/Get-Things-Done-with-Prompt-Engineering-and-LangChain)
- [LangChain Documentory](https://python.langchain.com/docs/get_started/introduction)

### Models
- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (sentence transformers model for embedding)
- [Mixtral](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1) (text generation model)

### Data Source Documents
- [The Indian Penal Code](https://www.iitk.ac.in/wc/data/IPC_186045.pdf)
- [Transfer of Property Act 1882](https://www.indiacode.nic.in/bitstream/123456789/2338/1/A1882-04.pdf)
- [Indian Stamp Act](https://registration.uk.gov.in/files/Stamp_Act_Eng.pdf)
- [The Land Acquisition Act](https://dolr.gov.in/sites/default/files/THE%20LAND%20ACQUISITION%20ACT.pdf)
- [The Registration Act, 1908](https://www.indiacode.nic.in/bitstream/123456789/13236/1/the_registration_act%2C_1908.pdf)
- [The Muslim Marriages Registration Act, 1981](https://www.indiacode.nic.in/bitstream/123456789/5615/1/muslim_marriages_registration_act%2C_1981.pdf)
- [The Indian Evidence Act, 1872](https://www.indiacode.nic.in/bitstream/123456789/2187/2/A187209.pdf)
- [Companies Act 2013](https://www.icsi.edu/media/webmodules/companiesact2013/COMPANIES%20ACT%202013%20READY%20REFERENCER%2013%20AUG%202014.pdf)
- [Indian Evidence Act 1872](https://www.indiacode.nic.in/bitstream/123456789/15351/1/iea_1872.pdf)
- [Indian Penal Code 1860](https://www.iitk.ac.in/wc/data/IPC_186045.pdf)
- [Code of Criminal Procedure](https://highcourtchd.gov.in/hclscc/subpages/pdf_files/4.pdf)
- [Information Technology Act 2000](https://cdnbbsr.s3waas.gov.in/s380537a945c7aaa788ccfcdf1b99b5d8f/uploads/2023/05/2023050195.pdf)
- [Code of Civil Procedure 1908](https://sclsc.gov.in/theme/front/pdf/ACTS%20FINAL/THE%20CODE%20OF%20CIVIL%20PROCEDURE,%201908.pdf)
- [The Indian Christian Marriage Act 1872](https://ncwapps.nic.in/acts/TheIndianChristianMarriageAct1872-15of1872.pdf)
- [Negotiable Instruments Act 1881](https://www.indiacode.nic.in/bitstream/123456789/2347/1/190907.pdf)
- [The Indian Partnership Act, 1932](https://www.indiacode.nic.in/bitstream/123456789/2280/1/A1869-04.pdf)
- [Special Marriage Act 1954](https://www.indiacode.nic.in/bitstream/123456789/15480/1/special_marriage_act.pdf)
