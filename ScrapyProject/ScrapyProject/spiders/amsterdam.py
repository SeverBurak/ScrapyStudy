import scrapy


class AmsterdamSpider(scrapy.Spider):
    name = 'amsterdam'
    allowed_domains = ['domain']
    start_urls = ['domain.com']

    custom_settings = {
        'FEED_URI' : 'Amsterdam_Results.json',
        'FEED_FORMAT': 'json'
    }

    def parse(self, response):
        ads = response.xpath("//div[@class = 'search-content-output']/ol/li")
        for ad in ads:
            title = ad.xpath(".//h2[@class='search-result__header-title fd-m-none']/text()").get().strip()
            adress = ad.xpath(".//h4[@class='search-result__header-subtitle fd-m-none']/text()").get().strip()
            living_area = ad.xpath(".//span[@title= 'Living area']/text()").get()
            rooms = ad.xpath(".//li[contains(text(), 'room')]/text()").get()
            status = ad.xpath(".//li[contains(text(), 'Available')]/text()").get()
            price = ad.xpath(".//div[@class = 'search-result-info search-result-info-price']/span[contains(text(), 'p/m')]/text()").get()
            yield{
                'Title' : title,
                'Adress' : adress,
                'Living Area' : living_area,
                'Rooms' : rooms,
                'Status' : status,
                'Price': price
            }

        next_page = response.xpath("//a[@rel = 'next']/@href").get()
        if next_page:
            full_link = response.urljoin(next_page)
            yield scrapy.Request(url=full_link, callback = self.parse)