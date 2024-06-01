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




# create a retrieval QA chain 

