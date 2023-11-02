import os

from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import glob
from threading import Timer
import re
from yt_dlp import YoutubeDL

#insert current files into array for checking
#for filenames in os.walk('/home/dragonite/Videos/YTS_files'):
#	currentfiles.append(filenames)
#glob???
#youtube-dl currently checks files in the output directory for duplicates already

def link_add(i: int, page: int, title: tuple, scrapped_list: list ):
	assert isinstance(title, tuple)

	if dltype == "1":

		print(">>>>Link"+str(i+1)+":",
							title[1],'|', #Video Title
							title[3],'|', #Publish Date
							title[5],'|') #Video Duration
		scrapped_list.append([page,i+1,'https://www.youtube.com/watch?v=' + title[7],title[1]])
	else:
		print(">>>>Link"+str(i+1)+":",
							title[1],'|', #Video Title
							title[3],'|', #Video Count
							title[5].replace("\\u0026","&"),'|')
		scrapped_list.append([page,i+1,'https://www.youtube.com/watch?v=' + title[5].replace("\\u0026","&"),title[1]])

def generate_scrapped_list(timeRequest):
	scrapped_list = []
	print ('==============Scraping started at:' + str(datetime.now().time()))	
	for page in range(1,int(pageNo)+1):
		print('###########Page ' + str(page) +'#############' + str(datetime.now().time()))
		url = "https://www.youtube.com/results?search_query=" + search2 + "&page=" + str(page) + mod #"&utm_source=opensearch"+ #youtube website doesn't use pagination anymore, how to query through more results?
		print('url page:' + url)
		content = urllib.request.urlopen(url).read()[150000:-35000]
		soup = BeautifulSoup(content, 'lxml') #lxml is the default HTML parser can check for new ones		

		#update for youtube new source
		#beautiful soup used to extract the tagged section which includes the youtube url link sub string watch?v= within the javascript tags
		for link in soup.find_all(string=re.compile('watch\\?v=')):
			
			#use regex findall to return list of groups specified within ( ) matching expression. first group is for title tags, second for title text, third for other code until url, fourth for url.
			rex_1 = '(\"title.+?)(?<=text\"\:\")(.+?)(?=\")(.+?)(?<=TimeText\"\:{\"simpleText\"\:\")(.+?)(?=\")(.+?)(?<=\"}},\"simpleText\"\:\")(.+?)(?=\")(.+?)(?<=watch\?v=)(.+?)(?=\")'
			#0 '(\"title.+?)(?<=text\"\:\")
			#1 (.+?)(?=\") title
			#2 (.+?)(?<=TimeText\"\:{\"simpleText\"\:\")
			#3 (.+?)(?=\") publish date
			#4 (.+?)(?<=seconds\"}},\"simpleText\"\:\")
			#5 (.+?)(?=\") time
			#6 (.+?)(?<=watch\?v=)
			#7 (.+?)(?=\")' link

			rex_2 = '(,\"title.+?)(?<=Text\"\:\")(.+?)(?=\")(.+?)(?<=videoCount\"\:\")(.+?)(?=\")(.+?)(?<=watch\?v=)(.+?)(?=\")'
			#0 '(\"title.+?)(?<=text\"\:\")
			#1 (.+?)(?=\") *title
			#2 (.+?)(?<=videoCount\"\:\")
			#3 (.+?)(?=\") *video count
			#4 (.+?)(?<=watch\?v=)
			#5 (.+?)(?=\") *link

			if playbool or playboolaudio:
				rex = rex_2
			else:
				rex = rex_1
			
			for i, title in enumerate(re.findall(rex, link)):

				#if a duration was requested
				if timeRequest != "":
					if int(timeRequest) == 1 and int(title[5][0]) < 2 and len(title[5])<5 and title[1] not in scrapped_list:
						link_add(i,title,scrapped_list)						

					if int(timeRequest) == 2 and int(title[5][0]) > 2 and len(title[5])<5 and title[1] not in [x[3] for x in scrapped_list]:
						link_add(i,title,scrapped_list)

					if int(timeRequest) == 3 and len(title[5])>=5 and title[1] not in [x[3] for x in scrapped_list]:
						link_add(i,title,scrapped_list)

				elif title[1] not in [x[3] for x in scrapped_list]:					
					link_add(i,page,title,scrapped_list)	
						
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

def youtubeDownloader(scrapped_list, selection_list, search):
	if input("Download?") == "y" or "Y":
		dlbool = True
	
	if dlbool:
		print ('==============Downloading started at:' + str(datetime.now().time()))	

		for link in scrapped_list:
			if [link[0],link[1]] in selection_list:
				print ('[Page ' + str(link[0]) +'] - ' + '[Link ' + str(link[1]) +'] - ' + str(link[3]))

				#--audio-format FORMAT Specify audio format: "best", "aac", "vorbis", "mp3", "m4a", "opus", or "wav"; "best" by default

				if mp3bool:
					command = 'yt-dlp --audio-quality 10 --extract-audio -o "./%(title)s.%(ext)s" "' + str(link[2])  + '"' 
				elif playbool:
					command = 'yt-dlp -S "res:480" --console-title --yes-playlist -o "./' + search + '/%(playlist_index)s - %(title)s.%(ext)s" "' + str(link[2])  + '"'					
				elif playboolaudio:  
					command = 'yt-dlp --yes-playlist --audio-quality 10 --extract-audio -o "./' + search + '/%(playlist_index)s - %(title)s.%(ext)s" "' + str(link[2])  + '"'
				else:
					command = 'yt-dlp --console-title -o "./' + search + '/%(title)s.%(ext)s" "' + str(link[2])  + '"'
				
				if dlbool: #check if want to download
					#YoutubeDL().download(str(link[2]))
					#print(f"command is {command}")
					os.system(command) #for linux

		print('++++++++finished search result: ' + search + ' ++++++++')
	



#=========MAIN Function=============

#Incorporate a timer for a certain time or add a delay using startTime
if __name__ == '__main__':
	print ('==============YTS============ started at:' + str(datetime.now().time()))
	search = input("Search for:")
	search2 = search.replace(" ","+")

	mod = ""
	timeRequest = ""
	dlbool = False
	mp3bool = False
	playbool = False
	playboolaudio = False

	dltype = input("1:audioconvert, 2:playlist, 3:audioconvert playlist")

	if dltype== "1":
	    mp3bool = True
	if dltype== "2":
	    playbool = True
	    mod = "&sp=EgIQAw%253D%253D"
	if dltype== "3":
	    playboolaudio = True	    
	    mod = "&sp=EgIQAw%253D%253D"

	if dltype == "1":

		timeRequest = input("1:short, 2:long, 3:super long")

		if timeRequest == "1":
			mod = "&sp=EgQQARgB"
		if timeRequest == "2":
			mod = "&sp=EgQQARgD"
		if timeRequest == "3":
			mod = "&sp=EgQQARgC"

	

	
	
	    
	max_dls = 40#input("Max Downloads per Page:")	#20 is max
	pageNo = input("Max Pages:")
	if pageNo == "":
		pageNo = 1
	startTime = 0#input("Delay in minutes:") #delay before scraper starts

	scrapped_list = generate_scrapped_list(timeRequest) 

	selection_list = generate_selection_list()

	#os.mkdir("./" + search2)

	main_fun = lambda: youtubeDownloader(scrapped_list, selection_list, search)

	print ('It is currently:' + str(datetime.now().time()))
	print ('waiting ' + str(float(startTime)) + ' minutes' )
	t = Timer(float(startTime)*60, main_fun ).start()
