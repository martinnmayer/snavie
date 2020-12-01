from xml.dom import minidom
import pandas as pd
from datetime import datetime
import os

def run(date_data="2020_09_28"):
    xmldoc = minidom.parse('sources/COSMOTE Sport1HD_{}.xml'.format(date_data))
    columns =["fixture_id","channel_name","snavie_channel_id","date_utc",
        "start_time_utc","end_time_utc","is_live","is_sport","program_title_1_original",
        "program_title_2_original","program_description_original","program_title_1_eng",
        "program_title_2_eng","program_description_eng"]


    itemlist = xmldoc.getElementsByTagName('broadcast')
    result_list = []
    for s in itemlist:
        channel_name = s.getElementsByTagName('station')[0].firstChild.data
        date_utc_raw = s.getElementsByTagName('start_date')[0].firstChild.data
        date_utc = datetime.strptime(date_utc_raw, '%Y-%m-%d').date()
        start_time = s.getElementsByTagName('start_time')[0].firstChild.data
        end_time = s.getElementsByTagName('end_time')[0].firstChild.data
        is_live = "[LIVE]" in s.getElementsByTagName('title')[0].firstChild.data
        is_sport = "Show:" not in s.getElementsByTagName('title')[0].firstChild.data
        title = s.getElementsByTagName('title')[0].firstChild.data
        title_2 = ""
        description = s.getElementsByTagName('text')[0].firstChild.data


        result_list.append([
            None,
            channel_name,
            None,
            date_utc,
            start_time,
            end_time,
            is_live,
            is_sport,
            title,
            title_2,
            description,None,None,None
        ])
        
    my_df = pd.DataFrame(result_list,columns=columns)

    path = os.path.join("output","cosmote_greece")
    if not os.path.exists(path):

        os.makedirs(path)
    file_name = date_data + ".csv"
    my_df.to_csv(os.path.join(path,file_name), index=False, header=True,encoding='utf-8-sig')
    my_df.head(40)


if __name__ == "__main__":
    date_string = datetime.now().strftime("%Y_%m_%d")
    run(date_string)