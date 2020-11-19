import os

from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
#import glob
from threading import Timer

#insert current files into array for checking
#for filenames in os.walk('/home/dragonite/Videos/YTS_files'):
#	currentfiles.append(filenames)
#glob???
#youtube-dl currently checks files in the output directory for duplicates already

def generate_scrapped_list():
	scrapped_list = []
	print ('==============Scraping started at:' + str(datetime.now().time()))	
	for page in range(1,int(pageNo)+1):
		print('###########Page ' + str(page) +'#############' + str(datetime.now().time()))
		url = "https://www.youtube.com/results?search_query=" + search2 +"&page=" + str(page) +"&utm_source=opensearch"
		print('url page:' + url)
		content = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(content, 'lxml') #lxml is the default HTML parser can check for new ones		

		i =1	#link number
		for link in soup.find_all('a'):
			a = link.get('href')	
			if (a[:6] == '/watch') and i <= int(max_dls) and link.get('title'):# and os.path.isfile( link.get('title')):
				try:
				    print ('[Link ' + str(i) +'] - ' + (link.get('title')))
				except UnicodeEncodeError:
					   print ('[Link ' + str(i) +'] - UnicodeEncodeError')
				scrapped_list.append([page,i,'https://www.youtube.com' + a,(link.get('title'))])
				i +=1
	print('++++++++finished search result: ' + search+ ' ++++++++')
	return scrapped_list

def generate_selection_list():
	selection_list = []

	for page in range(1,int(pageNo)+1):
		dl_input = [int(x) for x in input("Links for Page {} separated by spaces. e.g. 1 5 9 10: ".format(page)).split()]
		print("Page: {} Links: {}".format(page,dl_input))
		for link in dl_input:
			selection_list.append([page,link])

	print(selection_list)
	return selection_list

def youtubeDownloader(scrapped_list, selection_list):
	if input("Download?") == "y" or "Y":
		dlbool = True
	
	if dlbool:
		print ('==============Downloading started at:' + str(datetime.now().time()))	

		for link in scrapped_list:
			if [link[0],link[1]] in selection_list:
				print ('[Page ' + str(link[0]) +'] - ' + '[Link ' + str(link[1]) +'] - ' + str(link[3]))

				#--audio-format FORMAT Specify audio format: "best", "aac", "vorbis", "mp3", "m4a", "opus", or "wav"; "best" by default

				if mp3bool:
					command = 'youtube-dl -x -q --newline -o "./%(title)s.%(ext)s" "' + str(link[2])  + '"' 
				elif playbool:
					command = 'youtube-dl --console-title --yes-playlist -q --newline "' + str(link[2])  + '"'
				elif playboolaudio:
					command = 'youtube-dl --yes-playlist -f 133 -q --newline -x --verbose "' + str(link[2])  + '"'
				else:
					command = 'youtube-dl -q --console-title -o "./%(title)s.%(ext)s" "' + str(link[2])  + '"'

				#command = 'youtube-dl -q --yes-playlist ' + str(page)

				#print(command)
				#print(dlbool)
				#os.system('cd C:\Python\Python35-32\Lib\site-packages & ' + command) #for windows
				if dlbool: #check if want to download
					os.system(command) #for linux

		print('++++++++finished search result: ' + search+ ' ++++++++')
	



#=========MAIN Function=============

#Incorporate a timer for a certain time or add a delay using startTime
if __name__ == '__main__':
	print ('==============YTS============ started at:' + str(datetime.now().time()))
	search = input("Search for:")
	search2 = search.replace(" ","+")    
	dltype = input("1:audioconvert, 2:playlist, 3:audio playlist")

	dlbool = False
	mp3bool = False
	playbool = False
	playboolaudio = False

	if dltype== "1":
	    mp3bool = True
	if dltype== "2":
	    playbool = True
	if dltype== "3":
	    playboolaudio = True
	    
	max_dls = 20#input("Max Downloads per Page:")	#20 is max
	pageNo = input("Max Pages:")
	startTime = 0#input("Delay in minutes:") #delay before scraper starts

	scrapped_list = generate_scrapped_list() 

	selection_list = generate_selection_list()

	main_fun = lambda: youtubeDownloader(scrapped_list, selection_list)

	print ('It is currently:' + str(datetime.now().time()))
	print ('waiting ' + str(float(startTime)) + ' minutes' )
	t = Timer(float(startTime)*60, main_fun ).start()
