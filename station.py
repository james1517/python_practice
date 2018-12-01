from selenium import webdriver
from selenium.webdriver.support.select import Select
from pprint import pprint
import requests
from bs4 import BeautifulSoup


#ChromeDriverのパスを引数に指定しChromeを起動
driver = webdriver.Chrome("c:/driver/chromedriver")
#指定したURLに遷移
driver.get("https://transit.yahoo.co.jp/")

print("出発駅を入力してください.")
startStation = input()
print(startStation)

print("到着駅を入力してください.")
endStation = input()
print(endStation)

print("月日時間を入力してください.(入力例：12/01/13/58)")
dateTime = input()
dateTime = dateTime.split("/")
dateTime = list(map(int, dateTime))
print(dateTime)

driver.find_element_by_id("sfrom").send_keys(startStation)
driver.find_element_by_id("sto").send_keys(endStation)

#idを取得
month = driver.find_element_by_id("m")
day = driver.find_element_by_id("d")
hour = driver.find_element_by_id("hh")
minute = driver.find_element_by_id("mm")
#セレクトタグの要素を指定してSelectクラスのインスタンスを作成
select = Select(month)

#セレクトタグのオプションをインデックス番号から選択する
#通し番号が０から始まっているため-1
select.select_by_index(dateTime[0]-1)

select = Select(day)
select.select_by_index(dateTime[1]-1)
select = Select(hour)
select.select_by_index(dateTime[2])
select = Select(minute)
select.select_by_index(dateTime[3])

driver.find_element_by_id("searchModuleSubmit").click()

#カレントページのURLを取得
cur_url = driver.current_url

# POOL_MNG = PoolManager()
HTML = requests.get(cur_url)
SOUP = BeautifulSoup(HTML.content, "html.parser")
pprint(SOUP.select('#rsltlst .time'))

# html = request.urlopen(cur_url)
# soup = BeautifulSoup(html,"html.parser")
# for i in soup.find_all("li"):
#     print(urljoin(cur_url, i.get(".time")))
