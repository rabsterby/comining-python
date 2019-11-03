COMINING_URL = "https://api.comining.io/?key="
COMINING_KEY = "X5szT5DjaoXhkuVmGVnMrBU"
WORKER_UNIQ = ""
MINING_UNIQ = ""

import pymongo
import requests
from datetime import datetime
import time

blocklist = {"method":"blocks_list"}
headers = {'charset': 'utf-8'}

def RESP(opt):  #Post запрос к серверу
	response = requests.post(COMINING_URL + COMINING_KEY, json=opt, headers=headers)
	return response.json()
 
conn = pymongo.MongoClient("192.168.1.66", 27017)
 
db = conn['comining']
coll = db['mnblocks']

blcklst = RESP(blocklist)
blcklst = list(blcklst.get('data'))

for i in range(len(blcklst)):
	blkNmbr = blcklst[i].get('blockNumber')
	ids = blcklst[i].get('id')
	if  coll.find({"id": ids}).count() == 0:
		#print(blcklst[i].get('coin'), blkNmbr, 'new', blcklst[i].get('status'))
				
		if blcklst[i].get('reward') != None:
			
			blk = {'id': blcklst[i].get('id'), 'coin': blcklst[i].get('coin'), 'blockNumber': blcklst[i].get('blockNumber'), 'reward': (int(int(blcklst[i].get('reward')) * 0.99)),'created': blcklst[i].get('created')}
			#print(blk)
			coll.insert(blk)
			#print(blcklst[i].get('coin'), blkNmbr, 'inserted')

			
