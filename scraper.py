import scrapy

class OportunidadesSpider(scrapy.Spider):
    name = "oportunidades"
    start_urls = [
        "https://seusite.com"
    ]

    def parse(self, response):
        text = response.text  # Usa o `response.text` para garantir que Scrapy lida com encoding interno
          
        for oportunidade in response.xpath("//div"):
            yield {
                "titulo": oportunidade.xpath(".//h2/text()").get(default="Título não encontrado"),
                "link": oportunidade.xpath(".//a/@href").get(default="Link não disponível"),
                "data_limite": oportunidade.xpath(".//span[@class='data']/text()").get(default="Data não especificada"),
                "categoria": oportunidade.xpath(".//span[@class='categoria']/text()").get(default="Categoria não identificada"),
            }
