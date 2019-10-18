HTML_SAVE_PATH = "/var/www/html/comining_"

COMINING_URL = "https://api.comining.io/?key="
COMINING_KEY = "X5szT5DjaoXhkuVmGVnMrBU"

# import flask
import hashlib
import datetime
import urllib.request
from urllib.parse import urljoin 
import time
import gzip
import json
import html
import re
import operator
import os
import binascii
import requests

coinsreward = {"method":"coins_reward"}
mininglist = {"method":"mining_list"}
workers = {"method":"workers_summary"}
workerslist = {"method":"workers_list"}
blocklist = {"method":"blocks_list"}
coinslist = {"method":"coins_list"}
headers = {'charset': 'utf-8'}


def RESP(opt):  #Post запрос к серверу
	response = requests.post(COMINING_URL + COMINING_KEY, json=opt, headers=headers)
	return response.json()


def main():
	
	#wrkrs = RESP(workers)
	#wrkrs = list(wrkrs.get('data'))
	#wrkrs = wrkrs[0]
	#print(wrkrs)

	wrkrslst = RESP(workerslist)
	wrkrslst = list(wrkrslst.get('data'))
	wrkrslst = wrkrslst[0]
	print(wrkrslst)
	
	blcklst = RESP(blocklist)
	blcklst = list(blcklst.get('data'))
	print(blcklst[0])
	
	cnslst = RESP(coinslist)
	cnslst = list(cnslst.get('data'))
	cnslst = cnslst
	print(type(cnslst[1]))
	
	"""
	cnslst = RESP(coinslist)
	cnslst = list(cnslst.get('data'))
	cnslst = cnslst[0]
	#print(cnslst)
	
	saveHTML(wrkrs, HTML_SAVE_PATH)
	saveHTML(wrkrslst, HTML_SAVE_PATH)
	saveHTML(blcklst, HTML_SAVE_PATH)
	
	"""
main()


