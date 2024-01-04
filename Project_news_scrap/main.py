import requests
from bs4 import BeautifulSoup
import logging

# 로그 파일 설정
logging.basicConfig(filename='cnn_news.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# User-Agent 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.9999.0 Safari/537.36'
}

# CNN 뉴스 웹페이지 URL
url = 'https://edition.cnn.com/business'

# HTTP GET 요청 보내기 (User-Agent 포함)
response = requests.get(url, headers=headers)

# 응답 확인
if response.status_code == 200:
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 동일한 종류의 여러 클래스를 가진 div 요소 찾기
    container_articles = soup.find_all('div', class_='card')

    if container_articles:
        # 모든 뉴스 정보 가져오기
        for container_article in container_articles:
            # 뉴스 제목 추출
            news_title = container_article.find('span', class_='container__headline-text')
            if news_title:
                news_title = news_title.get_text(strip=True)
            else:
                news_title = "뉴스 제목 없음"

            # 링크 추출
            news_link = container_article.find('a', class_='container__link')
            if news_link:
                news_link = 'https://edition.cnn.com' + news_link['href']
            else:
                news_link = "링크 없음"

            # 정보 출력
            print("뉴스 제목:", news_title)
            print("뉴스 링크:", news_link)
            print("\n")

            # 로그 파일에 저장
            logging.info("뉴스 제목: %s", news_title)
            logging.info("뉴스 링크: %s", news_link)
    else:
        print("뉴스 정보를 찾을 수 없습니다.")
else:
    print("HTTP 요청에 실패하였습니다. 상태 코드:", response.status_code)
