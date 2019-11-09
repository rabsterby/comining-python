COMINING_URL = "https://api.comining.io/?key="
COMINING_KEY = "X5szT5DjaoXhkuVmGVnMrBU"

import pymongo
import requests
from datetime import datetime
import time
import urllib

image_url ="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
 
coinsreward = {"method":"coins_reward"}
mininglist = {"method":"mining_list"}
workers = {"method":"workers_summary"}
workerslist = {"method":"workers_list"}
coinslist = {"method":"coins_list"}

headers = {'charset': 'utf-8'}

def RESP(opt):  #Post запрос к серверу
	response = requests.post(COMINING_URL + COMINING_KEY, json=opt, headers=headers)
	return response.json()
 
conn = pymongo.MongoClient("192.168.1.66", 27017)
 
db = conn['comining']
mnblocks = db['mnblocks']
blocks = db['blocks']
pref = db['pref']
coins = db['coins']

coinslst = RESP(coinslist)
cnslst = list(coinslst.get('data'))

for i in range(len(cnslst)):
	image_url = cnslst[i].get('coinIconUrl')
	
	coin = cnslst[i].get('coin').lower() + '.png'
 
	r = requests.get(image_url)
 
	# open method to open a file on your system and write the contents
	with open(coin, "wb") as code:
		code.write(r.content)


