###
##
#Website tutorial that I used
#http://willdrevo.com/downloading-youtube-and-soundcloud-audio-with-python-and-pandas//
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
	"youtube.com", 
	"youtu.be",
	"vimeo.com", 
	"soundcloud.com",
	"bandcamp.com",
	"mixcloud.com"
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
	print('Hello. This program will download the video links of the front page of a subreddit as .mp3 files.')
	subreddit_name = input("Which subreddit would you like? /r/")
	target_dir 	   = input("Folder name to put files in: ")
	print("Ok. Preparing.")

	#setup reddit. Gets the subreddit and collects the top posts
	post_list = praw.Reddit(ID).get_subreddit(subreddit_name).get_hot(limit = NUM_POSTS)
	print('[playlist maker] Reddit ready')

	#setup youtube 
	youtube = youtube_dl.YoutubeDL(YOUTUBE_OPTIONS)
	print('[playlist maker] Youtube ready')

	#make a list of urls that can have a video downloaded from
	compatable_urls = []
	for post in post_list:
		if DownloadableURL(post.url):
			compatable_urls.append(post.url)

	#make a new folder.
	if not os.path.exists(target_dir):
	    os.makedirs(target_dir)
	    print('[playlist maker] new folder ' + target_dir + ' made')
	os.chdir(target_dir)
 
	#download the videos
	print('[playlist maker] Downloading')
	for url in compatable_urls:
		try:
			youtube.download([url])
		except:
			print("[playlist maker] Couldn't get this video.")


except:
	print('Error, sorry')


input("Done.")