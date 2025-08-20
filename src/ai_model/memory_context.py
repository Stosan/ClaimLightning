import pymongo
import datetime as dt
from datetime import datetime as dtt


def create_memory(collection, policy_number: str, prompt: str, ai_message: str):
    """
    This function creates a new memory entry in a MongoDB collection for a specified user.

    Args:
        collection: The MongoDB collection to insert the memory into.
        policy_number (str): The user ID to associate with the memory.
        prompt (str): The user's prompt.
        ai_message (str): The AI's response message.

    The function trims off a specified string from the ai_message before storing it.
    """
    try:
        data = {"user_prompt": prompt, "ai_response": ai_message}
        history = {
            "policy_number": policy_number,
            "History": {"type": "ai", "data": data},
            "timestamp":dtt.utcnow().isoformat()
        }

        # Insert the data into the collection
        collection.insert_one(history)
    except Exception as e:
        print(
                "Error occurred while creating memory: %s", str(e), exc_info=1
            )
 

def retrieve_memory_with_k(collection, policy_number: str, k: int = 3):
    """
    This function retrieves the most recent entries from a MongoDB collection where the policy_number matches the provided policy_number.
    It only returns entries if they were created within the last 1 minute. If no matching entries are found, or if the most recent
    matching entries are older than 1 minute, the function returns None.

    Args:
        collection: The MongoDB collection to retrieve the memory from.
        policy_number (str): The user ID to match.
        k (int): The number of memory messages to pull

    Returns:
        list: The most recent matching entries in the collection, or None if no match is found or if the entries are older than 1 minute.
    """
    # Query the collection for entries where the policy_number matches and the timestamp is within the last 15 minute
    min_time = dtt.utcnow() - dt.timedelta(minutes=15)
    query = {"policy_number": policy_number, "timestamp": {"$gte": min_time.isoformat()}}
    # Define the fields to return
    projection = {"History": 1}

    try:
        # Sort the results in descending order by timestamp and retrieve the first k results
        result_ = collection.find(query,projection).sort([('timestamp', pymongo.DESCENDING)]).limit(k)
        chat_history = []
        result = list(result_)
        # Check if the query returned a result
        if result != []:
            for r in reversed(result):
                chat_history.append(r['History']['data']['user_prompt'])
                chat_history.append(r['History']['data']['ai_response'])
            return chat_history
        else:
            # Return None if no match is found
            return None
    except pymongo.errors.PyMongoError as e:
        print(
                "Error occurred while retrieving memory: %s", str(e), exc_info=1
            )
        

