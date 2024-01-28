# Generate Data Using HuggingFace Text-generator Model

## Requirements
### Python Version
- Python 3.9.10

### Huggingface API
- Generate your API key and place it in the .env file:
    ```
    HUGGINGFACEHUB_API_TOKEN=""
    ```

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
- Create folders:
    1. Outputs
    2. Models (if you want to download manually) (Not necessary)

## References
- [YouTube Video Reference](https://www.youtube.com/watch?v=dXxQ0LR-3Hg&t=123s)
- [GitHub](https://github.com/curiousily/Get-Things-Done-with-Prompt-Engineering-and-LangChain)

### Models
- [gpt2](https://huggingface.co/gpt2)
- [gte-small](https://huggingface.co/thenlper/gte-small)
- [Mixtral](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1)

### PDF Documents
- [The Indian Penal Code](https://www.iitk.ac.in/wc/data/IPC_186045.pdf)


### HuggingFaceHub Repository link: 
- https://huggingface.co/spaces/dhruv4023/llmproject