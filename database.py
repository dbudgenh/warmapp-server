import pymongo
import os

class MongoDB:
    def __init__(self, database_name="warmapp", collection_name="time-series"):

        # Read the connection string from an environment variable
        user_name = os.getenv("USERNAME","david")
        password = os.getenv("PASSWORD","warmapp")
        connection_string = f"mongodb+srv://{user_name}:{password}@cluster0.kp7r8qd.mongodb.net/?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(connection_string)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    def insert(self, items):
        """
        Insert a dictionary of items into the MongoDB collection.
        """
        try:
            # Insert the data into the collection
            insert_result = self.collection.insert_one(items)

            # Print the inserted document's ID
            print(f"Inserted document ID: {insert_result.inserted_id}")

        except Exception as e:
            print(f"Error: {e}")
    def get_all_documents(self):
        try:
            documents = list(self.collection.find({}))
            print(f"Documents {documents}")
        except Exception as e:
            print(f"Error: {e}")


    def close_connection(self):
        """
        Close the MongoDB connection.
        """
        self.client.close()

if __name__ == '__main__':
    db = MongoDB()
    db.get_all_documents()