import scrapy

class DisruptSpider(scrapy.Spider):
    name = 'disrupt'
    allowed_domains = ['techcrunch.com']
    start_urls = ['https://techcrunch.com/tag/techcrunch-disrupt-2025/']

    def parse(self, response):
        
        article_links = response.css('a.loop-card__title-link::attr(href)').getall()
        self.log(f"Found {len(article_links)} articles.")

        for link in article_links:
            yield response.follow(link, self.parse_article)

        
        next_page = response.css('a.load-more::attr(href)').get()
        if next_page:
            self.log(f"Following next page: {next_page}")
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        author = response.css('a[rel="author"]::text').get()
        date = response.css('time::attr(datetime)').get()
        paragraphs = response.css('div.article-content p::text').getall()
        content = ' '.join(paragraphs)

        yield {
            'title': title,
            'author': author,
            'date': date,
            'url': response.url,
            'content': content
        }
