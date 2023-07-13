import scrapy
import json


class PumpSpider(scrapy.Spider):
    name = "pump_spider"
    allowed_domains = ["paciente.me"]

    def start_requests(self):
        user_id = "107721031806"
        url = f"https://paciente.me/evolucao_antropometria.php?id={user_id}"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        user_id = "107721031806"
        xpath = '//script[contains(., "dados_antropometria")]//text()'
        pattern = r'dados_antropometria = (\[.+\]);'
        values = response.xpath(xpath).re(pattern)
        measurements = json.loads(values[0])
        if measurements:
            for measurement in measurements:
                measurement["user_id"] = user_id
                yield measurement
        else:
            self.logger.warning("Value not found.")
    