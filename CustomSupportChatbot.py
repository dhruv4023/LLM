from pathlib import Path

import torch
from auto_gptq import AutoGPTQForCausalLM
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from transformers import AutoTokenizer, GenerationConfig, TextStreamer, pipeline


# ## Data


# questions_dir = Path("skyscanner")
# questions_dir.mkdir(exist_ok=True, parents=True)


# def write_file(question, answer, file_path):
#     text = f"""
# Q: {question}
# A: {answer}
# """.strip()
#     with Path(questions_dir / file_path).open("w") as text_file:
#         text_file.write(text)


# write_file(
#     question="How do I search for flights on Skyscanner?",
#     answer="""
# Skyscanner helps you find the best options for flights on a specific date, or on any day in a given month or even year. For tips on how best to search, please head over to our search tips page.

# If you're looking for inspiration for your next trip, why not try our everywhere feature. Or, if you want to hang out and ensure the best price, you can set up price alerts to let you know when the price changes.
# """.strip(),
#     file_path="question_1.txt",
# )


# write_file(
#     question="What are mash-ups?",
#     answer="""
# These are routes where you fly with different airlines, because it`s cheaper than booking with just one. For example:

# If you wanted to fly London to New York, we might find it`s cheaper to fly out with British Airways and back with Virgin Atlantic, rather than buy a round-trip ticket with one airline. This is called a "sum-of-one-way" mash-up. Just in case you're interested.

# Another kind of mash-up is what we call a "self-transfer" or a "non-protected transfer". For example:

# If you wanted to fly London to Sydney, we might find it`s cheaper to fly London to Dubai with Emirates, and then Dubai to Sydney with Qantas, rather than booking the whole route with one airline.

# Pretty simple, right?

# However, what`s really important to bear in mind is that mash-ups are NOT codeshares. A codeshare is when the airlines have an alliance. If anything goes wrong with the route - a delay, say, or a strike - those airlines will help you out at no extra cost. But mash-ups DO NOT involve an airline alliance. So if something goes wrong with a mash-up, it could cost you more money.
# """.strip(),
#     file_path="question_2.txt",
# )


# write_file(
#     question="Why have I been blocked from accessing the Skyscanner website?",
#     answer="""
# Skyscanner's websites are scraped by bots many millions of times a day which has a detrimental effect on the service we're able to provide. To prevent this, we use a bot blocking solution which checks to ensure you're using the website in a normal manner.

# Occasionally, this may mean that a genuine user may be wrongly flagged as a bot. This can be for a number of potential reasons, including, but not limited to:

# You're using a VPN which we have had to block due to excessive bot traffic in the past
# You're using our website at super speed which manages to beat our rate limits
# You have a plug-in on your browser which could be interfering with how our website interacts with you as a user
# You're using an automated browser
# If you've been blocked during normal use, please send us your IP address (this website may help: http://www.whatismyip.com/), the website you're accessing (e.g. www.skyscanner.net) and the date/time this happened, via the Contact Us button below and we'll look into it as quickly as possible.
# """.strip(),
#     file_path="question_3.txt",
# )


# write_file(
#     question="Where is my booking confirmation?",
#     answer="""
# You should get a booking confirmation by email from the company you bought your travel from. This can sometimes go into your spam/junk mail folder, so it's always worth checking there.

# If you still can't find it, try getting in touch with the company you bought from to find out what's going on.

# To find out who you need to contact, check the company name next to the charge on your bank account.
# """.strip(),
#     file_path="question_4.txt",
# )


# write_file(
#     question="How do I change or cancel my booking?",
#     answer="""
# For all questions about changes, cancellations, and refunds - as well as all other questions about bookings - you'll need to contact the company you bought travel from. They'll have all the info about your booking and can advise you.

# You'll find 1000s of travel agencies, airlines, hotels and car rental companies that you can buy from through our site and app. When you buy from one of these travel partners, they will take your payment (you'll see their name on your bank or credit card statement), contact you to confirm your booking, and provide any help or support you might need.

# If you bought from one of these partners, you'll need to contact them as they have all the info about your booking. We unfortunately don't have any access to bookings you made with them.
# """.strip(),
#     file_path="question_5.txt",
# )


# write_file(
#     question="I booked the wrong dates / times",
#     answer="""
# If you have found that you have booked the wrong dates or times, please contact the airline or travel agent that you booked your flight with as they will be able to help you change your flights to the intended dates or times.

# The search box below can help you find the contact details for the travel provider you booked with.

