from time import time
from urllib.parse import urljoin

import scrapy


class AptekaSpider(scrapy.Spider):
    name = "apteka"
    allowed_domains = ["apteka-ot-sklada.ru"]
#    start_urls = ["https://apteka-ot-sklada.ru/"]
    start_urls = ["https://apteka-ot-sklada.ru/catalog/kosmetika/bannye-serii/pena_-ekstrakty-dlya-vann/"]

    def parse(self, response):
        BASE_URL = 'https://apteka-ot-sklada.ru/'
        for good in response.css('div.goods-grid__inner div.ui-card'):
            original_price = good.css('div.goods-card__cost-area span::text').get()
            current_price = good.css('span.ui-link__text span::text').get()
            try:
                original_price = original_price.split()[0]
            except Exception:
                pass
            try:
                current_price = current_price.split()[1]
            except Exception:
                pass
            original_price = float(original_price or 0)
            current_price = float(current_price if current_price else original_price)
            if original_price and current_price and original_price != current_price:
                sale_tag = f'Скидка {int((1-current_price/original_price)*100)}%'
            else:
                sale_tag = 0
            url = urljoin(BASE_URL, good.css('a::attr(href)').get())
            current_good = dict(
                timestamp=int(time()),
                url=url,
                RPC=good.css('a::attr(href)').get().split('_')[-1],
                title=good.css('[itemprop="name"]::text').get(),
                brand=good.css('[itemtype="legalName"]::text').get(),
                price_data=dict(
                    current=current_price,
                    original=original_price,
                    sale_tag=sale_tag,
                ),
                stock=dict(
                    in_stock=True if (current_price or original_price) else False,
                    count=0,
                ),
                metadata={'СТРАНА ПРОИЗВОДИТЕЛЬ': good.css('[itemtype="location"]::text').get()},
                assets=dict(main_image=urljoin(BASE_URL, good.css('img::attr(src)').get())),
                variants=1,
            )
            yield current_good

        next_page = response.css('li.ui-pagination__item_next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
