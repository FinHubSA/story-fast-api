
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv # tells python to look for a .env file in the base folder
import os

load_dotenv()
# load in uri from env file
uri=os.getenv("DATABASE_URL")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["events_db"]
collection_user=db["user_collection"]
collection_events=db["events_collection"]
collection_attendance=db["attendance_collection"]

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)