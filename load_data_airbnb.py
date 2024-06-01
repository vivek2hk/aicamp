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

db = mongoClient.sample_airbnb
collection = db.listingsAndReviews


def generate_embedding(text: str) -> list[float]:

    return openaiClient.embeddings.create(model="text-embedding-3-small",input=text).data[0].embedding
   
#To create embeddings for all documents in the collection
# for doc in collection.find({'summary':{"$exists": True}}):
#   doc['summary_embedding_oi'] = generate_embedding(doc['summary'])
#   collection.replace_one({'_id': doc['_id']}, doc)


query = "I am looking for a place to stay in near a National Park. I would like to go hiking and see the wildlife."
results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "summary_embedding_oi",
    "numCandidates": 100,
    "limit": 4,
    "index": "airbnb_search_index",
      }}
]);

for document in results:
    print(f'Airbnb Name: {document["name"]},\nLocation Summary: {document["summary"]}\n')