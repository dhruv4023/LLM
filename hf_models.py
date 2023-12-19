from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

question = "what is flower"

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

# repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1"  
# repo_id = "databricks/dolly-v2-3b"
# repo_id = "microsoft/phi-2"
repo_id = "google/flan-t5-base"

llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
)
llm_chain = LLMChain(prompt=prompt, llm=llm)

print(llm_chain.run(question))