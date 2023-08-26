from urllib.parse import urljoin

import scrapy


class AptekaSpider(scrapy.Spider):
    name = "apteka"
    allowed_domains = ["apteka-ot-sklada.ru"]
#    start_urls = ["https://apteka-ot-sklada.ru/"]
    start_urls = ["https://apteka-ot-sklada.ru/catalog/sredstva-gigieny/uhod-za-polostyu-rta/zubnye-niti_-ershiki/"]

    def parse(self, response):
        BASE_URL = 'https://apteka-ot-sklada.ru/'
        for good in response.css('div.goods-grid__inner div.ui-card'):
            yield dict(
                url=urljoin(BASE_URL, good.css('a::attr(href)').get()),
                RPC=good.css('a::attr(href)').get().split('_')[-1],
                title=good.css('[itemprop="name"]::text').get(),
                brand=good.css('[itemtype="legalName"]::text').get(),
                price_data=float(good.css('[itemprop="price"]::attr(content)').get() or 0),
#                in_stock=True if good_price else False,
                main_image=urljoin(BASE_URL, good.css('img::attr(src)').get()),
            )
