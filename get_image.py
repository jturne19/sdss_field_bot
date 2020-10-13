#! /usr/bin/env python3
"""
script that:
reads in the running list of SDSS fields,
picks one at random,
fetches the color image from the SDSS skyserver,
creates text for the tweet with the Run, CamCol, and Field numbers
gets the twitter api stuff using tweepy read from credentials.py,
tweets out the image and text,
rewrites the running list without the latest field in it

chmod +x get_image.py

crontab it get it to post on a regular basis

2020-10-13
"""
import numpy as np
import tweepy
import wget

from credentials import *

if __name__ == '__main__':

	# read in the running list of fields
	with open('running_field.list', 'r') as f:
		fields = f.readlines()

	# get the number of fields needed for the random index
	l = len(fields)

	# pick a random index
	index = np.random.randint(low=0, high=l)

	# strip out the newline character from the chosen field
	field_string = fields[index].strip('\n')

	# create the URL to acess the SDSS SkyServer which creates the actual 3 color image for us
	query = 'http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getJpegCodec/?%s&Z=50&TaskName=Skyserver.FrameByRCFZ'%field_string

	# fetch the image and save in the tmp directory
	# can't overwrite the tmp.jpg so it makes 'tmp (1).jpg' instead and overwrites that because it's dumb 
	image_path = wget.download(query, out='tmp/tmp.jpg')

	# split up the field string into the component parts - Run, CamCol, Field
	fsarr = field_string.split('&')

	R = fsarr[0][2:]
	C = fsarr[1][2:]
	F = fsarr[2][2:]

	# create the tweet text 
	tweet_text = 'Run %s Column %s Field %s'%(R, C, F)

	# twitter api stuff using tweepy and our credentials.py which has the secret keys
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	# post to twitter
	status = api.update_with_media(image_path, tweet_text)

	# delete that field from the running list
	with open('running_field.list', 'w') as f:
		for line in fields:
			if line.strip('\n') != field_string:
				f.write(line)	