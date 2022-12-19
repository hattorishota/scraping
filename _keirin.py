import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import tqdm

def createURL(month, day):
    url = 'https://keirin.kdreams.jp/racecard/2021/' + str(month).zfill(2) + '/' + str(day).zfill(2) + '/'
    return url

seedURLs = [ createURL(i, j) for i in range(4, 5, 1) for j in range(1, 2, 1)]
# print(seedURLs)

def get_race_urls(sourceURLs):
    #URLを格納するための辞書を定義
    race_urls = []

    #tqdmを使うことでループの進度が表示される
    for sourceURL in tqdm.tqdm(sourceURLs):
        try:
            #リクエストを作成
            req = requests.get(sourceURL)

            #htmlデータを取得
            soup = BeautifulSoup(req.content, 'html.parser')

            #3秒待機
            time.sleep(3)

            #レース情報のページのURLを取得する
            race_html = soup.find_all('a', class_='JS_POST_THROW')

            for i in range(len(race_html)):
                url = race_html[i].get('href')
                ngword = 'racecard'

                if ngword not in url:
                  race_urls.append(url)

        except:
            break
    return race_urls

race_urls = get_race_urls(seedURLs)
print(race_urls)

for race_url in tqdm.tqdm(race_urls):
  try :
    r = pd.read_html(race_url, header = 0) 

    df = pd.DataFrame(r[0])
    df.to_excel('keirin.xlsx')

    time.sleep(3)

  except :
    break