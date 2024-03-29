# LLM CHATHUB - chatAPI

## Requirements
### Python Version
- [python 3.9.13](https://www.python.org/downloads/release/python-3913/) 

### Huggingface API
- Generate your API key and place it in the .env file:
    ```
    HUGGINGFACEHUB_API_TOKEN=""
    ```
### MongoDB Atlas Database
- generate your Mongodb Database URL

## Setup Environment

### Option 1: Automated Setup (PowerShell)
- Run `CreateEnv.ps1` file in PowerShell. It will:
    - Create a virtual environment
    - Activate it
    - Create temporary folders
    - Install necessary Python modules

### Option 2: Manual Setup
- Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
- Activate virtual environment:
    ```bash
    .venv\Scripts\Activate.ps1
    ```
- Install Python modules:
    ```bash
    python -m pip install -r "requirements.txt"
    ```
- Create folders:
    - Models (if you want to download manually) (Not necessary)

## References
- [YouTube Video Reference](https://www.youtube.com/watch?v=dXxQ0LR-3Hg&t=123s)
- [GitHub](https://github.com/curiousily/Get-Things-Done-with-Prompt-Engineering-and-LangChain)
- [MongoDB](https://www.mongodb.com/docs/)  
- [React JS](https://reactjs.org/docs/getting-started.html) 
- [LangChain](https://python.langchain.com/docs/get_started/introduction) 
- [HuggingFaceHub](https://huggingface.co   ) 


### Models
- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Mixtral](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1)


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


## Other Repository URL for whole project
- [Front end](https://github.com/dhruv4023/ChatBotAppClient)
- [Main Node Server](https://github.com/dhruv4023/ChatBotServerNode)
- [Authentication Server](https://github.com/dhruv4023/AuthMicroService)