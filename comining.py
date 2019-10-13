HTML_SAVE_PATH = "/var/www/html/comining.html"

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

coinslist = {"method":"coins_list"}
coinsreward = {"method":"coins_reward"}
blocklist = {"method":"blocks_list"}
mininglist = {"method":"mining_list"}
workershash = {"method":"workers_hashrate"}
workerslist = {"method":"workers_list"}
workers = {"method":"workers_summary"}
headers = {'charset': 'utf-8'}

def RESP(opt):  #Post запрос к серверу
	response = requests.post(COMINING_URL + COMINING_KEY, json=opt, headers=headers)
	print(response.status_code)
	return response.json()

wrkrs = RESP(workers)
x = list(wrkrs.get('data'))
y = x[0]

workersHashrate = y['workersHashrate']
coinName = y['coinName']
