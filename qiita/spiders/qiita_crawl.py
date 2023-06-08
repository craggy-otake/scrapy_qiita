import scrapy
import json
import w3lib.html

class QiitaCrawlSpider(scrapy.Spider):
    name = "qiita_crawl"
    allowed_domains = ["qiita.com"]
    start_urls = ['https://qiita.com/ueta7/items/d0a4f108c7072f29e9e3']


    def parse(self, response):
        texts = response.xpath('//*[@id="personal-public-article-body"]/div/p')
        
        for text in texts:
            items = {}
            items['url'] = response.url
            items['text'] = w3lib.html.remove_tags(text.extract())
            with open('output.jsonl', 'a', encoding='utf-8') as writer:
                json.dump(items,writer)
                writer.write('\n')

        next_pages = response.xpath('//*[contains(@href,"qiita.com")]/@href')

        for next_page in next_pages:
            yield response.follow(url=next_page, callback=self.parse)
