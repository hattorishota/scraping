from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

for n in range(2,6):

    url = 'https://web-kanji.com/search/okinawa/page/'+str(n)
    r = requests.get(url)
    time.sleep(3)

    soup = BeautifulSoup(r.text, 'html.parser')

    contents = soup.find(class_="companies")
    get_a = contents.find_all("a", class_='companies-item')

    title_links = []
    for i in range(len(get_a)):
        try:
            link_ = get_a[i].get("href")
            title_links.append(link_)
        except:
            pass
    #print(title_links)

    #title_link = title_links[0]
    #print(title_link)

    #for i in range(len(title_links)):
        #title_link = title_links[i]
        #print(str(i)+"回目のループ→",title_link)

    company_titles = []
    company_links = []

    for i in range(len(title_links)):
        title_link = title_links[i]
    #     print(str(i)+"回目のループ→",title_link)

        r = requests.get(title_link)
        time.sleep(3)
        soup = BeautifulSoup(r.text, 'html.parser')

        content = soup.find('dl', class_='company-data is-narrow')
        company_title = str(content.find('dd')).strip('</dd>')
        #company_title = soup.find(class_="company-data is-narrow").text
        #print(company_title) 
        company_titles.append(company_title)
        company_link = soup.find('a', class_='link js-forced-ad is-wordbreak')['href']
        company_links.append(company_link)  
    #print(company_titles)
    #print(company_links)   

    result ={
        'company_title' : company_titles,
        'company_link' : company_links
    }
    #print(result)
    df = pd.DataFrame(result)
    print(df)
    df.to_excel('result'+str(n)+'.xlsx', index=False, encoding='utf-8')