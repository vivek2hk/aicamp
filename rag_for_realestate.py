import pymongo
import pymongo
from openai import OpenAI
from dotenv import load_dotenv
import os
import certifi
config = load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

openaiClient = OpenAI()

def get_context(query):

  # Set your OpenAI API key

  mongoClient = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())

  db = mongoClient.sample_housing
  collection = db.data2

  def generate_embedding(text: str) -> list[float]:

      return openaiClient.embeddings.create(model="text-embedding-3-small",input=text).data[0].embedding
    

  #To create embeddings for all documents in the collection
  # for doc in collection.find({'consolidated_text':{"$exists": True}}):
  #   doc['text_embedding'] = generate_embedding(doc['consolidated_text'])
  #   collection.replace_one({'_id': doc['_id']}, doc)



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

  formatted_results = []

  for document in results:
        # formatted_results += f'House Location: {document["state"]},\nSummary: {document["consolidated_text"]}\n'
        formatted_document = {
          "state": document["state"],
          "consolidated_text": document["consolidated_text"],
          "exterior_image": document["exterior_image"],
          "interior_image": document["interior_image"],
          "price": document["price"],
          "bed": document["bed"],
          "bath": document["bath"],
          "acre_lot": document["acre_lot"],
          "neighborhood_safety": document["neighborhood_safety"],
          "elementary_school_rating": document["elementary_school_rating"],
          "middle_school_rating": document["middle_school_rating"],
          "high_school_rating": document["high_school_rating"],

        }

        formatted_results.append(formatted_document)

  return formatted_results