import requests
from bs4 import BeautifulSoup
req = requests.get("https://steamcommunity.com/sharedfiles/filedetails/?id=1125571106")
soup = BeautifulSoup(req.text, 'lxml')
val = soup.find('div', {'class':"workshopItemTitle"}).get_text()

print(val)

