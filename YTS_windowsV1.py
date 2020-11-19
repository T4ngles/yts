from bs4 import BeautifulSoup
import urllib.request
import os

search = input("Search for:")
search2 = search.replace(" ","+")
max_dls = input("Max Downloads per Page:")
pageNo = input("Max Pages:")

for page in range(1,int(pageNo)+1):
	print('###########Page ' + str(page) +'#############')
	url = "https://www.youtube.com/results?search_query=" + search2 +"&page=" + str(page) +"&utm_source=opensearch"
	print('url page:' + url)
	content = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(content, 'lxml') #lxml is the default HTML parser can check for new ones
	i =1	
	for link in soup.find_all('a'):
		a = link.get('href')	
		if (a[:6] == '/watch') and i <= int(max_dls) and link.get('title'):
			print ('==============Link ' + str(i) +'============')
			i +=1
			print(link.get('title'))
			print (a)
			page = 'https://www.youtube.com/' + a
			#title = str(link.string, encoding='utf-8', errors = 'ignore'))
			command = 'youtube-dl -o "F:/YTS_files/%(title)s.%(ext)s" ' + str(page)
			print(command)
			#os.system('cd C:\Python\Python35-32\Lib\site-packages & ' + command)

