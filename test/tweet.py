#!/usr/bin/python

from TwitterAPI import TwitterAPI, TwitterOAuth

o = TwitterOAuth.read_file('credentials.txt')
api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret) 

TWEET_TEXT = "Dit is een tweet met een plaatje"

file = open('image1.jpg', 'rb')
data = file.read()
r = api.request('statuses/update_with_media', {'status': TWEET_TEXT}, {'media[]': data})

print('SUCCESS' if r.status_code == 200 else 'FAILURE')

print('\nQUOTA: %s' % r.get_rest_quota())

