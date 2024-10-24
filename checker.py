from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from colorist import green, yellow, red

def __is_blank_test(str):
    if len(str) == 0:
        return True
    return False


def pick_element_by_css_selector(driver: webdriver.Chrome, css_selector):
    exit_elem = None

    try:
        elements = driver.find_elements(By.CSS_SELECTOR, css_selector)

        if len(elements) > 0:
            print(
                f"CSS Selector에 부합하는 엘리먼트가 존재합니다. '{len(elements)}'개입니다."
            )

            for elem in elements:
                if __is_blank_test(elem.text) == True:
                    print("CSS Selector에 부합하는 엘리멘트의 텍스트가 공백입니다.")
                else:
                    print(f"--> CSS Selector에 부합하는 텍스트는 [ '{elem.text}' ]")
                    exist_elem = elem

            return exist_elem
        else:
            print("CSS Selector에 부합하는 엘리먼트가 존재하지 않습니다.")
            return None

    except Exception as e:
        print(f"에러 발생: {e}")
        return None


def pick_element_by_xpath(driver: webdriver.Chrome, xpath, keyword):
    exist_elem = None

    try:
        elements = driver.find_elements(By.XPATH, xpath)

        if len(elements) > 0:
            print(
                f"['{keyword}']와 관계된 엘리먼트가 존재합니다. '{len(elements)}'개입니다."
            )

            for elem in elements:
                if __is_blank_test(elem.text) == True:
                    print(f"['{keyword}']와 관계된 엘리멘트의 텍스트가 공백입니다.")
                else:
                    print(f"--> 찾은 텍스트는 [ '{elem.text}' ]")
                    exist_elem = elem

            return exist_elem
        else:
            print(f"['{keyword}']와 관계된 엘리먼트가 존재하지 않습니다.")
            return None

    except Exception as e:
        print(f"에러 발생: {e}")
        return None


def pick_multiple_element_by_xpath(driver: webdriver.Chrome, xpath):
    exist_elems = []

    try:
        elements = driver.find_elements(By.XPATH, xpath)

        if len(elements) > 0:
            print(f"엘리먼트가 존재합니다. '{len(elements)}'개입니다.")

            for elem in elements:
                if __is_blank_test(elem.text) == True:
                    print("엘리멘트의 텍스트가 공백입니다.")
                else:
                    print(f"--> 찾은 텍스트는 [ '{elem.text}' ]")
                    exist_elems.append(elem)

            return exist_elems
        else:
            print("엘리먼트가 존재하지 않습니다.")
            return None

    except Exception as e:
        print(f"에러 발생: {e}")
        return None


def check_iframes(driver: WebDriverWait):
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    length = len(iframes)
    if length == 0:
        return False
    
    elif length == 1:
        yellow(f"iframe 1개 발견되었습니다!")
        return True

    for index, iframe in enumerate(iframes):
        iframe_src = iframe.get_attribute("src") 
        
        red(f"No handle of this error: '{length}개의 iframe이 발견되었고 처리가 필요합니다.'")
        red(f"iframe {index+1}의 링크: {iframe_src}")
    return True