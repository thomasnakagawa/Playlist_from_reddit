import praw
import youtube_dl
import re
import os

#constants
SUBNAME = 'music'
NUM_TRACKS = 25


def FixTitle(str, idx):
	return re.sub('[^0-9a-zA-Z]+', '_', str)
try:
	DIREC = input("Folder name to put files in: ")
	print("Ok. Preparing.")
	os.makedirs(DIREC)
	os.chdir(DIREC)
	r = praw.Reddit("Playlistmaker")
	subreddit = r.get_subreddit(SUBNAME)
	postlist = subreddit.get_hot(limit = NUM_TRACKS)
	#for idx, post in enumerate(postlist):
	idx = 0
	for post in postlist:
		try:
			post_url = post.url
			post_title = FixTitle(post.title, idx)
			#post_title = idx + post_title
			if post_url.find("reddit") == -1:#if reddit is in the url, then it is a self-post, which wont have a video, so skip it
				options = {
				    'format': 'bestaudio/best', # choice of quality
				    'extractaudio' : True,      # only keep the audio
				    'audioformat' : "mp3",      # convert to mp3 
				    'outtmpl': post_title + '.mp3',        # name the file the ID of the video
				    'noplaylist' : True,        # only download single song, not playlist
				}
				ydl = youtube_dl.YoutubeDL(options)
				ydl.download([post_url])
				idx += 1
		except:
			print("An error getting this video. Skipping")
except:
	input("Big error, sorry")


input("Done")