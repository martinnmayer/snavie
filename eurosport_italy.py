import requests
from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup
import pandas as pd
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")

#Get the password
config = config_object["SCRAPERCONFIG"]
chosen_driver = config["driver"]

if chosen_driver != "firefox":

    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")


def run():
    sport_list  = ["snooker","biathlon","sci alpino",
                "pure etcr","rally","combinata nordica",
                "sci di fondo","scacchi","salto con sci"]
    if chosen_driver == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=option)
    driver.get("https://www.eurosport.it/watch/schedule.shtml")
    time.sleep(3)
    driver.find_element_by_xpath('//button[contains(text(),"ACCETTO")]').click()
    result_list =[]
    columns =["fixture_id","channel_name","snavie_channel_id","date_utc",
    "start_time_utc","end_time_utc","is_live","is_sport","program_title_1_original",
    "program_title_2_original","program_description_original","program_title_1_eng",
    "program_title_2_eng","program_description_eng","sport_name","is_premium"]
    result_list.append(columns)
    for i in range(7):
        response = driver.page_source
        soup = BeautifulSoup(response,features="lxml")
        inner = soup.find("script", {"id": "__NEXT_DATA__"})
        json_all = json.loads(inner.decode_contents())
        json_results = json_all["props"]["pageProps"]["serverQueryRecords"]

        all_events = [value for key, value in json_results.items() if 'eurosport-' in key.lower()]
        for event in all_events:
            if "title" in event:
                start_date_time = datetime.strptime(event["startTime"],"%Y-%m-%dT%H:%M:%S.%fZ")
                end_date_time = datetime.strptime(event["endTime"],"%Y-%m-%dT%H:%M:%S.%fZ")
                channel = "unknown"
                channel_id = event["__id"].split("ch")[1]
                if channel_id == "204":
                    channel = "Eurosport_2"
                elif channel_id == "4":
                    channel = "Eurosport_1"
                elif channel_id in ("732","730","729"):
                    channel = "Eurosport"
                is_sport = event["sportName"].lower() in sport_list

                result = [None,channel,None,start_date_time.date(),start_date_time.time(),
                        end_date_time.time(),event["isLive"],
                        is_sport,event["title"],event["subtitle"],None,None,None,None,
                        event["sportName"],event["isPremium"]
                        ]


                result_list.append(result)
        driver.find_element_by_xpath('//button[@data-testid="next-button"]').click()
        time.sleep(3)
    my_df = pd.DataFrame(result_list)
    
    path = os.path.join("output","eurosport_italy")
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = "{}.csv".format(datetime.now().date())
    my_df.to_csv(os.path.join(path,file_name), index=False, header=False,encoding='utf-8-sig')
    driver.close()


if __name__ == "__main__":
    run()