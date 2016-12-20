#import the library used to query a website
import urllib2
from bs4 import BeautifulSoup as BS
import urllib
import csv,os,time
from multiprocessing import Pool

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

artists = {}
#specify the url
# wiki = "http://mymp3singer.net/files_by_artist/1221/Ankit+Tiwari/download/"
# wiki ="http://mymp3singer.net/files_by_artist/77/A+R+Rahman/new2old/"
# wiki = "http://mymp3singer.net/files_by_artist/87/Atif+Aslam/new2old/"
# wiki = "http://mymp3singer.net/files_by_artist/495/Armaan+Malik/new2old/"
wiki = "http://mymp3singer.net/filelist/3924/special_songs/new2old/"
wikiDownload = "http://mymp3singer.net/files/download/id/"

counter = 0

def fileDownload(current_path, song, song_name):
	print(song)
	if not os.path.isfile(os.path.join(current_path,song_name)):
		urllib.urlretrieve(song, os.path.join(current_path,song_name))			
		print (song_name+" Dowloaded")
	else : 
		print (song_name+" Already Dowloaded")				

def getSonglinks(title, url):
	# c.writerow(title)
	if not os.path.exists(title):
		os.makedirs(title)		
	current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), title)
	req = urllib2.Request(url, headers=hdr)       
	#Query the website and return the html to the variable 'page'
	page = urllib2.urlopen(req)
	soup = BS(page, "html5lib")
	pool = Pool(processes=1)
	for divtag in soup.find_all('div', {'class': 'list'}):
		for divtag2 in divtag.find_all('div', {'class': 'fl odd'}):
			a = divtag2.find('a')
			if a:
				temp = a.find('div').find('div')
				song_name = temp.text.split(".mp3")[0]
				DownloadUrl = wikiDownload+str(a['href'].split('/')[2])								
				pool.apply_async(fileDownload, [current_path, DownloadUrl, song_name+".mp3"])				
		for divtag2 in divtag.find_all('div', {'class': 'fl even'}):
			ae = divtag2.find('a')
			if ae:
				temp = ae.find('div').find('div')
				song_name = temp.text.split(".mp3")[0]
				DownloadUrl = wikiDownload+str(a['href'].split('/')[2])								
				pool.apply_async(fileDownload, [current_path, DownloadUrl, song_name+".mp3"])				
	pool.close()
	pool.join()	
	return
# array = [9, 10, 11, 12, 16, 22, 32, 36]
if __name__ == '__main__':
	for i in range(1,11):		
		getSonglinks("Special Songs", wiki+str(i));
	

