import pymongo
import os
from models import User

class MongoDB:
    def __init__(self, 
                 database_name="warmapp", 
                 time_series_collection_name="time-series",
                 user_collection_name = "users"):

        # Read the connection string from an environment variable
        user_name = os.getenv("USERNAME","david")
        password = os.getenv("PASSWORD","warmapp")
        connection_string = f"mongodb+srv://{user_name}:{password}@cluster0.kp7r8qd.mongodb.net/?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(connection_string)
        self.database = self.client[database_name]
        self.times_series_collection = self.database[time_series_collection_name]
        self.users_collection = self.database[user_collection_name]

    def insert(self, items):
        """
        Insert a dictionary of items into the MongoDB collection.
        """
        try:
            # Insert the data into the collection
            insert_result = self.times_series_collection.insert_one(items)

            # Print the inserted document's ID
            print(f"Inserted document ID: {insert_result.inserted_id}")

        except Exception as e:
            print(f"Error: {e}")
    def get_all_documents(self):
        try:
            return list(self.times_series_collection.find({}))
        except Exception as e:
            print(f"Error: {e}")

    def get_sensor_data_for_device(self,device_id:str):
        try:
            query = {"context.deviceMac": device_id}
            #Exclude '_id' from output
            projection = {'_id':0}
            result = self.times_series_collection.find(query,projection)
            return list(result)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def close_connection(self):
        """
        Close the MongoDB connection.
        """
        self.client.close()

if __name__ == '__main__':
    db = MongoDB()
    print(len(db.get_sensor_data_for_device("EAE31EA7C084")))