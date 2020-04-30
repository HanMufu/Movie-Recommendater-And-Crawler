from selenium import webdriver
import pymysql
from selenium.webdriver.chrome.options import Options


def open_chrome(headless=True):
    if headless:
        chrome_options = Options()
        # 设置chrome浏览器无界面模式
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
    else:
        driver = webdriver.Chrome()
    return driver


def get_thumbnail(driver, url):
    driver.get(url)
    try:
        img_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a/yt-img-shadow/img'
        image = driver.find_element_by_xpath(img_xpath)
        img_url = image.get_attribute('src')
    except Exception as e:
        print(e)
    return img_url


fname = 'database_password.txt'
with open(fname, 'r') as f:
    lines = f.readlines()
    host_ip = lines[0].strip('\n')
    user = lines[1].strip('\n')
    password = lines[2].strip('\n')
    database_name = lines[3].strip('\n')

# 打开数据库连接
db = pymysql.connect(host_ip, user, password, database_name)

# 使用cursor()方法获取操作游标
cursor = db.cursor()

db1 = pymysql.connect(host_ip, user, password, database_name)
cursor1 = db1.cursor()

# SQL 查询语句
sql = "SELECT * FROM movies"
try:
    driver = open_chrome()
    cursor.execute(sql)
    results = cursor.fetchall()
    counter = 0
    for row in results:
        movieId = row[0]
        title = row[1]
        genres = row[2]
        youtubeEmbedId = row[3]
        img_url = row[4]
        print(title)
        if img_url == 'https://i.ytimg.com/vi/bTqVqk7FSmY/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCuux40l6PQKzR7E2HnI1G8UyKT-w':
            try:
                # url = 'https://www.youtube.com/results?search_query=%s' % (title + ' trailer')
                url = 'https://www.youtube.com/results?search_query=%s' % (title)
                img_url = get_thumbnail(driver, url)
                print(img_url)
            except Exception as e:
                print(e.message)
                continue
            sql1 = "UPDATE movies SET imgUrl = '%s' WHERE movieId = '%s'" % (img_url, movieId)
            try:
                cursor1.execute(sql1)
                db1.commit()
                counter += 1
                print("%s is done" % str(counter))
            except:
                db1.rollback()
    driver.quit()

except Exception as e:
    print("Error: unable to fetch data")
    print(e.message)

# 关闭数据库连接
db.close()
db1.close()