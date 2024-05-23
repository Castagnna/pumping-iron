# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class PumpPipeline:
    def __init__(self):
        self.floats = [
            "massa",
            "dobra_triceptal",
            "dobra_subescapular",
            "dobra_toraxica",
            "dobra_axilar",
            "dobra_suprailiaca",
            "dobra_abdominal",
            "dobra_coxa",
            "c_torax",
            "c_ombro",
            "c_cintura",
            "c_abdomen",
            "c_quadril",
            "c_bracorelaxado",
            "c_bracocontraido",
            "c_antebraco",
            "c_coxamedial",
            "c_panturrilha",
            "massaLivre",
            "imc",
            "mlg",
            "gc",
            "peso_g",
            "peso_r",
            "somatorio",
            "razao",
        ]

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        date = adapter.get("dataOrdem")
        if date:
            # Perform data type conversions
            adapter["dataOrdem"] = datetime.strptime(date, "%Y%m%d")
            adapter["estatura"] = int(item.get("estatura", 0))
            for f in self.floats:
                adapter[f] = float(item.get(f, 0.0))
            return item
        else:
            raise DropItem(f"Missing dataOrdem in {item}")


class MongoDBPipeline:
    def __init__(self, uri, database, collection):
        self.uri = uri
        self.database = database
        self.collection = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get("MONGODB_URI"),
            database=crawler.settings.get("MONGODB_DATABASE"),
            collection=crawler.settings.get("MONGODB_COLLECTION"),
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.database]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.db[self.collection].insert_one(dict(item))
            print(f"\tNew row inserted from date {item['dataAvaliacao']}")
        except DuplicateKeyError:
            print(f"\tWarning date {item['dataAvaliacao']} already inserted")
