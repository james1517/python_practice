from selenium import webdriver
from selenium.webdriver.support.select import Select
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import re

#ChromeDriverのパスを引数に指定しChromeを起動
driver = webdriver.Chrome("C:/Program Files (x86)/Python37-32/chromedriver")

#指定したURLに遷移
driver.get("https://transit.yahoo.co.jp/")

print("出発駅を入力してください.")
startStation = input()
print("到着駅を入力してください.")
endStation = input()
print("月日時間を入力してください.(入力例：12/01/13/58)")
dateTime = input()
dateTime = dateTime.split("/")
dateTime = list(map(int, dateTime))

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
tmp = SOUP.select('#rsltlst .time')
tmpA = tmp[0]
tmpB = tmpA.getText()[0:5]
print("出発時刻：" + tmpB)
tmp = SOUP.select('#rsltlst .time span.mark')
tmpA = tmp[0]
print("到着時刻：" + tmpA.getText())
tmp = SOUP.select('#rsltlst .time span.small')
tmpA = tmp[0]
print("所要時間：" + tmpA.getText())
tmp = SOUP.select('#rsltlst .fare')
tmpA = tmp[0]
print("料金：" + tmpA.getText())
tmp = SOUP.select('#rsltlst .transfer span.mark')
tmpA = tmp[0]
print("乗り換え回数：" + tmpA.getText())
#中身
# print(SOUP.select('#rsltlst .time span.mark').getText())