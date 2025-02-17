import scrapy


class BookdeepcrawlerSpider(scrapy.Spider):
    name = "bookdeepcrawler"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books=response.css("article.product_pod")
        for book in books:
            relative_url=response.css("h3 a::attr(href)").get()
            if relative_url:
                book_url=response.urljoin(relative_url)
            yield response.follow(book_url,callback=self.parse_book_page)
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page:
            next_page_url=response.urljoin(next_page)
        yield response.follow(book_url, callback=self.parse_book_page)
            
            
    def parse_book_page(self,response):
        table_rows=response.css('table tr')
        yield{
            "url":response.url,
            "title":response.css(".product_main h1::text").get(),
            'product type':table_rows[1].css("td ::text").get(),
            'price excl tax':table_rows[2].css("td ::text").get(),
            'price incl tax':table_rows[3].css("td ::text").get(),
            'tax':table_rows[4].css("td ::text").get(),
            'star':response.css("star-rating").attrib['class']
            
        }
        
            
            
