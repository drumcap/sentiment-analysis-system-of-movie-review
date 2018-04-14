# -*- coding: utf-8 -*-
__author__ = 'drumcap'

import scrapy

from movie_scrap.items import MovieScrapItem

from datetime import datetime
import re
import random
import time

extract_nums = lambda s: re.search('\d+', s).group(0)
sanitize_str = lambda s: s.strip()

NAVER_BASEURL     = 'http://movie.naver.com/movie/point/af/list.nhn'
NAVER_RATINGURL   = NAVER_BASEURL + '?&page=%s'
NAVER_MOVIEURL    = NAVER_BASEURL + '?st=mcode&target=after&sword=%s&page=%s'

class MovieCommentSpider(scrapy.Spider):
    name = "movie"

    def extract_nums(self, s): return re.search('\d+', s).group(0)

    def start_requests(self):
        yield scrapy.Request(NAVER_RATINGURL % 1, self.parse_naver)

    def parse_naver(self, response):
        dtnow = datetime.now()
        for sel in response.css('#old_content > table > tbody > tr'):
            item = MovieScrapItem()
            item['source'] = 'naver'
            item['review_id'] = sel.xpath('./td[@class="ac num"]/text()').extract_first()
            item['rating'] = sel.xpath('./td[@class="point"]/text()').extract_first()
            item['movie_id'] = extract_nums(sel.xpath('./td[@class="title"]/a/@href').extract_first())
            item['movie_name'] = sel.xpath('./td[@class="title"]/a/text()').extract_first()
            item['review_txt'] = ' '.join(sel.xpath('./td[@class="title"]/text()').extract()).strip()
            item['author'] = sel.xpath('./td[@class="num"]/a/text()').extract_first()
            item['date'] = datetime.strptime(sel.xpath('./td[@class="num"]/text()').extract_first(),'%y.%m.%d').isoformat()
            yield item

        next_page = response.css('.paging .pg_next::attr(href)').extract_first()
        next_page_num = int(extract_nums(next_page))
        if next_page is not None and next_page_num < 1000:
            sleep_time = int(random.randrange(3, 7))
            time.sleep(sleep_time)
            print("go next page {}".format(next_page_num))
            yield response.follow(next_page, callback=self.parse_naver)