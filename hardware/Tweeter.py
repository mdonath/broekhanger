from TwitterAPI import TwitterAPI, TwitterOAuth

class Tweeter:
	def __init__(self, app):
		print("Init Tweeter")
		ck = app.config['TWITTER_CONSUMER_KEY']
		cs = app.config['TWITTER_CONSUMER_SECRET']
		atk = app.config['TWITTER_ACCESS_TOKEN_KEY']
		ats = app.config['TWITTER_ACCESS_TOKEN_SECRET']
		self.twitterapi = TwitterAPI(ck, cs, atk, ats) 
		print("Tweeter [OK]")

	def tweet(self, bestand, score, naam):
		print("Tweeting!")
		tweet = "{0} heeft {1} aan de spijkerbroek gehangen bij Scouting Heino!".format(naam, score)
		file = open(bestand, 'rb')
		data = file.read()
		r = self.twitterapi.request('statuses/update_with_media', {'status': tweet}, {'media[]': data})
		print('getweet!' if r.status_code == 200 else 'FAILURE')

