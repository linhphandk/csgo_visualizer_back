"""
Module containing mongo client service
"""
import os
from typing import Type

from pymongo import MongoClient
class MongoService():
    """
    Pymongo service
    """
    host = "localhost" if not os.environ.get("MONGO_HOST") else os.environ.get("MONGO_HOST")
    port = 27017
    username = "root"
    password = "example"
    def __init__(self, client: Type[MongoClient], database):
        self.database = database
        # pylint: disable=line-too-long
        self.client = client("mongodb://"+self.username+":"+self.password+"@"+self.host+":"+str(self.port)+"/")

    def insert_many(self, records, collection):
        """
        bridge method
        """
        self.client[self.database][collection].insert_many(records)

    def insert(self, records, collection):
        """
        bridge method
        """
        self.client[self.database][collection].insert_one(records)


    def list_collection_names(self):
        """
        bridge method
        """
        return self.client[self.database].list_collection_names()

    def find_one(self, collection):
        """
        bridge method
        """
        return self.client[self.database][collection].find_one()

    def find(self, collection):
        """
        bridge method
        """
        return self.client[self.database][collection].find()

    def server_info(self):
        """
        bridge method
        """
        return self.client.server_info()

client_instance = MongoService(MongoClient,"csgo")

def get_client():
    """
    return an instance of pymongo
    """
    return client_instance

if __name__ == "__main__":
    mongo_client = get_client()
