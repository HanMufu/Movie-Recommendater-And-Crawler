from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pyperclip
from selenium.webdriver.chrome.options import Options


def open_chrome(headless = True):
    if headless:
        chrome_options = Options()
        # 设置chrome浏览器无界面模式
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
    else:
        driver = webdriver.Chrome()
    return driver


def get_embedId(driver, movie_title):
    driver.get('https://www.youtube.com/results?search_query=%s' % (movie_title + ' trailer'))
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    print(user_data)
    for i in user_data:
        if i.get_attribute('href') is not None:
            text = i.get_attribute('href')
            print(text)
            break
    embedId = text[-11:]
    print(embedId)
    driver.close()
    return embedId

driver = open_chrome(False)
# driver.get('https://www.youtube.com/results?search_query=%s' % 'view from blue moon trailer')
# user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
# links = []
# for i in user_data:
#     links.append(i.get_attribute('href'))
#     if i.get_attribute('href') is not None:
#         print(i.get_attribute('href'))
# driver.getCurrentUrl()
get_embedId(driver, 'view from blue moon')
driver.quit()
