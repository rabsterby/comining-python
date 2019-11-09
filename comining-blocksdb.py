COMINING_URL = "https://api.comining.io/?key="
COMINING_KEY = "X5szT5DjaoXhkuVmGVnMrBU"

import pymongo
import requests
from datetime import datetime
import time

blocklist = {"method":"blocks_list"}
workerslist = {"method":"workers_list"}
mininglist = {"method":"mining_list"}
headers = {'charset': 'utf-8'}

mnnglst, mnglst, mnnlst, mininground = {}, {}, {}, {}
mnnc = ('CLO', 'ELLA', 'ETP', 'MUSIC', 'DBIX', 'PIRL', 'CLO', 'NUKO', 'CLO', 'VIC', 'EXP', 'PGC', 'MOAC', 'AURA', 'MOAC', 'AKA', 'ETP', 'ESN', 'EXP', 'EGEM', 'CLO', 'DOGX', 'EXP', 'ATH', 'CLO', 'NILU', 'MOAC', 'PRKL', 'EXP',  'REOSC', 'TSF', 'ETP',  'SAGE', 'MOAC', 'XERO', 'CLO', 'FUNC')

def RESP(opt):  #Post запрос к серверу
	response = requests.post(COMINING_URL + COMINING_KEY, json=opt, headers=headers)
	return response.json()

def MNNGLIST(): 
	mnnglst = RESP(mininglist)
	mnnglst = mnnglst.get('data')
	
	for j in range(len(mnnglst)):
		mnglst = mnnglst[j]
		r = mnglst.get('mining')
		r = r[-10:]
		#print(r)
		if r == '10G / SOLO':
			mnnlst[mnglst.get('coin')] = mnglst.get('uniq')
	return mnnlst

def WRKRSLIST(): 
	wrckrlst = {}
	wrkrslst = RESP(workerslist)
	wrkrslst = wrkrslst.get('data')
	
	for n in range(len(wrkrslst)):
		wrkrslst = wrkrslst[n]
		wrckrlst['worker'] = wrkrslst.get('name')
		wrckrlst['coin'] = wrkrslst.get('coin')
		wrckrlst['wrkruniq'] = wrkrslst.get('uniq')
		wrckrlst['miningUniq'] = wrkrslst.get('miningUniq')
		wrckrlst['status'] = wrkrslst.get('status')
	return wrckrlst

def CHNGMINING(WORKER_UNIQ, MINING_UNIQ): 
	# изменяем майнинг на другую монету
	chng = {"method": "change_mining", "workers": [ WORKER_UNIQ ], "mining": MINING_UNIQ}
	chngmnng = requests.post(COMINING_URL + COMINING_KEY, json=chng, headers=headers)
	return chngmnng.json	

conn = pymongo.MongoClient("192.168.1.66", 27017)
 
db = conn['comining']
mnblocks = db['mnblocks']
pref = db['pref']

blcklst = RESP(blocklist)
blcklst = list(blcklst.get('data'))

dictccn = pref.find_one({'last': 'block'})
ccn = dictccn.get('count')
cn = dictccn.get('lastbl')

for i in range(len(blcklst)):
	blkNmbr = blcklst[i].get('blockNumber')
	ids = blcklst[i].get('id')
	cnn = blcklst[i].get('coin') #last mined
	
	if  mnblocks.find({"id": ids}).count() == 0:
		print(blcklst[i].get('coin'), blkNmbr, 'new', blcklst[i].get('status'))
		if blcklst[i].get('reward') != None:

			blk = {'id': blcklst[i].get('id'), 'coin': blcklst[i].get('coin'), 'blockNumber': blcklst[i].get('blockNumber'), 'reward': (int(int(blcklst[i].get('reward')) * 0.99)),'created': blcklst[i].get('created')}
			mnblocks.insert(blk)
			if blcklst[i].get('coin') == cn:
				ccn = ccn + 1
			else:
				ccn = 1
			pref.update({'last': 'block'},{'last': 'block', 'lastbl': blcklst[i].get('coin'), 'count': ccn, 'date': blcklst[i].get('created')})
			print(blcklst[i].get('coin'), blkNmbr, 'inserted')

mnnlst = MNNGLIST()		#словарь: 10G Solo
wrckrlst = WRKRSLIST() #словарь: майнеры
cmnc = wrckrlst['coin']
round1 = pref.find_one({'miningcoin': 'miningcoin'})
rc = round1.get('round1')
cmnnc =  mnnc[rc]

countercoin = pref.find_one({'coin': cn}) #словарь: монета, количество блоков для добычи

if wrckrlst['coin'] == cn and countercoin.get('count') <= ccn:
	round1 = pref.find_one({'miningcoin': 'miningcoin'})
	rc = round1.get('round1')
	mnncoin = mnnlst.get(cmnnc)
	WORKER_UNIQ = wrckrlst.get('wrkruniq')
	MINING_UNIQ = mnncoin
	CHNGMINING(WORKER_UNIQ, MINING_UNIQ)
	rc = rc + 1
	if rc >= (len(mnnc)):
		rc =0
	pref.update({'miningcoin': 'miningcoin'},{'miningcoin': 'miningcoin', 'round1': rc})
else:
	print('Nochange',cn, ccn)
