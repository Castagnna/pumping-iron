import scrapy
import json


class PumpSpider(scrapy.Spider):
    name = "pump_spider"
    allowed_domains = ["paciente.me"]

    def start_requests(self):
        urls = [
            "https://paciente.me/evolucao_antropometria.php?id=107721031806",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        xpath = '//script[contains(., "dados_antropometria")]//text()'
        pattern = r'dados_antropometria = (\[.+\]);'
        values = response.xpath(xpath).re(pattern)
        if values[0]:
            yield {"dados_antropometria": json.loads(values[0])}
        else:
            self.logger.warning("Value not found.")
    