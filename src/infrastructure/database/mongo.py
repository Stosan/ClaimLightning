from pymongo import MongoClient
from src.config.appconfig import env_config


class MongoDBClientConfig():
    def __init__(self):
        # Construct the MongoDB URI using app configuration
        context_uri = f"mongodb://{env_config.mongo_user}:{env_config.mongo_password}@{env_config.mongo_host}:{env_config.mongo_port}/mongo_staging?serverSelectionTimeoutMS=2000&authSource=mongo_staging&directConnection=true"
        
        # Create a MongoDB client with TLS configuration
        self.context_client = MongoClient(context_uri)
        
        # Get database information
        db_info = self.context_client.server_info()

        # Connect to the 'context_memory' database
        self.context_db = self.context_client[env_config.database_name]

        collection_name = 'aichatmemory'

        if collection_name not in self.context_db.list_collection_names():
            # Create the collection
            self.context_db.create_collection(collection_name)

        # Connect to the 'cliveai_chat_memory' collection
        self.context_collection = self.context_db[collection_name]

    @classmethod
    def get_context_db(cls):
        return cls().context_db

    @classmethod
    def get_context_collection(cls):
        return cls().context_collection
  