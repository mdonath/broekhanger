speler_counter = 0

class Speler:
	def __init__(self, naam, email, categorie='K'):
		global speler_counter
		speler_counter = speler_counter + 1
		self.id = speler_counter
		self.naam = naam
		self.email = email
		self.categorie = categorie
		self.scores = []
		self.fotos = []

	def voeg_score_toe(self, score):
		print("DEBUG: Voeg score {1} toe aan speler: {0}".format(self.naam, score))
		self.scores.insert(0,score)

	def voeg_foto_toe(self, foto):
		print("Nieuwe Foto: '{0}' voor {1}".format(foto, self.naam))
		self.fotos.insert(0, foto)
