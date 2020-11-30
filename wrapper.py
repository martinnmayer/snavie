import eurosport_italy as ei
import teledeporte_spain as tds
import cosmote_greece as cg
import tv2
from datetime import datetime


print("*"*20)
print("Starting to scrape Cosmote Greece")
print("*"*20)
try:

    date_string = datetime.now().strftime("%Y_%m_%d")
    cg.run(date_string)
    print("Finished")
except Exception as e:
    print("error in scraping")
    print(e)


print("*"*20)
print("Starting to scrape TeleDeporte Spain")
print("*"*20)
try:
    tds.run()
    print("Finished")
except Exception as e:
    print("error in scraping")
    print(e)
print("*"*20)


print("Starting to scrape Eurosport Italy")
print("*"*20)
try:
    ei.run()
    print("Finished")
except Exception as e:
    print("error in scraping")
    print(e)
print("*"*20)

print("Starting to scrape TV2")
print("*"*20)
try:
    tv2.run()
    print("Finished")
except Exception as e:
    print("error in scraping")
    print(e)
print("*"*20)
