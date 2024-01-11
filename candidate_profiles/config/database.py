from pymongo import MongoClient
from bson.codec_options import CodecOptions, DEFAULT_CODEC_OPTIONS
from bson.binary import Binary, UuidRepresentation
from settings import base as app_settings


client = MongoClient(app_settings.DATABASES["main"])
db = client.candidates_db

users_collection_name = db["user"]
candidate_collection_name = db["candidate"]

opts = CodecOptions(uuid_representation=UuidRepresentation.STANDARD)
users_collection = client.testdb.get_collection("user", codec_options=opts)
candidates_collection = client.testdb.get_collection("candidate", codec_options=opts)
