import pymongo
from openai import OpenAI
from dotenv import load_dotenv
import os
config = load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

openaiClient = OpenAI()
import certifi

# Set your OpenAI API key

mongoClient = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())

db = mongoClient.sample_airbnb
collection = db.listingsAndReviews


def generate_embedding(text: str) -> list[float]:

    return openaiClient.embeddings.create(model="text-embedding-3-small",input=text).data[0].embedding
   
# To create embeddings for all documents in the collection, here the limit is set to 50
# for doc in collection.find({'summary':{"$exists": True}}).limit(50):
#   doc['summary_embedding_openai'] = generate_embedding(doc['summary'])
#   collection.replace_one({'_id': doc['_id']}, doc)


query = "I am looking for a place to stay in near a National Park. I would like to go hiking and see the wildlife."
results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "summary_embedding_openai",
    "numCandidates": 100,
    "limit": 4,
    "index": "vector_index",
      }}
]);

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')