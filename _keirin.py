import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import tqdm
import os
import glob

# 曜日ごとのレースのページを取得
def createURL(month, day):
    url = 'https://keirin.kdreams.jp/racecard/2021/' + str(month).zfill(2) + '/' + str(day).zfill(2) + '/'
    return url

seedURLs = [ createURL(i, j) for i in range(4, 5, 1) for j in range(1, 2, 1)]
# print(seedURLs)

# レースごとのURlを取得する
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

# レースごとのURLをもとにループさせる
# 現状：1レースごとにファイルが生成され、積み重なっていく。
for n, race_url in tqdm.tqdm(enumerate(race_urls)):

  # ループ1回目でデータを入れるためのフォルダを作成
  if n == 0:
    os.mkdir('race_data')

  # ページ内にあるtableタグの中身を取得
  r = pd.read_html(race_url, header = 0) 

  df = pd.DataFrame(r[0])

  # エクセルで出力
  df.to_csv('race_data/result' + str(n) + '.csv')

  # 3秒待機
  time.sleep(3)


# csvファイルを結合する
# 現状：うまくいってない
# 原因：csvファイルのそれぞれ1行目がなんとからしい

# # ディレクトリ変更
# os.chdir('/Users/hattorishota1/github.com/scraping/race_data')

# #1---フォルダ内のCSVファイルの一覧を取得
# files = sorted(glob.glob('race_data/*.csv'))

# #2---ファイル数を取得
# file_number = len(files)

# #3---CSVファイルの中身を読み出して、リスト形式にまとめる
# csv_list = []

# for file in files:
#     csv_list.append(pd.read_csv(file))

# #4---CSVファイルの結合
# df = pd.concat(csv_list, axis = 0, sort = True)

# #5---CSVファイル出力
# df.to_csv("race_data.csv", index = False)

# #6---完了合図
# print(file_number,' 個のCSVファイルを結合完了！！')