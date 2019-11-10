COMINING_URL = "https://api.comining.io/?key="
COMINING_KEY = "Your-Comining-Key"

import pymongo
import requests
from datetime import datetime
import time

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
	cns = {'coin': cnslst[i].get('coin'), 'baseReward': cnslst[i].get('baseReward'),'active': cnslst[i].get('active'), 'coinIconUrl': cnslst[i].get('coinIconUrl'), 'blockTime': cnslst[i].get('blockTime'), 'profit': cnslst[i].get('profit'), 'blockRevenueUsd': cnslst[i].get('blockRevenueUsd'), 'networkDifficulty': cnslst[i].get('networkDifficulty'), 'networkHashrate': cnslst[i].get('networkHashrate'), 'siteUrl': cnslst[i].get('siteUrl'), 'workers': cnslst[i].get('workers'), 'workersHashrate': cnslst[i].get('workersHashrate')}
	coins.insert(cns)	
	
"""
for i in range(len(blcklst)):
	cn = 0
	blkNmbr = blcklst[i].get('blockNumber')
	ids = blcklst[i].get('id')
	cnn = blcklst[i].get('coin') + 'cn'
	
	#print('Need_add', cnn)
	#pref.update({cnn : cn})
	#pref.update({cnn : 0})
	#cn = pref.find({cnn :})
	
	if  mnblocks.find({"id": ids}).count() == 0:
		print(blcklst[i].get('coin'), blkNmbr, 'new', blcklst[i].get('status'))
		if blcklst[i].get('reward') != None:
			dictccn = pref.find_one({'last': 'block'})
			ccn = dictccn.get('count')
			cn = dictccn.get('lastbl')
			blk = {'id': blcklst[i].get('id'), 'coin': blcklst[i].get('coin'), 'blockNumber': blcklst[i].get('blockNumber'), 'reward': (int(int(blcklst[i].get('reward')) * 0.99)),'created': blcklst[i].get('created')}
			mnblocks.insert(blk)
			if blcklst[i].get('coin') == cn:
				ccn = ccn + 1
			else:
				ccn = 1
			pref.update({'last': 'block'},{'last': 'block', 'lastbl': blcklst[i].get('coin'), 'count': ccn, 'date': blcklst[i].get('created')})
			print(blcklst[i].get('coin'), blkNmbr, 'inserted')
	"""
