import requests
from bs4 import BeautifulSoup
import logging
import csv

# 로그 파일 설정 (UTF-8 인코딩)
logging.basicConfig(filename='news.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# User-Agent 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.9999.0 Safari/537.36'
}

# CNN 뉴스 웹페이지 URL
cnn_url = 'https://edition.cnn.com/business'

# Time 뉴스 웹페이지 URL
time_url = 'https://time.com/section/business/'

# 사용자 입력 받기
num_of_news = int(input("원하는 뉴스 수를 입력하세요: "))

# CSV 파일로 데이터 저장할 리스트 생성
news_data = []

# Scraping CNN News
response_cnn = requests.get(cnn_url, headers=headers)

# 응답 확인
if response_cnn.status_code == 200:
    # BeautifulSoup을 사용하여 HTML 파싱
    soup_cnn = BeautifulSoup(response_cnn.text, 'html.parser')

    # 동일한 종류의 여러 클래스를 가진 div 요소 찾기
    container_articles_cnn = soup_cnn.find_all('div', class_='card')

    if container_articles_cnn:
        # 중복 기사를 체크하기 위한 set
        seen_articles_cnn = set()

        # 사용자가 입력한 수만큼 뉴스 정보 가져오기
        for i, container_article_cnn in enumerate(container_articles_cnn):
            # 뉴스 제목 추출
            news_title_cnn = container_article_cnn.find('span', class_='container__headline-text')
            if news_title_cnn:
                news_title_cnn = news_title_cnn.get_text(strip=True)
            else:
                news_title_cnn = "뉴스 제목 없음"

            # 링크 추출
            news_link_cnn = container_article_cnn.find('a', class_='container__link')
            if news_link_cnn:
                news_link_cnn = 'https://edition.cnn.com' + news_link_cnn['href']
            else:
                news_link_cnn = "링크 없음"

            # 중복 기사 체크
            if news_title_cnn not in seen_articles_cnn:
                seen_articles_cnn.add(news_title_cnn)

                # 정보 출력
                print("CNN 뉴스 제목:", news_title_cnn)
                print("CNN 뉴스 링크:", news_link_cnn)
                print("\n")

                # 로그 파일에 저장
                logging.info("CNN 뉴스 제목: %s", news_title_cnn)
                logging.info("CNN 뉴스 링크: %s", news_link_cnn)

                # 뉴스 데이터를 리스트에 추가
                news_data.append(['CNN', news_title_cnn, news_link_cnn])

                # 사용자가 입력한 수만큼 뉴스 스크랩
                if len(seen_articles_cnn) >= num_of_news:
                    break
    else:
        print("CNN 뉴스 정보를 찾을 수 없습니다.")
else:
    print("CNN HTTP 요청에 실패하였습니다. 상태 코드:", response_cnn.status_code)

# Scraping Time News
response_time = requests.get(time_url, headers=headers)

# 응답 확인
if response_time.status_code == 200:
    # BeautifulSoup을 사용하여 HTML 파싱
    soup_time = BeautifulSoup(response_time.text, 'html.parser')

    # 'taxonomy-tout' 클래스를 가진 <div> 태그들 찾기
    tout_divs = soup_time.find_all('div', class_='taxonomy-tout')

    if tout_divs:
        # 중복 기사를 체크하기 위한 set
        seen_articles_time = set()

        # 사용자가 입력한 수만큼 뉴스 정보 가져오기
        for i, tout_div in enumerate(tout_divs):
            # <a> 태그를 찾고 href 속성 추출
            news_link_time = 'https://time.com' + tout_div.find('a')['href']

            # 뉴스 제목 추출
            news_title_time = tout_div.find('h2', class_='headline').get_text(strip=True)

            # 중복 기사 체크
            if news_link_time not in seen_articles_time:
                seen_articles_time.add(news_link_time)

                # 정보 출력
                print("Time 뉴스 제목:", news_title_time)
                print("Time 뉴스 링크:", news_link_time)
                print("\n")

                # 로그 파일에 저장
                logging.info("Time 뉴스 제목: %s", news_title_time)
                logging.info("Time 뉴스 링크: %s", news_link_time)

                # 뉴스 데이터를 리스트에 추가
                news_data.append(['Time', news_title_time, news_link_time])

                # 사용자가 입력한 수만큼 뉴스 스크랩
                if len(seen_articles_time) >= num_of_news:
                    break
    else:
        print("Time 뉴스 정보를 찾을 수 없습니다.")
else:
    print("Time HTTP 요청에 실패하였습니다. 상태 코드:", response_time.status_code)

# 뉴스 데이터를 CSV 파일로 저장
with open('news.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Source', 'Title', 'Link'])
    for data in news_data:
        csv_writer.writerow(data)

print("뉴스 정보를 news.csv 파일로 저장했습니다.")
