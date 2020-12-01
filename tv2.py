import requests
from datetime import datetime, timedelta
import pandas as pd
import itertools
import os


def get_programme_list(target_date,channel):
    channel_id = channel[0]
    channel_name = channel[1]
    sport_true_list = ["tennis:","banecykling:","håndboldMatchen:","skiskydning","fodbold","ski"]
    sport_false_list = ["Studiet"]

    result_list = []
    columns =["fixture_id","channel_name","snavie_channel_id","date_utc",
        "start_time_utc","end_time_utc","is_live","is_sport","program_title_1_original",
        "program_title_2_original","program_description_original","program_title_1_eng",
        "program_title_2_eng","program_description_eng"]
    result_list.append(columns)
    url = "https://tvtid-api.api.tv2.dk/api/tvtid/v1/epg/dayviews/{}?ch={}".format(target_date,channel[0])
    response = requests.get(url)
    json_list = response.json()
    if json_list:
        json_list = json_list[0]
        programs = json_list["programs"]
        for program in programs:
            start_datetime = datetime.fromtimestamp(program["start"])
            date_utc = start_datetime.date()
            start_time = (str(start_datetime.time())[:-3])
            end_datetime = datetime.fromtimestamp(program["stop"])
            end_time = (str(end_datetime.time())[:-3])
            is_live = program["live"]
            event_id = program["id"]
            is_sport = "unknown"
            title = program["title"]
            if any(word.lower() in title.lower() for word in sport_true_list):
                is_sport = True
            elif any(word in title for word in sport_false_list):
                is_sport = False

            result_list.append([
                event_id,
                channel_name,
                None,
                date_utc,
                start_time,
                end_time,
                is_live,
                is_sport,
                title,
                None,
                None,
                None,None,None
            ])
        df = pd.DataFrame(result_list)
        path = os.path.join("output","tv2")
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = "{}_{}.csv".format(channel_name,target_date)
        df.to_csv(os.path.join(path,file_name), index=False, header=False,encoding='utf-8-sig')

def run():
    today = datetime.today()
    date_list = [(today + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(20)]
    channel_list = {
        "2147483561": "TV 2 SportX",
        "2147483561": "TV 2 SportX",
        "2147483568": "TV 2 Play 1",
        "2147483567": "TV 2 Play 2",
        "2147483566": "TV 2 Play 3",
        "2147483565": "TV 2 Play 4",
        "2147483564": "TV 2 Play 5",
        "2147483563": "TV 2 Play 6",
        "2147483562": "TV 2 Play 7",
    }
    for x in itertools.product(date_list,channel_list.items()):
        print("Starting: {} - {}".format(x[0],x[1][1]))
        get_programme_list(x[0],x[1])


if __name__ == "__main__":
    run()