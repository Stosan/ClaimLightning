import logging
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from src.config.appconfig import env_config


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MongoDBClientConfig:
    def __init__(self):
        """Initialize MongoDB client with comprehensive connection logging."""
        try:
            logger.info("🔄 Initializing MongoDB connection...")
            
            # Construct the MongoDB URI using app configuration
            context_uri = env_config.mongo_conn_url
            logger.info(f"📍 Connecting to MongoDB URI: {self._mask_uri(context_uri)}")
            
            # Create a MongoDB client with TLS configuration
            logger.info("🔗 Creating MongoDB client...")
            self.context_client = MongoClient(context_uri, serverSelectionTimeoutMS=5000)
            
            db_info = self.context_client.server_info()
            logger.info(f"✅ Successfully connected to MongoDB!")
            
            # Connect to the database
            database_name = env_config.mongo_database_name
            logger.info(f"🗄️  Connecting to database: '{database_name}'")
            self.context_db = self.context_client[database_name]
            
            # Setup collection
            collection_name = 'aichatmemory'
            self.context_collection = None
            self._setup_collection(collection_name)
            
            logger.info("🎉 MongoDB initialization completed successfully!")
            
        except ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
            raise
        except ServerSelectionTimeoutError as e:
            logger.error(f"⏰ MongoDB connection timeout: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"💥 Unexpected error during MongoDB initialization: {str(e)}")
            raise

    def _setup_collection(self, collection_name):
        """Setup the collection with proper logging."""
        try:
            logger.info(f"📋 Checking if collection '{collection_name}' exists...")
            
            existing_collections = self.context_db.list_collection_names()
            logger.info(f"📚 Found {len(existing_collections)} existing collections in database")
            
            if collection_name not in existing_collections:
                logger.info(f"➕ Creating new collection: '{collection_name}'")
                self.context_db.create_collection(collection_name)
                logger.info(f"✅ Collection '{collection_name}' created successfully!")
            else:
                logger.info(f"✅ Collection '{collection_name}' already exists")
            
            # Connect to the collection
            logger.info(f"🔗 Connecting to collection: '{collection_name}'")
            self.context_collection = self.context_db[collection_name]
            
            # Verify collection access
            doc_count = self.context_collection.count_documents({})
            logger.info(f"📄 Collection '{collection_name}' contains {doc_count} documents")
            
        except Exception as e:
            logger.error(f"❌ Error setting up collection '{collection_name}': {str(e)}")
            raise

    def _mask_uri(self, uri):
        """Mask sensitive information in the URI for logging."""
        if '@' in uri:
            # Split at @ to separate credentials from host
            parts = uri.split('@')
            if len(parts) >= 2:
                # Keep protocol and mask credentials
                protocol_and_creds = parts[0]
                host_and_path = '@'.join(parts[1:])
                
                # Extract protocol
                if '://' in protocol_and_creds:
                    protocol = protocol_and_creds.split('://')[0]
                    return f"{protocol}://***:***@{host_and_path}"
        return uri.split('://')[0] + '://***' if '://' in uri else '***'


    def get_context_db(self)->Database:
        """Get the context database instance with logging."""
        logger.info("🔍 Retrieving context database instance...")

        logger.info("✅ Context database instance retrieved successfully")
        return self.context_db


    def get_context_collection(self)->Collection:
        """Get the context collection instance with logging."""
        logger.info("🔍 Retrieving context collection instance...")
        logger.info("✅ Context collection instance retrieved successfully")
        return self.context_collection

    def health_check(self):
        """Perform a health check on the MongoDB connection."""
        try:
            logger.info("🩺 Performing MongoDB health check...")
            
            # Test basic connectivity
            self.context_client.admin.command('ismaster')
            logger.info("✅ MongoDB connection is healthy")
            
            # Test database access
            collections = self.context_db.list_collection_names()
            logger.info(f"✅ Database access verified - {len(collections)} collections found")
            
            # Test collection access
            if hasattr(self, 'context_collection'):
                doc_count = self.context_collection.count_documents({})
                logger.info(f"✅ Collection access verified - {doc_count} documents")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Health check failed: {str(e)}")
            return False

    def close_connection(self):
        """Close the MongoDB connection with logging."""
        try:
            logger.info("🔒 Closing MongoDB connection...")
            if hasattr(self, 'context_client'):
                self.context_client.close()
                logger.info("✅ MongoDB connection closed successfully")
        except Exception as e:
            logger.error(f"❌ Error closing MongoDB connection: {str(e)}")

# Usage example:
if __name__ == "__main__":
    try:
        # Initialize the MongoDB client
        mongo_client = MongoDBClientConfig()
        
        # Perform health check
        mongo_client.health_check()
        
        # Your application logic here...
        
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
    finally:
        # Clean up
        if 'mongo_client' in locals():
            mongo_client.close_connection()
  