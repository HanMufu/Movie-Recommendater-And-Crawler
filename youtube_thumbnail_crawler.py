from selenium import webdriver


def get_thumbnail(url):
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        img_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a/yt-img-shadow/img'
        image = driver.find_element_by_xpath(img_xpath)
        img_url = image.get_attribute('src')
        print(img_url)
    except Exception as e:
        print(e)
    driver.quit()


url1 = 'https://www.youtube.com/results?search_query=honggaoliang+trailer'
get_thumbnail(url1)