from selenium import webdriver
from selenium.webdriver.support.select import Select
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import csv


print("出発駅を入力してください.")
startStation = input()
print("到着駅を入力してください.")
endStation = input()
print("月日時間を入力してください.(入力例：12/01/13/58)\n※現在時刻で取得する場合は「now」と入力してください。")
dateTime = None
while(dateTime == None):
    dateTime = input()

#ChromeDriverのパスを引数に指定しChromeを起動
driver = webdriver.Chrome("c:/driver/chromedriver")
#指定したURLに遷移
driver.get("https://transit.yahoo.co.jp/")
#idを取得
month = driver.find_element_by_id("m")
day = driver.find_element_by_id("d")
hour = driver.find_element_by_id("hh")
minute = driver.find_element_by_id("mm")
#セレクトタグの要素を指定してSelectクラスのインスタンスを作成
select = Select(month)

if(dateTime != "now"):
    dateTime = dateTime.split("/")
    dateTime = list(map(int, dateTime))

driver.find_element_by_id("sfrom").send_keys(startStation)
driver.find_element_by_id("sto").send_keys(endStation)

if(dateTime != "now"):
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
time_req = SOUP.select('#rsltlst .time span.small')
price = SOUP.select('#rsltlst .fare span.mark')
transfer = SOUP.select('#rsltlst .transfer')
tmpA = time_req[0]
priceA = price[0]
transferA = transfer[0]
print("所要時間：" + tmpA.getText())
print("料金：" + priceA.getText())
print(transferA.getText())
