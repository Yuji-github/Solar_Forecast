from bs4 import BeautifulSoup
import requests

url = requests.get("https://www.wunderground.com/history/daily/au/adelaide/YPAD/date/2022-2-3")
if url.status_code == 200:
    bs = BeautifulSoup(url.text)
    print(bs)
    table = bs.find(class_="mat-table")
    print(table)