# You can search flexible or specific dates on Skyscanner to find your preferred flight, and when you select a flight on Skyscanner you are transferred to the website where you will make and pay for your booking. Once you are redirected to the airline or travel agent website, you might be required to select dates again, depending on the website. In all cases, you will be shown the flight details of your selection and you are required before confirming payment to state that you have checked all details and agreed to the terms and conditions. We strongly recommend that you always check this information carefully, as travel information can be subject to change.
# """.strip(),
#     file_path="question_6.txt",
# )


# write_file(
#     question="I entered the wrong email address",
#     answer="""
# Please contact the airline or travel agent you booked with as Skyscanner does not have access to bookings made with airlines or travel agents.

# If you can't remember who you booked with, you can check your credit card statement for a company name.

# The search box below can help you find the contact details for the travel provider you booked with.
# """.strip(),
#     file_path="question_7.txt",
# )


# write_file(
#     question="Luggage",
#     answer="""
# Depending on the flight provider, the rules, conditions and prices for luggage (including sports equipment) do vary.
# It's always a good idea to check with the airline or travel agent directly (and you should be shown the options when you make your booking).
# """.strip(),
#     file_path="question_8.txt",
# )


# write_file(
#     question="Changes, cancellation and refunds",
#     answer="""
# For changes, cancellations or refunds, we recommend that you contact the travel provider (airline or travel agent) agent that you completed your booking with.

# As a travel search engine, Skyscanner doesn't take your booking or payment ourselves. Instead, we pass you through to your chosen airline or travel agent where you make your booking directly. We therefore don't have access or visibility to any of your booking information. Depending on the type of ticket you've booked, there may be different options for changes, cancellations and refunds, and the travel provider will be best placed to advise on these.
# """.strip(),
#     file_path="question_9.txt",
# )


# write_file(
#     question="Why does the price sometimes change when I am redirected to a flight provider?",
#     answer="""
# Flight prices and availability change constantly, so we make sure the data is updated regularly to reflect this. When you redirect to a travel provider's site, the price is updated again so you can be sure that you will always see the best price available from the airline or travel agent at time of booking.

# We make every effort to ensure the information you see on Skyscanner is accurate and up to date, but very occasionally there can be reasons why a price change has not updated accurately on the site. If you see a price difference between Skyscanner and a travel provider, please contact us with all the flight details (from, to, dates, departure times, airline and travel agent if applicable) and we will investigate further.
# """.strip(),
#     file_path="question_10.txt",
# )


# write_file(
#     question="Why is Skyscanner free?",
#     answer="""
# Does Skyscanner charge commission?

# Nope. Skyscanner is always free to search, and we never charge you any hidden fees.

# Want to know how do we do it?

# Well, we search through thousands of sites to find you the best deals for flights, hotels and car hire. That includes everything from fancy hotels to low cost airlines, so no matter what your budget is, we'll help you get there.

# See a price you like? We'll connect you to that airline or travel company so you can book with them directly. And for this referral, the airline or travel company pays us a small fee.

# And that's all there is to it!
# """.strip(),
#     file_path="question_11.txt",
# )


# write_file(
#     question="Are my details safe?",
#     answer="""
# We take your privacy and safety online very seriously. We'll never sell, share or pass on your IP details, cookies, personal info and location data to others unless it's required by law, or it's necessary for one of the reasons set out in our Privacy Policy.
# """.strip(),
#     file_path="question_12.txt",
# )


# ## Model


DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"


model_name_or_path = "TheBloke/Nous-Hermes-13B-GPTQ"
model_basename = "nous-hermes-13b-GPTQ-4bit-128g.no-act.order"

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

model = AutoGPTQForCausalLM.from_quantized(
    model_name_or_path,
    model_basename=model_basename,
    use_safetensors=True,
    trust_remote_code=True,
    device=DEVICE,
)

generation_config = GenerationConfig.from_pretrained(model_name_or_path)


question = (
    "Which programming language is more suitable for a beginner: Python or JavaScript?"
)
prompt = f"""
### Instruction: {question}
### Response:
""".strip()



input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(DEVICE)
with torch.inference_mode():
    output = model.generate(inputs=input_ids, temperature=0.7, max_new_tokens=512)


print(tokenizer.decode(output[0]))


generation_config


streamer = TextStreamer(
    tokenizer, skip_prompt=True, skip_special_tokens=True, use_multiprocessing=False
)


pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=2048,
    temperature=0,
    top_p=0.95,
    repetition_penalty=1.15,
    generation_config=generation_config,
    streamer=streamer,
    batch_size=1,
)


llm = HuggingFacePipeline(pipeline=pipe)


response = llm(prompt)


