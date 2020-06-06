import logging

from mongoengine import connect
from mongoengine.connection import MongoClient

from app.core.config import settings


class DataBase:
    client: MongoClient = None

    def connect_to_mongo(self):
        logging.info("connect mongodb...")
        self.client = connect(
            db=settings.MONGO_DB,
            username=settings.MONGO_INITDB_ROOT_USERNAME,
            password=settings.MONGO_INITDB_ROOT_PASSWORD,
            host=settings.MONGO_SERVER,
            authentication_source="admin",
        )
        logging.info("connect mongodb success！")

    def close_mongo_connection(self):
        logging.info("disconnect mongodb...")
        self.client.close()
        logging.info("disconnection mongodb success！")


db = DataBase()


async def get_database() -> MongoClient:
    return db.client
