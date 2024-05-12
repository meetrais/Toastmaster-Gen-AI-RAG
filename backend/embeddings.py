import os
import urllib
from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_community.document_loaders import PyPDFLoader
import pymongo
from pymongo import MongoClient
import json

#Load variables from .env file
load_dotenv()

#Initialize Azure OpenAI Service details
AZURE_OPEN_AI_KEY = os.getenv('AZURE_OPEN_AI_KEY')
AZURE_OPEN_AI_ENDPOINT = os.getenv('AZURE_OPEN_AI_ENDPOINT')
AZURE_COSMOSDB_MONGODB_USERNAME = os.getenv('AZURE_COSMOSDB_MONGODB_USERNAME')
AZURE_COSMOSDB_MONGODB_PASSWORD = os.getenv('AZURE_COSMOSDB_MONGODB_PASSWORD')
AZURE_COSMOSDB_MONGODB_CLUSTER = os.getenv('AZURE_COSMOSDB_MONGODB_CLUSTER')
API_VERSION = "2024-02-01"
AZURE_OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
AZURE_OPENAI_CHAT_MODEL = "gpt-35-turbo"
DATA_PATH = 'Python-Code/data/Toastmasters-CC-Manual.pdf'

#This function creates and returns embedding for the text
def generate_embeddings(text: str):
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPEN_AI_ENDPOINT,
        api_key=AZURE_OPEN_AI_KEY,
        api_version=API_VERSION
    )
    response = client.embeddings.create(input=text, model=AZURE_OPENAI_EMBEDDING_MODEL)
    embeddings = response.data[0].embedding
    return embeddings

#This function splits/chunks PDF file into pages, then creates embeddings and saves into MongoDB. 
def CreateAndSaveEmbeddingsForPDFFile():
    print("Creating and saving embeddings for PDF file. This may take few minutes.")
    loader = PyPDFLoader(file_path=DATA_PATH)
    pages = loader.load_and_split()
    
    CONNECTION_STRING = "mongodb+srv://" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_USERNAME) + ":" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_PASSWORD) + "@" + AZURE_COSMOSDB_MONGODB_CLUSTER
    INDEX_NAME = "VectorSearchIndex"
    DB_NAME = "Toastmaster5"
    COLLECTION_NAME = "DetailsTable"
    client: MongoClient = MongoClient(CONNECTION_STRING)
    collection = client[DB_NAME][COLLECTION_NAME]
    
    bulk_operations = []
    counter =1
    #Looping through PDF pages, create embeddings and save into Vector-Index alongwith id and page text.
    for page in pages:
        page_text = page.page_content
        content_vector = generate_embeddings(page_text)    
        bulk_operations.append(pymongo.UpdateOne(
                    {"_id": counter},
                    {"$set": {"contentVector": content_vector, "record_text": page_text}},
                    upsert=True
                ))
        counter+=1
    # execute bulk operations
    collection.bulk_write(bulk_operations)
    print("Embeddings for PDF file saved in MongoDB.")

#This function performs vector search on MongoDB vector-index for the user query. Then returns vector-search result.
def perform_vector_search(query, top_k):
    CONNECTION_STRING = "mongodb+srv://" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_USERNAME) + ":" + urllib.parse.quote(AZURE_COSMOSDB_MONGODB_PASSWORD) + "@" + AZURE_COSMOSDB_MONGODB_CLUSTER    
    INDEX_NAME = "VectorSearchIndex"
    DB_NAME = "Toastmaster5"
    COLLECTION_NAME = "DetailsTable"
    client: MongoClient = MongoClient(CONNECTION_STRING)
    collection = client[DB_NAME][COLLECTION_NAME]
    query_embedding = generate_embeddings(query)    
    number_of_results=top_k
    pipeline = [
        {
            '$search': {
                "cosmosSearch": {
                    "vector": query_embedding,
                    "path": "contentVector",
                    "k": number_of_results
                },
                "returnStoredSource": True }},
        {'$project': { 'similarityScore': { '$meta': 'searchScore' }, 'document' : '$$ROOT' } }
    ]
    
    results = collection.aggregate(pipeline)
    return results

#This function performs first vector-search and then RAG search by using OpenAI model defined for chat-completion.
def perform_rag_vector_search(user_text, temprature, top_k, max_tokens, top_p):
    system_prompt = """
        You atr a helpful assistant. Answer only if you know the answer otherwise say - Sorry I dont know about this.
    """
    
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPEN_AI_ENDPOINT,
        api_key=AZURE_OPEN_AI_KEY,
        api_version=API_VERSION
    )
    results = perform_vector_search(user_text, top_k)
    record_list=""
    
    for result in results:
        if "contentVector" in result["document"]:
            del result["document"]["contentVector"]
        record_list += json.dumps(result["document"], indent=4, default=str) + "\n\n"
        
    prompt = system_prompt + record_list
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_text}
    ]
    
    completion = client.chat.completions.create(
        messages=messages,
        model=AZURE_OPENAI_CHAT_MODEL, 
        temperature=temprature,
        max_tokens=max_tokens,
        top_p=top_p
        )
    
    return completion.choices[0].message.content