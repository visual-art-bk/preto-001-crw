from WebDriverSingleton import WebDriverSingleton
from GeneralCrawler import GeneralCrawler
import time

TIME_SLIP_FOR_CLOSE_DRAIVER = 10
URL_NAVER = 'https://www.naver.com'

wds = WebDriverSingleton()
general_craw = GeneralCrawler()
driver = wds.get_driver()

# 다른 모듈이나 함수에서 사용
def navigate_to_site(url):
    driver.get(url)


# 프로그램 실행
if __name__ == '__main__':
    navigate_to_site(URL_NAVER)
    # 다른 작업 수행
    
    general_craw.init(driver)
    general_craw.search_keyword('강아지 사료', "input[name='query']")
    general_craw.go_blog_tab()

    time.sleep(TIME_SLIP_FOR_CLOSE_DRAIVER)
    wds.close_driver()