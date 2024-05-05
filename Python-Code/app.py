import os
import urllib
from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores.azure_cosmos_db import AzureCosmosDBVectorSearch, CosmosDBSimilarityType, CosmosDBVectorSearchType
import pymongo
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from pymongo.operations import IndexModel
from langchain_openai import AzureOpenAIEmbeddings
from models.product import Product


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

def create_mongodb_db_and_index():
    CONNECTION_STRING = "mongodb+srv://" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_USERNAME) + ":" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_PASSWORD) + "@toastmaster-db.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    INDEX_NAME = "sample_text"
    NAMESPACE = "toastmaster.pdfdata"
    DB_NAME, COLLECTION_NAME = NAMESPACE.split(".")
    client: MongoClient = MongoClient(CONNECTION_STRING)
    
    # Specify the database and collection
    db = client.toastmaster2
    collection = db.detailsTable
    
    # Create the products vector index
    db.command({
    'createIndexes': 'tmVectorIndex',
    'indexes': [
        {
        'name': 'VectorSearchIndex',
        'key': {
            "contentVector": "cosmosSearch"
        },
        'cosmosSearchOptions': {
            'kind': 'vector-ivf',
            'numLists': 1,
            'similarity': 'COS',
            'dimensions': 1536
        }
        }
    ]
    })

def InitializeEmbeddingsForPDFFile():
    loader = PyPDFLoader(file_path=DATA_PATH)
    pages = loader.load_and_split()
    
    embedding = AzureOpenAIEmbeddings(
        azure_endpoint=AZURE_OPEN_AI_ENDPOINT,
        api_key=AZURE_OPEN_AI_KEY,
        api_version=API_VERSION,
        model=AZURE_OPENAI_MODEL,
        chunk_size=1
    )   
    
    CONNECTION_STRING = "mongodb+srv://" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_USERNAME) + ":" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_PASSWORD) + "@toastmaster-db.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    INDEX_NAME = "VectorSearchIndex"
    NAMESPACE = "toastmaster2.tmVectorIndex"
    DB_NAME, COLLECTION_NAME = NAMESPACE.split(".")
    client: MongoClient = MongoClient(CONNECTION_STRING)
    collection = client[DB_NAME][COLLECTION_NAME]
    
    fruits = ["apple", "banana", "cherry"]
    bulk_operations = []
    counter =1
    for fruit in fruits:
        content_vector = generate_embeddings(fruit)    
        bulk_operations.append(pymongo.UpdateOne(
                    {"_id": counter},
                    {"$set": {"contentVector": content_vector}},
                    upsert=True
                ))
        counter+=1
    # execute bulk operations
    collection.bulk_write(bulk_operations)

def perform_vector_search(query):
    CONNECTION_STRING = "mongodb+srv://" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_USERNAME) + ":" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_PASSWORD) + "@toastmaster-db.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    INDEX_NAME = "sample_text"
    NAMESPACE = "toastmaster.pdfdata"
    DB_NAME, COLLECTION_NAME = NAMESPACE.split(".")
    client: MongoClient = MongoClient(CONNECTION_STRING)
    
    

if __name__ == "__main__":
    InitializeEmbeddingsForPDFFile()
    #print(embeddings)
