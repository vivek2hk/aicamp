import pymongo
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.llms import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os
config = load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

openaiClient = OpenAI()
import certifi

# set up a MongoDB Atlas vector store
mongoClient = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())
dbName= "rag_climate_demo"
collectionName = "climate_data"
collection= mongoClient[dbName][collectionName]

loader = DirectoryLoader('./data_files',glob='*.txt',show_progress=True)
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(data)


vector_store = MongoDBAtlasVectorSearch.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(disallowed_special=()),
    collection=collection,
    index_name="climate_search_index",
    )

# create a retrieval QA chain 
def query_data(query):
    docs=vector_store.similarity_search(query, K=1)
    as_output = docs[0].page_content

    retriever= vector_store.as_retriever()
    qa= RetrievalQA.from_chain_type(openaiClient,chain_type="stuff", retriever=retriever)
    retriever_output = qa.run(query)
    print(retriever_output)
    return as_output, retriever_output

print(query_data("how has climate change affected tornadoes in Midwest?"))