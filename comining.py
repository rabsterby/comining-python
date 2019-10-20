HTML_SAVE_PATH = "/var/www/html/comining_"

COMINING_URL = "https://api.comining.io/?key="
COMINING_KEY = "X5szT5DjaoXhkuVmGVnMrBU"

# import flask
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
	return response.json()

def saveHTML(list, filePath):
	f = open(filePath+list=".html",'w', encoding='utf-8')
	html =  """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ru-RU">
<head>
<meta charset="utf-8">
<meta content="width=1280" name="viewport">
<title>Майнинг</title>
</head> 
  <div class="shadow">
    <a href="/index.html" <button class="torrentbutton" style="">на Главную</button></a>
    <div class="block1" style="background-color: #f2f2f2;">"""
	descriptionTemplate = """
                <tr>
                  <td class="type">{}</td>
                  <td>
                    <div style="position: relative">
                        {}
                    </div>
                  </td>
                </tr>"""
	buttonsTemplate = """          <button class="torrentbutton" style="" onclick="location.href='{}'">{}</button>"""
	mainTemplate = """      <div class="block2" data-releaseDate="{}" data-torrentDate="{}" date-rating="{}">
        <div class="photoInfoTable">
          <div class="headerFilm">
            <h1 class="moviename" itemprop="name">{}</h1>
            <span itemprop="alternativeHeadline" style="{}">{}</span>
          </div>
          <div class="photoBlock">
            <div class="film-img-box">
              <div class="film-rating" style="background-color: {};">{}</div> <!-- #3bb33b > 7 #aaa; -->
              <img src="{}" alt="{}" itemprop="image" width="360"></img>
            </div>
          </div>
          <div class="infoTable">
            <table class="info">
              <tbody>
{}
              </tbody>
            </table>
          </div>
        </div>
        <div class="movie-buttons-container">
{}
        </div>
      </div>
"""
	descriptionBlock = ""
	descriptionBlock += descriptionTemplate.format("Монета", wrkrs['coinName'])
	descriptionBlock += descriptionTemplate.format("Хэшрейт", wrkrs['workersHashrate'])
	descriptionBlock += descriptionTemplate.format("Майнеры", wrkrs['workers'])
	descriptionBlock += descriptionTemplate.format("Offline", wrkrs['workersOffline'])
#	descriptionBlock += descriptionTemplate.format("Имя майнера", wrkrslst['name'])
#		if len(movie["ratingAgeLimits"]) > 0:
#				descriptionBlock += descriptionTemplate.format("возраст", "от 6 лет")
#		descriptionBlock += descriptionTemplate.format("продолжительность", movie["filmLength"])
#		if len(movie["ratingKP"]) > 0:
#			rKP = movie["ratingKP"]
#		else:
#			rKP = "отсутствует"
#		descriptionBlock += descriptionTemplate.format("рейтинг КиноПоиск", "<a href=\"{}\" style=\"text-decoration: underline; color:black\">{}</a>".format(movie["webURL"], rKP))
#		descriptionBlock += descriptionTemplate.format("торрент-релиз", "<a href=\"{}\" style=\"text-decoration: underline; color:black\">{}</a>".format(RUTOR_BASE_URL + movie["filmID"], movie["torrentsDate"].strftime("%d.%m.%Y")))
#		descriptionBlock += descriptionTemplate.format("описание", movie["description"])
	buttonsBlock = "" 
#				buttonsBlock += buttonsTemplate.format(torrent["magnet"], torrent["type"])
#				buttonsBlock += buttonsTemplate.format(torrent["link"], torrent["type"])
	ratingColor = "#aaa"
#		if movie["ratingFloat"] >= 7:
#			ratingColor = "#3bb33b"
#		elif movie["ratingFloat"] < 5.5:
#			ratingColor = "#b43c3c"
	html += mainTemplate.format(wrkrs['coin'], wrkrs['coinName'], wrkrs['workersHashrate'], wrkrs['workers'], wrkrs['workersOffline'], wrkrs['coinName'], ratingColor, wrkrs['coin'], wrkrs['coinIconUrl'], wrkrs['coin'], descriptionBlock, buttonsBlock)
		
	html += """    </div>
  </div>
</body>
</html>"""
	f.write(html)
	f.close()
	return 


def main():
	
	wrkrs = RESP(workers)
	wrkrs = list(wrkrs.get('data'))
	wrkrs = wrkrs[0]

	wrkrslst = RESP(workerslist)
	wrkrslst = list(wrkrslst.get('data'))
	wrkrslst = wrkrslst[0]
	print(wrkrslst['name'])
	
	blcklst = RESP(blocklist)
	blcklst = list(blcklst.get('data'))
	print(blcklst[0])

	"""
	wrkrshsh = RESP(workershash)
	wrkrshsh = list(wrkrshsh.get('data'))
	print(wrkrshsh)
	
	mnnglst = RESP(mininglist)
	mnnglst = list(mnnglst.get('data'))
	mnnglst = mnnglst[0]
	print(mnnglst[0])
	print(mnnglst[1])
	print(mnnglst[2])
	print(mnnglst[3])
	print(mnnglst[4])
	print(mnnglst[5])
	
	cnslst = RESP(coinslist)
	cnslst = list(cnslst.get('data'))
	cnslst = cnslst[0]
	#print(cnslst)
	
	cnsrwrd = RESP(coinsreward)
	cnsrwrd = list(cnsrwrd.get('data'))
	#print(cnsrwrd)
	"""
	saveHTML(wrkrs, HTML_SAVE_PATH)
	saveHTML(wrkrslst, HTML_SAVE_PATH)
	saveHTML(blcklst, HTML_SAVE_PATH)
	
main()
