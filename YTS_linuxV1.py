from bs4 import BeautifulSoup
import urllib.request
import os
from datetime import datetime
import glob
from threading import Timer

print ('==============YTS============ started at:' + str(datetime.now().time()))
search = input("Search for:")
search2 = search.replace(" ","+")
if input("Download?") == "y":
    dlbool = True
else:
    dlbool = False

if input("Convert to audio?") == "y":
    mp3bool = True
else:
    mp3bool = False

max_dls = input("Max Downloads per Page:")	#20 is max
pageNo = input("Max Pages:")
startTime = input("Delay in minutes:") #delay before scraper starts

#insert current files into array for checking
#for filenames in os.walk('/home/dragonite/Videos/YTS_files'):
#	currentfiles.append(filenames)
#glob???
#youtube-dl currently checks files in the output directory for duplicates already

def youtubeScraper():
	print ('==============Scraping started at:' + str(datetime.now().time()))
	for page in range(1,int(pageNo)+1):
		print('###########Page ' + str(page) +'#############')
		url = "https://www.youtube.com/results?search_query=" + search2 +"&page=" + str(page) +"&utm_source=opensearch"
		print('url page:' + url)
		content = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(content, 'lxml') #lxml is the default HTML parser can check for new ones
		i =1	
		for link in soup.find_all('a'):
			a = link.get('href')	
			if (a[:6] == '/watch') and i <= int(max_dls) and link.get('title'):# and os.path.isfile( link.get('title')):
				print ('==============Link ' + str(i) +'============ ' + str(datetime.now().time()))
				i +=1
				print (link.get('title'))

				
				#print(link.string)
				page = 'https://www.youtube.com' + a
				#title = str(link.string, encoding='utf-8', errors = 'ignore'))
				
				#check if file already exists in library
				#if (dir.findname(link.get('title'))):
				#	next link

				#-r 50K download rate in bytes
				#-v --verbose -q quiet
				#-x extract audio
				#--audio-format FORMAT Specify audio format: "best", "aac", "vorbis", "mp3", "m4a", "opus", or "wav"; "best" by default
				#--max-filesize SIZE Do not download any videos larger than SIZE (e.g. 50k or 44.6m)
				#--yes-playlist Download the playlist, if the URL refers to a video and a playlist.

				if mp3bool:
					command = 'youtube-dl -x -q -o "./%(title)s.%(ext)s" ' + str(page) 
				else:
					command = 'youtube-dl -q -o "./%(title)s.%(ext)s" ' + str(page) 

				#command = 'youtube-dl -q --yes-playlist ' + str(page)

				print(command)
				#os.system('cd C:\Python\Python35-32\Lib\site-packages & ' + command) #for windows
				if dlbool:
				    os.system(command) #for linux
	print('++++++++finished search result: ' + search+ ' ++++++++')
	return

#Incorporate a timer for a certain time or add a delay using startTime
print ('It is currently:' + str(datetime.now().time()))
print ('waiting ' + str(float(startTime)) + ' minutes' )
t = Timer(float(startTime)*60,youtubeScraper).start()