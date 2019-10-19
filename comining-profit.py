HTML_SAVE_PATH = "/var/www/html/comining_"

COMINING_URL = "https://api.comining.io/?key="
COMINING_KEY = "X5szT5DjaoXhkuVmGVnMrBU"
WORKER_UNIQ = ""
MINING_UNIQ = ""

# import flask
#import hashlib
from datetime import datetime
import time
import urllib.request
from urllib.parse import urljoin 
import gzip
import json
import html
import re
import operator
import os
import binascii
import requests
from operator import itemgetter

coinsreward = {"method":"coins_reward"}
mininglist = {"method":"mining_list"}
workers = {"method":"workers_summary"}
workerslist = {"method":"workers_list"}
blocklist = {"method":"blocks_list"}
coinslist = {"method":"coins_list"}
changemining = {"method":"change_mining", "workers": WORKER_UNIQ, "mining": MINING_UNIQ}
headers = {'charset': 'utf-8'}

mnnlst = {}
mnnglst = {}


def RESP(opt):  #Post запрос к серверу
	response = requests.post(COMINING_URL + COMINING_KEY, json=opt, headers=headers)
	return response.json()

def rvnd():
	# делаем словарь расчетного профита 	Coin (id, blks/day, usd/day)
	rvd = {}
	cnslst = RESP(coinslist)
	cnslst = list(cnslst.get('data'))
	cnslst = cnslst
	for i in range(len(cnslst)):
		if cnslst[i].get('active') == True:
			nd = int(cnslst[i].get('networkDifficulty')) / 1000000000000
			pr = cnslst[i].get('profit')
			rv =  float(pr.get('coins') / 10 / float(cnslst[i].get('baseReward')))
			if rv > 0.5:	
				if rv > 10:
					rv = int(rv)
					rvd[cnslst[i].get('coin')] = int(cnslst[i].get('id')), rv, float(pr.get('revenue_usd') / 10)
					
				else:
					rvd[cnslst[i].get('coin')] = int(cnslst[i].get('id')), rv, float(pr.get('revenue_usd') / 10)
	return rvd

def blckslist(): # делаем словарь добытых блоков	Coin (blk)
	blks = {}
	chngmnng = 0
	blcklst = RESP(blocklist)
	blcklst = list(blcklst.get('data'))
	wrkrlst = wrkrslist()
	crntmnng = wrkrlst.get('coin')
	#print(blcklst)
	for l in range(len(blcklst)):
		blk = blcklst[l]
		dt = str(blk.get('created')) 
		dtm = str(datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S"))
		dtm = ' ' + dtm[5:10]
		#rwrd = int(blk.get('reward')) / 100000000
		# = int(cnslst[l].get('id')), rv, float(pr.get('revenue_usd') / 10)
		#if blks.get
		blks[blk.get('coin') + dtm] = blk.get('miningUniq'), 
		#print(blk.get('coin')+str(blk.get('created')), dtm, blk.get('reward'), blk.get('miningUniq'))
	blky = list(blks.keys())
	print(crntmnng + ' ' + crntDt[:5])
	for g in range(len(blky)):
		if blky[g] == crntmnng + ' ' + crntDt[:5]:
			chngmnng = 1
	return blks, chngmnng
	
def chngmining(WORKER_UNIQ, MINING_UNIQ): 
	# изменяем майнинг на другую монету
	chng = {"method": "change_mining", "workers": [ WORKER_UNIQ ], "mining": MINING_UNIQ}
	chngmnng = requests.post(COMINING_URL + COMINING_KEY, json=chng, headers=headers)
	print(chng)
	print(chngmnng.json)
	return chngmnng.json

def mnnglist(): 
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

def wrkrslist(): 
	wrckrlst = {}
	wrkrslst = RESP(workerslist)
	wrkrslst = wrkrslst.get('data')
	
	for n in range(len(wrkrslst)):
		wrkrslst = wrkrslst[n]
		#if wrkrslst.get('status') == True:
		wrckrlst['worker'] = wrkrslst.get('name')
		wrckrlst['coin'] = wrkrslst.get('coin')
		wrckrlst['wrkruniq'] = wrkrslst.get('uniq')
		wrckrlst['mnnguniq'] = wrkrslst.get('miningUniq')
	return wrckrlst

WORKER_UNIQ = ""
MINING_UNIQ = ""
crntDt = str(datetime.today().strftime("%m-%d %H:%M"))
#wrkrs = RESP(workers)
#wrkrs = list(wrkrs.get('data'))
#wrkrs = wrkrs[0]

blks = blckslist()
chngmnng = blks[1]
blks = blks[0]
wrkrlst = wrkrslist()
crntmnng = wrkrlst.get('coin')
mnnglst = mnnglist()
rvn = rvnd()
mn = crntmnng + ' ' + crntDt
mn = mn[0:-6]
#for t in range(blks):
bl = blks.get(mn)	
if crntmnng == 0:
	rvn = rvnd()
mnncoin = mnnlst.get('ETP')
WORKER_UNIQ = wrkrlst.get('wrkruniq')
MINING_UNIQ = mnncoin
print(crntDt)
#print(blks)
dt = crntDt[:4]
#if dt == 
#print(blks)
#chngmining(WORKER_UNIQ, MINING_UNIQ)
#print(wrkrlst)
#print(rvn)



"""
N = (t*R*H)/(D*2^32)
где:
N - доход в монетах
t - период майнинга в секундах (например, сутки = 86400)
R - награда за блок в монетах
H - хэшрейт в секунду (например, 1ГХш = 1000000000)
D - сложность
"""
	



