import scrapy
class BookscrapeSpider(scrapy.Spider):
    name = "bookscrape"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            yield {
                'name': book.css('h3 a::text').get(),
                'price': book.css('.product_price .price_color::text').get(),
                'link': response.urljoin(book.css('h3 a').attrib['href'])  # Absolute URL
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)  # This properly joins relative URLs
            yield response.follow(url=next_page_url, callback=self.parse)
