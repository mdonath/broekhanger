from TwitterAPI import TwitterAPI, TwitterOAuth

class Tweeter:
	def __init__(self, credentialsfile = 'credentials.txt'):
		print("Initialiseer Tweeter")
		o = TwitterOAuth.read_file(credentialsfile)
		self.twitterapi = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret) 
		print("Tweeter [OK]")

	def tweet(self, bestand, score):
		print("Tweeting!")
		tweet = 'En weer een nieuwe score van ' + score[:2]+':'+score[2:]
		file = open(bestand, 'rb')
		data = file.read()
		r = self.twitterapi.request('statuses/update_with_media', {'status': tweet}, {'media[]': data})
		print('getweet!' if r.status_code == 200 else 'FAILURE')

