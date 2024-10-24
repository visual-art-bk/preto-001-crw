import pandas as pd
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from WebDriverSingleton import WebDriverSingleton
import checker
import time
from colorist import green, yellow, red
from xml.etree import ElementTree as ET

# 크롬 드라이버 설정 및 페이지 접근
CHROME_DRIVER_PATH = "/home/kbk/chromedriver-linux64/chromedriver"

wait = WebDriverWait(WebDriverSingleton().get_driver(), 3)


class GeneralCrawler:
    _keyword = ""
    _driver = None
    _cur_iframe = None
    _limit_size_keyword = 50
    _blogs_data = []
    _blog_author_data = {}

    def _wait():
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    @classmethod
    def init(cls, driver: webdriver.Chrome):
        cls._driver = driver
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        cls._driver.maximize_window()

    @classmethod
    def search_keyword(cls, keyword, css_selector_input):
        cls._keyword = keyword

        search_box = cls._driver.find_element(By.CSS_SELECTOR, css_selector_input)
        search_box.send_keys(cls._keyword)
        search_box.submit()

    @classmethod
    def go_blog_tab(cls):
        tab_name = "블로그"

        # 블로그 탭 클릭
        blog_tab = checker.pick_element_by_xpath(
            cls._driver, "//a[contains(text(),'블로그')]", "블로그"
        )
        time.sleep(2)  # 페이지 로딩 대기
        blog_tab.click()

        keywords = cls._keyword.split(" ")
        cls._crawl_01(keywords[0], keywords[1])

        # 엑셀 파일로 저장
        df = pd.DataFrame(cls._blogs_data, columns=["닉네임", "이메일", "방문자 수"])
        df.to_excel(f"naver_blog_data_{cls._keyword}.xlsx", index=False)

        print("블로그 데이터가 엑셀 파일로 저장되었습니다.")

    @classmethod
    def _crawl_01(cls, keyword_1, keyword_2):

        blog_count = 0
        rank = 1

        # 현재 창의 핸들을 저장 (부모 창)
        parent_window = cls._driver.current_window_handle

        blog_titles = checker.pick_multiple_element_by_xpath(
            cls._driver, '//a[@class="title_link"]'
        )

        if len(blog_titles) > cls._limit_size_keyword:
            last_count = cls._limit_size_keyword
        else:
            last_count = len(blog_titles)
            
        while blog_count < 21:
            for i, title in enumerate(blog_titles):
                if keyword_1 in title.text and keyword_2 in title.text:
                    title.click()  # 블로그 클릭
                    time.sleep(2)  # 페이지 로딩 대기

                    # @TODO [2324]
                    # 스크롤하여 클릭 요소를 화면에 표시하고 클릭
                    # try:
                    #     cls._driver.execute_script("arguments[0].scrollIntoView(true);", blog_titles[i])
                    #     cls._driver.execute_script("arguments[0].click();", blog_titles[i])
                    # except Exception as e:
                    #     print(f"블로그 {i + 1} 클릭 중 오류 발생: {e}")
                    #     continue

                    # 새 창으로 전환
                    cls._driver.switch_to.window(cls._driver.window_handles[-1])

                    if checker.check_iframes(cls._driver) == True:
                        iframe = cls._driver.find_element(By.TAG_NAME, "iframe")
                        red(
                            f"iframes으로 전환, 다음의 링크로 가서, 엘리멘터 xpath or, css를 반드시 확인바람."
                        )
                        red(iframe.get_attribute("src"))

                        cls._cur_iframe = iframe.get_attribute("src")
                        cls._driver.switch_to.frame(iframe)

                    print(f"#{i} - 게시물")
                    post_data = cls._crawl_target_blog_post(cls)
                    cls._blogs_data.append(post_data)

                    rank += 1
                    blog_count += 1
                    cls._driver.close()

                    cls._driver.switch_to.window(parent_window)

                    if blog_count >= last_count:
                        break

    def _crawl_target_blog_post(cls):
        blog_id = None
        post_author_data = []

        # 닉네임
        try:
            nickname = cls._driver.find_element(By.XPATH, '//span[@class="nick"]').text
            print(f"닉네임 - {nickname}")
        except:
            nickname = "닉네임-결과없음"
            print(f"닉네임 - {nickname}")

        # 블로그 아이디
        try:
            parsed_url = urlparse(cls._cur_iframe)
            query_params = parse_qs(parsed_url.query)
            blog_id = query_params.get("blogId", [None])[0]
            print(f"블로그id - {blog_id}")
        except:
            blog_id = "블로그-id-결과없음"
            print(f"블로그id - {blog_id}")

        # 블로그 소유자 메일주소
        blog_domain = "naver.com"
        blog_email = f"{blog_id}@{blog_domain}"
        print(f"이메일 - {blog_email}")

        # 블로그 방문자수
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # 브라우저 GUI를 사용하지 않음
            service = Service(executable_path=CHROME_DRIVER_PATH)
            tmp_driver = webdriver.Chrome(options=options, service=service)

            naver_api = f"https://blog.naver.com/NVisitorgp4Ajax.nhn?blogId={blog_id}"
            tmp_driver.get(naver_api)
            tmp_driver.implicitly_wait(10)
            
            cls._driver.get(naver_api)
            cls._driver.implicitly_wait(10)

            cnt_value = tmp_driver.find_element(By.ID, "20241024").get_attribute("cnt")
            visitor_count = int(cnt_value)
            print(f"방문자수: {visitor_count}")
        except:
            visitor_count = "방문자수결과 없음"
            print(visitor_count)

        tmp_driver.quit()

        return [nickname, blog_email, visitor_count]
