from bs4 import BeautifulSoup
import requests
import tqdm.notebook as tqdm
import time
import pandas as pd

def createURL(month, day):
    url = 'https://keirin.kdreams.jp/racecard/2021/' + str(month).zfill(2) + '/' + str(day).zfill(2) + '/'
    return url

seedURLs = [ createURL(i, j) for i in range(4, 8, 1) for j in range(1, 30, 1)]
print(seedURLs)

def get_race_urls(sourceURLs):
    #URLを格納するための辞書を定義
    race_urls = {}
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
            for html in race_html:
                url = html.get('href')
                #"一覧"のURL以外を取得
                if 'racedetail' in url:
                    race_id = req.sub(r'\D', '', url)
                    race_urls[race_id] = url
        except:
            break
    return race_urls

race_urls = get_race_urls(seedURLs)
print(race_urls)

main_colum = ['予想', '好気合', '総評', '枠番', '車番', '選手名府県/年齢/期別', '級班', '脚質', 'ギヤ倍数', '競走得点', '1着', '2着', '3着', '着外']
result_colum = ['予想', '着順', '車番', '選手名', '着差', '上り', '決まり手', 'S/B', '勝敗因']

race_results = None

def scrape_race_result(race_urls, pre_race_results={}):
    #取得途中のデータを途中から読み込む
    race_results = pre_race_results
    for race_id, url in tqdm.tqdm(race_urls.items()):
        if race_id in race_results.keys():
            continue
        try:
            #ページ内ののテーブル(表)のhtmlを取得
            main = pd.read_html(url)

            #レース情報(特徴量データ)のテーブルを取得
            df = main[4][:-1]
            df.columns = main_colum

            #レース結果(教師データ)のテーブルを取得
            result_table = main[-2]
            result_table.columns = result_colum
            df_result = result_table.loc[ : , ['着順', '車番']]

            #文字列型に変換
            df = df.astype(str)
            df_result = df_result.astype(str)

            #特徴量データと教師データを一つにまとめる
            df = pd.merge(df_result, df, on='車番', how='left')
            race_results[race_id] = df

            #1秒待機
            time.sleep(1)
        except IndexError:
            print('IndexError: {}', url)
            continue
        except KeyError:
            print('keyerror: {}', url)
            continue
        except ValueError:
            print("ValueError: {}", url)
            continue
        except :
            traceback.print_exc()
            break
    return race_results

results = scrape_race_result(race_urls, race_results)

# #各レースデータの行名をレースIDに変更
for key in results.keys():
    results[key].index = [key]*len(results[key])
#全データを結合
race_results = pd.concat([results[key] for key in results.keys()], sort=False)

print("race_results")