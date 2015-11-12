###
##
#Websites that I used
#http://willdrevo.com/projects/
#
#
##
###


import praw			#to access reddit
import youtube_dl	#to download youtube videos
import re
import os

#constants
ID = 'Playlistmaker'
NUM_POSTS = 25
VALID_SITES = [
	"youtube", 
	"youtu.be",
	"vimeo", 
	"soundcloud",
	"bandcamp",
	"mixcloud"
]
YOUTUBE_OPTIONS = {
    'format': 'bestaudio/best', 						# choice of quality
    'extractaudio' : True,      						# only keep the audio
    'audioformat' : "mp3",      						# convert to mp3 
    'autonumber_size' : 2,								# use two digits for the incrementing number
    'outtmpl': '\%(autonumber)s,%(title)s.mp3',			# name the file the ID of the video
    'noplaylist' : True,        						# only download single song, not playlist
}

#methods
def DownloadableURL(str):
	if any(x in str for x in VALID_SITES):
		return True
	return False

#main
try:
	#welcome user and ask for a name for the playlist
	subreddit_name = input("Which subreddit would you like? /r/")
	target_dir 	   = input("Folder name to put files in: ")
	print("Ok. Preparing.")

	#make a new folder.
	os.makedirs(target_dir)
	os.chdir(target_dir)

	#setup reddit. Gets the subreddit and collects the top posts
	post_list = praw.Reddit(ID).get_subreddit(subreddit_name).get_hot(limit = NUM_POSTS)
	print('Reddit ready')

	#setup youtube 
	youtube = youtube_dl.YoutubeDL(YOUTUBE_OPTIONS)
	print('Youtube ready')

	#make a list of urls that can have a video downloaded from
	compatable_urls = []
	for post in post_list:
		if DownloadableURL(post.url):
			compatable_urls.append(post.url)

	#download the videos
	print('Downloading')
	youtube.download(compatable_urls)

except:
	print('Error, sorry')


input("Done.")