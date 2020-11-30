import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import os

def run():
    cols =["fixture_id","channel_name","snavie_channel_id","date_utc",
            "start_time_utc","end_time_utc","is_live","is_sport","program_title_1_original",
            "program_title_2_original","program_description_original","program_title_1_eng",
            "program_title_2_eng","program_description_eng"]
    sport_list = ["patinaje","voleibol","atletismo",
                    "ciclismo","motociclismo","bobsleigh",
                    "golf","baloncesto","triatlon",
                    "gimnasia","tenis"]
    channel_name = "TeleDeporte"

    today = datetime.now().date()
    date_list = [today + timedelta(days=x) for x in range(3)]
    for date in date_list:
        date_url = date.strftime("%d%m%Y")

        url = "https://www.rtve.es/contenidos/sala-de-comunicacion/programacion-descargable/TELEDEPORTE_{}.html".format(date_url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        result_list = []
        result_list.append(cols)
        results = soup.find_all('strong')


        for res in results[1:]:

            line = res.text
            start_time = line[:5]
            title = line[5:]


            is_sport = None
            if any(word in title.lower() for word in sport_list):
                is_sport = True


            item = [None,channel_name,None,date,start_time,None,None,is_sport,title,None,None,None,None,None]
            result_list.append(item)


        index_length = len(result_list) -1
        df = pd.DataFrame(result_list[1:],columns=result_list[0])




        for index in df.index:
            if index < index_length -1:
                df.at[index, 'end_time_utc'] = df.loc[index+1]["start_time_utc"]
        path = "output\\teledeporte_spain"
        if not os.path.exists(path):
            os.makedirs(path)
        print(df.head())
        df.to_csv('output\\teledeporte_spain\{}.csv'.format(date), index=False, header=True,encoding='utf-8-sig')

if __name__ == "__main__":
    run()