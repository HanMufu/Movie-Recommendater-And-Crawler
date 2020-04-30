import pymysql
from selenium import webdriver
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


def get_embedId(driver, movie_title):
    driver.get('https://www.youtube.com/results?search_query=%s' % (movie_title + ' trailer'))
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        if i.get_attribute('href') is not None:
            text = i.get_attribute('href')
            print(text)
            break
    embedId = text[-11:]
    print(embedId)
    return embedId


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
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    counter = 0
    for row in results:
        movieId = row[0]
        title = row[1]
        genres = row[2]
        youtubeEmbedId = row[3]
        print(title)
        if youtubeEmbedId == 'bTqVqk7FSmY':
            youtubeEmbedId = get_embedId(driver, title)
            sql1 = "UPDATE movies SET youtubeEmbedId = '%s' WHERE movieId = '%s'" % (youtubeEmbedId, movieId)
            try:
                # 执行SQL语句
                cursor1.execute(sql1)
                # 提交到数据库执行
                db1.commit()
                counter += 1
                print("%s is done" % str(counter))
            except:
                # 发生错误时回滚
                db1.rollback()
    driver.quit()

except Exception as e:
    print("Error: unable to fetch data")
    print(e.message)

# 关闭数据库连接
db.close()
db1.close()