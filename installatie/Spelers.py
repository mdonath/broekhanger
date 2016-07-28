class Spelers:
	def __init__(self):
		self.lijst = []
		self.wachtrij = []

	def voeg_speler_toe(self, speler):
		self.lijst.append(speler)
		self.wachtrij.append(speler)
	
	def geef_wachtrij(self):
		return self.wachtrij

	def haal_eerste_uit_wachtrij(self):
		return self.wachtrij.pop()


class Speler:
	def __init__(self, naam, email, categorie):
		self.naam = naam
		self.email = email
		self.categorie = categorie
		self.beurten = []

	def geef_beurt(self, score, bestand, tijdstip):
		beurt = Beurt(score, bestand, tijdstip)
		self.beurten.append(beurt)


class Categorie:
	KLEIN, MIDDEL, GROOT = range(0,3)


class Beurt:
	def __init__(self, score, foto, tijdstip):
		self.score = score
		self.foto = foto
		self.tijdstip = tijdstip
