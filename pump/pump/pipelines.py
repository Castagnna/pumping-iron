# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class PumpPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    def __init__(self, uri, database, collection):
        self.uri = uri
        self.database = database
        self.collection = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('MONGODB_URI'),
            database=crawler.settings.get('MONGODB_DATABASE'),
            collection=crawler.settings.get('MONGODB_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.database]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection].insert_one(dict(item))
        return item
