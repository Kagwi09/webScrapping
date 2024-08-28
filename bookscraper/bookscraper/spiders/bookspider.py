import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"  # name of spider
    allowed_domains = ["books.toscrape.com"]  # allowed domains list
    start_urls = ["https://books.toscrape.com"]   #  first url spider starts scraping

    def parse(self, response, **kwargs):
        books = response.css('article.product_pod')
        for book in books:
            yield {
                'book_title': book.css('h3 a::text').get(),
                'book_price': book.css('div.product_price .price_color::text').get(),
                'book_url': book.css('h3 a').attrib['href'],
            }
        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url,callback=self.parse)


