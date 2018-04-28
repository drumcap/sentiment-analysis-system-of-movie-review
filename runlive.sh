#!/bin/bash

cd ~/Documents/sentiment-analysis-system-of-movie-review/data
PATH=$PATH:~/anaconda3/bin
export PATH

scrapy crawl movie-recent-comment