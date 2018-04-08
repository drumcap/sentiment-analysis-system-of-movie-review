# sentiment-analysis-system-of-movie-review
빅데이터 기술전문가 15기 3조 프로젝트 - SNS 빅데이터로 분석하는 영화리뷰 감성분석 시스템

기술전문가 과정에 맞게 비교적 분석이 어렵지 않은 주제인 영화 리뷰 분석으로 빅데이터 시스템을 구축한다

## 실습 서버사양
총 3대이며 각각 centOS 7, 메모리 32GB, 8코어, 300GB 

## 시스템 아키텍처
- 서버1 : 수집서버, 검색엔진
  - Scrapy
  - Fluentd
  - Flume
  - ElashticSearch
  - Cratedb
- 서버2 : HDFS Main
  - Hortonworks NN
  - DN1
- 서버3 : Spark Main, 분석 대시보드
  - DN2
  - Spark
  - Zeppelin
  - Kibana
  - Redis
  - WAS

