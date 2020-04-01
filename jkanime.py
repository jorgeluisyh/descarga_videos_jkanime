#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import re, time
import glob
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from datetime import datetime
# print os.path.dirname(__file__)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver.exe',options=options)
tryvar = "hi"


#####FUNCIONES GENERALES PARA CUALQUIER URL####
def getcontent(url):
	'''
	funcion para obtener los elementos html de la pagina
	:param url: link url de la pagina
	:return:
	'''
	res = requests.get(url)
	contenido = res.content
	sopa = bs(contenido,'html.parser')
	return sopa

def getWithDriver(url):
	'''
	funcion para obtener los elementos html de la pagina
	usando chromedriver para mejor funcionalidad con paginas complejas
	usar solo en caso de que getcontent no obtenga el resultado esperado
	:param url:
	:return:
	'''
	driver.get(url)
	time.sleep(1)
	sqpage= driver.page_source
	soup = bs(sqpage, 'html.parser')
	return soup

def downloadfile(name,url,path,type):
	'''

	:param name: nombre que tendra el archivo al ser descargado
	:param url: enlace de descarga
	:param path: ruta donde se almacenara el archivo
	:param type: formato del archivo de salida
	:return:
	'''
	name=name+".%s"%type
	r=requests.get(url)
	print "****Connected****"
	outpath = os.path.join(path,name)
	f=open(outpath,'wb');
	print "Downloading.....%s"%name
	for chunk in r.iter_content(chunk_size=255):
		if chunk: # filter out keep-alive new chunks
			f.write(chunk)
	print "Done"
	f.close()



##### FUNCIONES ESPECIFICAS PARA EL SCRAPPING DE JKANIME#####
def getnumofcaps(url):
	'''
	obtiene el numero de capitulos del enlace jkanime
	:param url: url de la pagina de animes
	:return:
	'''
	sopa = getcontent(url)
	listx = sopa.find_all('span','info-value')
	numcaps=0
	for x in listx:
		y= x.get_text()
		if re.match('^[0-9]{1,2}$',y):
			numcaps = int(y)
	print numcaps
	return numcaps

def getExistentes(path):
	'''
	obtiene el numero de capitulos ya existentes en la carpeta
	:param path:
	:return:
	'''
	files = [int(os.path.basename(f).split('_')[1].split('.')[0]) for f in glob.glob(path + "**/*.mp4")]
	return files

def getvideos(numcaps,path,url):
	'''
	funcion que descarga los videos a la carpeta destino
	:param numcaps: numero de capitulos existentes en el enlace
	:param path: ruta de salida para los videos
	:param url: url del anime
	:return:
	'''
	animename = url.split(r'.net/')[1][:-1]
	existentes = getExistentes(path)
	videolinks =[]
	for num in range(numcaps):
		if num+1 not in existentes:
			tempurl = url+ str(num+1)+ r'/'
			soup = getWithDriver(tempurl)
			iframexx = soup.find_all("iframe","player_conte")
			iframe_page = iframexx[0].get('src')
			soup1 = getWithDriver(iframe_page)
			nn=soup1.find_all('source')
			videolink = nn[0].get('src')
			videolinks.append(videolink)

			namefile = animename+ "_"+ str(num+1).zfill(len(str(numcaps)))
			downloadfile(namefile,videolink,path,'mp4')
	print "finalizado"
	


def mainjk(url,path):
	animename = url.split(r'.net/')[1][:-1]
	numcaps = getnumofcaps(url)
	getvideos(numcaps,path,url)


if __name__ == '__main__':
	url = r'https://jkanime.net/shingeki-no-kyojin/'
	path1 = r'D:\animes\attack_on_tittan\snk_t1'
	mainjk(url,path1)
	driver.quit()
	print "end"


