from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

config = load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") or ""

DB_NAME = "sample_housing"
COLLECTION_NAME = "data"


vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    MONGO_URI,
    DB_NAME + "." + COLLECTION_NAME,
    OpenAIEmbeddings(disallowed_special=()),
    index_name="vector_index",
)



prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

qa_retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 25},
)

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=qa_retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
)

docs = qa({"query": "gpt-4 compute requirements"})

print(docs["result"])
print(docs["source_documents"])