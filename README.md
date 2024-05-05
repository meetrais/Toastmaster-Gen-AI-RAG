# Toastmaster-Gen-AI
Gen-AI specialized chatbot designed to answer fundamental questions about Toastmaster program.


from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from pymongo.operations import IndexModel
# Connect to MongoDB vCore database
client = MongoClient("<mongodb-uri>")
# Specify the database and collection
db = client.get_database("<database-name>")
collection = db.get_collection("<collection-name>")
# Create the collection if it doesn't exist
try:
    db.create_collection("<collection-name>")
except CollectionInvalid:
    print("Collection already exists")
# Create the search index if it doesn't exist
if len(list(collection.list_indexes())) == 1:
    print("Creating search index...")
    index_model = IndexModel([("embedding", "2dsphere")])
    collection.create_indexes([index_model])
    print("Search index created")
else:
    print("Search index already exists")