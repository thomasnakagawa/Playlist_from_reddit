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
	#welcome user and ask for a name for the playlist
	DIREC = input("Folder name to put files in: ")
	print("Ok. Preparing.")

	#make a new folder with the name stored in DIREC. chdir makes the program run from this new directory. This makes it so the files will be put here
	os.makedirs(DIREC)
	os.chdir(DIREC)

	#setup reddit data. Gets the subreddit and collects the top posts
	r = praw.Reddit("Playlistmaker")
	subreddit = r.get_subreddit(SUBNAME)
	postlist = subreddit.get_hot(limit = NUM_TRACKS)

	#do the following for every one of the posts
	idx = 0
	for post in postlist:
		try:
			#remove any special characters from the title, this is so the title can become the name of the .mp3 file
			post_title = FixTitle(post.title, idx)
			#####
			#if the post is a music streaming one, then setup the settings for the downloading and saving of the audio
			if post.link_flair_text.lower() == 'music streaming':
				options = {
				    'format': 'bestaudio/best', # choice of quality
				    'extractaudio' : True,      # only keep the audio
				    'audioformat' : "mp3",      # convert to mp3 
				    'outtmpl': str(idx) + post_title + '.mp3',        # name the file the ID of the video
				    'noplaylist' : True,        # only download single song, not playlist
				}

				#download the video
				ydl = youtube_dl.YoutubeDL(options)
				ydl.download([post.url])
				print('Got track ' + str(idx) + ' successfully.')
				idx += 1
			####

		except:
			#for some reason the video can't be downloaded. Oh well, just move on to the next
			print("An error getting this video. Skipping")
except:
	#some kind of error that was not related to downloading a video happened.
	input("Big error, sorry")


input("Done")