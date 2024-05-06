import os
import urllib
from dotenv import load_dotenv
from pymongo import MongoClient

def create_mongodb_db_and_index():
    
    #Load variables from .env file
    load_dotenv()

    #Initialize Azure OpenAI Service details
    AZURE_OPEN_AI_KEY = os.getenv('AZURE_OPEN_AI_KEY')
    AZURE_OPEN_AI_ENDPOINT = os.getenv('AZURE_OPEN_AI_ENDPOINT')
    AZURE_COSMOSDB_MONGODB_USERNAME = os.getenv('AZURE_COSMOSDB_MONGODB_USERNAME')
    AZURE_COSMOSDB_MONGODB_PASSWORD = os.getenv('AZURE_COSMOSDB_MONGODB_PASSWORD')
    
    CONNECTION_STRING = "mongodb+srv://" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_USERNAME) + ":" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_PASSWORD) + "@toastmaster-db.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    client: MongoClient = MongoClient(CONNECTION_STRING)
    
    # Specify the database and collection
    db = client.Toastmaster4
    collection = db.DetailsTable
    
    # Create the products vector index
    db.command({
    'createIndexes': 'DetailsTable',
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
