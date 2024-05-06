import os
import urllib
from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_community.document_loaders import PyPDFLoader
import pymongo
from pymongo import MongoClient
from langchain_openai import AzureOpenAIEmbeddings

#Load variables from .env file
load_dotenv()

#Initialize Azure OpenAI Service details
AZURE_OPEN_AI_KEY = os.getenv('AZURE_OPEN_AI_KEY')
AZURE_OPEN_AI_ENDPOINT = os.getenv('AZURE_OPEN_AI_ENDPOINT')
AZURE_COSMOSDB_MONGODB_USERNAME = os.getenv('AZURE_COSMOSDB_MONGODB_USERNAME')
AZURE_COSMOSDB_MONGODB_PASSWORD = os.getenv('AZURE_COSMOSDB_MONGODB_PASSWORD')

API_VERSION = "2024-02-01"
AZURE_OPENAI_MODEL = "text-embedding-ada-002"
DATA_PATH = 'Python-Code/data/Toastmasters-CC-Manual.pdf'

def generate_embeddings(text: str):
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPEN_AI_ENDPOINT,
        api_key=AZURE_OPEN_AI_KEY,
        api_version=API_VERSION
    )
    response = client.embeddings.create(input=text, model=AZURE_OPENAI_MODEL)
    embeddings = response.data[0].embedding
    return embeddings

def CreateAndSaveEmbeddingsForPDFFile():
    loader = PyPDFLoader(file_path=DATA_PATH)
    pages = loader.load_and_split()
    
    CONNECTION_STRING = "mongodb+srv://" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_USERNAME) + ":" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_PASSWORD) + "@toastmaster-db.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    INDEX_NAME = "VectorSearchIndex"
    DB_NAME = "Toastmaster4"
    COLLECTION_NAME = "DetailsTable"
    client: MongoClient = MongoClient(CONNECTION_STRING)
    collection = client[DB_NAME][COLLECTION_NAME]
    
    fruits = ["apple", "banana", "cherry"]
    bulk_operations = []
    counter =1
    for fruit in fruits:
        content_vector = generate_embeddings(fruit)    
        bulk_operations.append(pymongo.UpdateOne(
                    {"_id": counter},
                    {"$set": {"contentVector": content_vector, "record_text": fruit}},
                    upsert=True
                ))
        counter+=1
    # execute bulk operations
    collection.bulk_write(bulk_operations)

def perform_vector_search(query):
    CONNECTION_STRING = "mongodb+srv://" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_USERNAME) + ":" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_PASSWORD) + "@toastmaster-db.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    INDEX_NAME = "VectorSearchIndex"
    DB_NAME = "Toastmaster4"
    COLLECTION_NAME = "DetailsTable"
    client: MongoClient = MongoClient(CONNECTION_STRING)
    collection = client[DB_NAME][COLLECTION_NAME]
    query_embedding = generate_embeddings(query)    
    number_of_resilts=1
    pipeline = [
        {
            '$search': {
                "cosmosSearch": {
                    "vector": query_embedding,
                    "path": "contentVector",
                    "k": number_of_resilts
                },
                "returnStoredSource": True }},
        {'$project': { 'similarityScore': { '$meta': 'searchScore' }, 'document' : '$$ROOT' } }
    ]
    
    results = collection.aggregate(pipeline)
    return results

def print_product_search_result(result):
    print(f"Similarity Score: {result['similarityScore']}")  
    print(f"Name: {result['document']['record_text']}")   