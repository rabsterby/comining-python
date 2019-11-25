COMINING_URL = "https://api.comining.io/?key="
COMINING_KEY = "Your-Comining-Key"

import pymongo
import requests
from datetime import datetime
import time

coinslist = {"method":"coins_list"} #coins list and their profit
coinsreward = {"method":"coins_reward"} #coins reward your acount
blocklist = {"method":"blocks_list"}
mininglist = {"method":"mining_list"}
workershash = {"method":"workers_hashrate"}
workerslist = {"method":"workers_list"}
workers = {"method":"workers_summary"}
headers = {'charset': 'utf-8'}

def RESP(opt):  #Post запрос к серверу
	response = requests.post(COMINING_URL + COMINING_KEY, json=opt, headers=headers)
	return response.json()

cnslst = RESP(coinslist)
cnslst = list(cnslst.get('data'))
cnslst = cnslst

conn = pymongo.MongoClient("192.168.1.66", 27017)
 
db = conn['comining']
blockcoin = db['blockcoin']
pref = db['pref']
coins = db['coins']

for i in range(len(cnslst)):
	profit = cnslst[i].get('profit')
	revusd = profit.get('revenue_usd') / 10
	revusd = float('{:.2f}'.format(revusd))
	revcns = profit.get('coins') / 10
	revcns = float('{:.3f}'.format(revcns))
	cns = {'coin': cnslst[i].get('coin'), 'baseReward': cnslst[i].get('baseReward'),'active': cnslst[i].get('active'), 'coinIconUrl': cnslst[i].get('coinIconUrl'), 'blockTime': cnslst[i].get('blockTime'), 'blockRevenueUsd': cnslst[i].get('blockRevenueUsd'), 'networkDifficulty': cnslst[i].get('networkDifficulty'), 'networkHashrate': cnslst[i].get('networkHashrate'), 'siteUrl': cnslst[i].get('siteUrl'), 'workersHashrate': cnslst[i].get('workersHashrate'), 'revenue_usd': revusd, 'revenue_coins': revcns}

	coins.update({'coin': cnslst[i].get('coin')},{'coin': cnslst[i].get('coin'), 'baseReward': cnslst[i].get('baseReward'),'active': cnslst[i].get('active'), 'coinIconUrl': cnslst[i].get('coinIconUrl'), 'blockTime': cnslst[i].get('blockTime'), 'blockRevenueUsd': cnslst[i].get('blockRevenueUsd'), 'networkDifficulty': cnslst[i].get('networkDifficulty'), 'networkHashrate': cnslst[i].get('networkHashrate'), 'siteUrl': cnslst[i].get('siteUrl'), 'workersHashrate': cnslst[i].get('workersHashrate'), 'revenue_usd': revusd, 'revenue_coins': revcns})
	
	if cnslst[i].get('active') == True:
		cnt = revcns / float(cnslst[i].get('baseReward'))
		cnt = float('{:.2f}'.format(cnt))
		if cnt >= 100:
			cnt = 10
		elif cnt >= 50:
			cnt = 6
		elif cnt >= 40:
			cnt = 5	
		elif cnt >= 30:
			cnt = 4	
		elif cnt >= 20:
			cnt = 3	
		elif cnt >= 10:
			cnt = 2	
		elif cnt >= 1:
			cnt = 1
		elif cnt < 1:
			cnt = 0
		pref.update({'coin': cnslst[i].get('coin')}, {'coin': cnslst[i].get('coin'), 'count': cnt, 'coincounter': 'conter coin'})
