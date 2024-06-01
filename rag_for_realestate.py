import pymongo
import pymongo
from openai import OpenAI
from dotenv import load_dotenv
import os
import certifi
config = load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

openaiClient = OpenAI()


# Set your OpenAI API key

mongoClient = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())

db = mongoClient.sample_housing
collection = db.data

def generate_embedding(text: str) -> list[float]:

    return openaiClient.embeddings.create(model="text-embedding-3-small",input=text).data[0].embedding
   

#To create embeddings for all documents in the collection
# for doc in collection.find({'consolidated_text':{"$exists": True}}):
#   doc['text_embedding'] = generate_embedding(doc['consolidated_text'])
#   collection.replace_one({'_id': doc['_id']}, doc)


query="get me houses in Puerto Rico"

# # create a vector store

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "text_embedding",
    "numCandidates": 100,
    "limit": 4,
    "index": "vector_index",
      }}
])
print("Results: ")
for document in results:
    print(f'House Location: {document["state"]},\nSummary: {document["consolidated_text"]}\n')

# create a retrieval QA chain 
# def query_data(query):
#     #docs=vector_store.similarity_search(query, K=1)
#     qa= RetrievalQA.from_chain_type(openaiClient,chain_type="stuff", retriever=results)
#     retriever_output = qa.run(query)
#     return retriever_output

#print(query_data("how has climkate change affected tornadoes in Midwest?"))