# ## Embed Documents


embeddings = HuggingFaceEmbeddings(
    model_name="embaas/sentence-transformers-multilingual-e5-base",
    model_kwargs={"device": DEVICE},
)


loader = DirectoryLoader("./skyscanner/", glob="**/*txt")
documents = loader.load()
len(documents)


text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)
texts = text_splitter.split_documents(documents)


texts[4]


db = Chroma.from_documents(texts, embeddings)


db.similarity_search("flight search")


# ## Conversational Chain


template = """
### Instruction: You're a travelling support agent that is talking to a customer. Use only the chat history and the following information
{context}
to answer in a helpful manner to the question. If you don't know the answer - say that you don't know.
Keep your replies short, compassionate and informative.
{chat_history}
### Input: {question}
### Response:
""".strip()


prompt = PromptTemplate(
    input_variables=["context", "question", "chat_history"], template=template
)


memory = ConversationBufferMemory(
    memory_key="chat_history",
    human_prefix="### Input",
    ai_prefix="### Response",
    output_key="answer",
    return_messages=True,
)


chain = ConversationalRetrievalChain.from_llm(
    llm,
    chain_type="stuff",
    retriever=db.as_retriever(),
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt},
    return_source_documents=True,
    verbose=True,
)


question = "How flight search works?"
answer = chain(question)


answer.keys()


answer["source_documents"]


question = "I bought flight tickets, but I can't find any confirmation. Where is it?"
response = chain(question)


# ## QA Chain with Memory


memory = ConversationBufferMemory(
    memory_key="chat_history",
    human_prefix="### Input",
    ai_prefix="### Response",
    input_key="question",
    output_key="output_text",
    return_messages=False,
)

chain = load_qa_chain(
    llm, chain_type="stuff", prompt=prompt, memory=memory, verbose=True
)


question = "How flight search works?"
docs = db.similarity_search(question)
answer = chain.run({"input_documents": docs, "question": question})


question = "I entered wrong email address during my flight booking. What should I do?"
docs = db.similarity_search(question)
answer = chain.run({"input_documents": docs, "question": question})


print(answer.strip())


# ## Support Chatbot


DEFAULT_TEMPLATE = """
### Instruction: You're a travelling support agent that is talking to a customer. Use only the chat history and the following information
{context}
to answer in a helpful manner to the question. If you don't know the answer - say that you don't know.
Keep your replies short, compassionate and informative.
{chat_history}
### Input: {question}
### Response:
""".strip()


class Chatbot:
    def __init__(
        self,
        text_pipeline: HuggingFacePipeline,
        embeddings: HuggingFaceEmbeddings,
        documents_dir: Path,
        prompt_template: str = DEFAULT_TEMPLATE,
        verbose: bool = False,
    ):
        prompt = PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template=prompt_template,
        )
        self.chain = self._create_chain(text_pipeline, prompt, verbose)
        self.db = self._embed_data(documents_dir, embeddings)

    def _create_chain(
        self,
        text_pipeline: HuggingFacePipeline,
        prompt: PromptTemplate,
        verbose: bool = False,
    ):
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            human_prefix="### Input",
            ai_prefix="### Response",
            input_key="question",
            output_key="output_text",
            return_messages=False,
        )

        return load_qa_chain(
            text_pipeline,
            chain_type="stuff",
            prompt=prompt,
            memory=memory,
            verbose=verbose,
        )

    def _embed_data(
        self, documents_dir: Path, embeddings: HuggingFaceEmbeddings
    ) -> Chroma:
        loader = DirectoryLoader(documents_dir, glob="**/*txt")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return Chroma.from_documents(texts, embeddings)

    def __call__(self, user_input: str) -> str:
        docs = self.db.similarity_search(user_input)
        return self.chain.run({"input_documents": docs, "question": user_input})


chatbot = Chatbot(llm, embeddings, "./skyscanner/")


import warnings

warnings.filterwarnings("ignore", category=UserWarning)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "goodbye"]:
        break
    answer = chatbot(user_input)
    print()

#
# ## References
# 
# - [Skyscanner help center](https://help.skyscanner.net/hc/en-us/categories/200385602-Traveling)
# - [Embeddings Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
# - [Local LLM Comparison](https://github.com/Troyanovsky/Local-LLM-comparison)
# - [Nous-Hermes-13B GPTQ](https://huggingface.co/TheBloke/Nous-Hermes-13B-GPTQ)
# - [Nous Hermes 13B (Original model)](https://huggingface.co/NousResearch/Nous-Hermes-13b)
# - [Text Embeddings Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
# - [OpenLLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)


