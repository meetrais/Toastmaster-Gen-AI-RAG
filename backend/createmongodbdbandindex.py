import os
import urllib
from dotenv import load_dotenv
from pymongo import MongoClient

#This function creates dtabase, collection and index in MongoDB VCore cluster
def create_mongodb_db_and_index():
    
    #Load variables from .env file
    load_dotenv()

    #Initialize Azure OpenAI Service details
    AZURE_OPEN_AI_KEY = os.getenv('AZURE_OPEN_AI_KEY')
    AZURE_OPEN_AI_ENDPOINT = os.getenv('AZURE_OPEN_AI_ENDPOINT')
    AZURE_COSMOSDB_MONGODB_USERNAME = os.getenv('AZURE_COSMOSDB_MONGODB_USERNAME')
    AZURE_COSMOSDB_MONGODB_PASSWORD = os.getenv('AZURE_COSMOSDB_MONGODB_PASSWORD')
    AZURE_COSMOSDB_MONGODB_CLUSTER = os.getenv('AZURE_COSMOSDB_MONGODB_CLUSTER')
    
    #Initialize Azure MongoDB VCore connection
    CONNECTION_STRING = "mongodb+srv://" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_USERNAME) + ":" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_PASSWORD) + "@" + AZURE_COSMOSDB_MONGODB_CLUSTER
    client: MongoClient = MongoClient(CONNECTION_STRING)
    
    # Specify the name of database and collection
    db = client.Toastmaster5
    collection = db.DetailsTable
    
    # Create the vector index
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
    
    print("Database Created.")
    
if __name__ == "__main__": 
    create_mongodb_db_and_index()