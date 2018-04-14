# -*- coding: utf-8 -*-
import re
from datetime import date, timedelta

import scrapy

########################################################################
# Constants
########################################################################
# URL_TMPL = 'http://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=000&date={date}'  # noqa
URL_TMPL = 'http://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&date={date}'  # noqa

LINK_CSS_SELECTOR = 'td.content dt > a'

# START_DATE = date(2004, 4, 20)
START_DATE = date(2018, 4, 10)
END_DATE = date.today()
DATE_FMT = '%Y%m%d'
DATE_RE = re.compile('&date=(.*?)$', re.DOTALL)

########################################################################
# Codes
########################################################################


def _date_to_str_date(date):
    return date.strftime(DATE_FMT)


def _daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def yield_start_urls():
    for dt in _daterange(START_DATE, END_DATE + timedelta(days=1)):
        yield URL_TMPL.format(date=_date_to_str_date(dt))


class NaverNewsSpider(scrapy.Spider):
    name = 'naver_news'
    allowed_domains = ['http://news.naver.com']

    def start_requests(self):
        for url in yield_start_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        date = DATE_RE.findall(response.url)[0]
        urls = response.css(LINK_CSS_SELECTOR + '::attr(href)').extract()
        titles = response.css(LINK_CSS_SELECTOR + '::text').extract()
        iterable = enumerate(zip(urls, titles), start=1)

        for rank, (news_url, news_title) in iterable:
            yield {
                'rank': rank,
                'url': self.allowed_domains[0] + news_url,
                'title': news_title,
                'date': date
            }