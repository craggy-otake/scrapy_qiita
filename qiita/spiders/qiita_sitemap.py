import scrapy
from datetime import datetime

from scrapy.spiders.sitemap import SitemapSpider
import json
import w3lib.html

# conslut with https://orangain.hatenablog.com/entry/scrapy
class QiitaCrawlSpider(SitemapSpider):
    name = "qiita_sitemap"
    allowed_domains = ["qiita.com"]
    start_urls = ["https://qiita.com/"]

    sitemap_urls = []
    for i in range(1,21):
        sitemap_urls.append('https://cdn.qiita.com/sitemap-https/sitemap{}.xml.gz'.format(str(i)))
    
    print('sitemap_urls',sitemap_urls)
    sitemap_rules = [
        # 正規表現 '/items/' にマッチするページをparseメソッドでパースする
        (r'/items/', 'parse'),
    ]


    def parse(self, response):
        texts = response.xpath('//*[@id="personal-public-article-body"]/div/p')
        
        for text in texts:
            items = {}
            items['url'] = response.url
            items['text'] = w3lib.html.remove_tags(text.extract())
            with open('output_from_sitemap.jsonl', 'a', encoding='utf-8') as writer:
                json.dump(items, writer, ensure_ascii=False)
                writer.write('\n')

        # next_pages = response.xpath('//*[contains(@href,"qiita.com")]/@href')

        # for next_page in next_pages:
        #     yield response.follow(url=next_page, callback=self.parse)


