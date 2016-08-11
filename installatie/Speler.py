speler_counter = 0

class Speler:
	def __init__(self, naam, email, categorie='K'):
		global speler_counter
		speler_counter = speler_counter + 1
		self.id = speler_counter
		self.naam = naam
		self.email = email
		self.categorie = categorie
