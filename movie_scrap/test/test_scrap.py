# Intellij Scrapy 테스트용 실행파일


from scrapy import cmdline

# cmdline.execute("scrapy crawl quotes".split())
# cmdline.execute("scrapy crawl naver_news -o naver_news.jl".split())
cmdline.execute("scrapy crawl movie-rank".split())