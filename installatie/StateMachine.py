import pygame


class State:
	def __init__(self, name):
		self.name = name

	def event(self, event):
		return self

	def action(self, broekhanger):
		pass

	def __str__(self):
		return self.name

class StateStart(State):
	def __init__(self):
		State.__init__(self, 'Start')
		pygame.mixer.init()
		self.audio_boing = pygame.mixer.Sound('audio/boing.wav')

	def event(self, event):
		if (event == 'plank_p'):
			print ("Speler gaat op de plank staan")
			self.audio_boing.play()
			return StateMachine.OP_PLANK
		return None

	def action(self, broekhanger):
		broekhanger.klok_leeg()

class StateOpPlank(State):
	def __init__(self):
		State.__init__(self, 'Staat op de plank')
		pygame.mixer.init()
		self.audio_boing = pygame.mixer.Sound('audio/boing.wav')

	def event(self, event):
		if (event == 'broek_p'):
			print ("Speler hangt aan de broek, maar nog met voeten aan de grond")
			self.audio_boing.play()
			return StateMachine.OP_SCHERP
		if (event == 'plank_r'):
			print ("Speler stapt er weer vanaf")
			return StateMachine.VAN_PLANK
		if event == 'reset':
			print ("RESET!")
			return StateMachine.START
		return None

	def action(self, broekhanger):
		broekhanger.klok_op_nul()

class StateVanPlank(State):
	def __init__(self):
		State.__init__(self, 'Even van de plank gestapt')
		pygame.mixer.init()
		self.audio_boing = pygame.mixer.Sound('audio/boing.wav')

	def event(self, event):
		if (event == 'plank_p'):
			print ("Speler stapt er toch weer op")
			self.audio_boing.play()
			return StateMachine.OP_PLANK
		if event == 'reset':
			print ("RESET!")
			return StateMachine.START
		return None

	def action(self, broekhanger):
		broekhanger.klok_leeg()

class StateOpScherp(State):
	def __init__(self):
		State.__init__(self, 'Klaar om te beginnen')
		pygame.mixer.init()
		self.audio_boing = pygame.mixer.Sound('audio/boing.wav')

	def event(self, event):
		if (event == 'plank_r'):
			print ("Speler hangt en het tellen kan beginnen!")
			return StateMachine.HANGT
		if (event == 'broek_r'):
			print ("Speler laat de broek weer los")
			self.audio_boing.play()
			return StateMachine.OP_PLANK
		return None

class StateHangt(State):
	def __init__(self):
		State.__init__(self, 'HANGT!')

	def event(self, event):
		if (event == 'plank_p'):
			print ("Speler raakt met voeten de grond -> AF!")
			return StateMachine.LOSGELATEN
		if (event == 'broek_r'):
			print ("Speler laat de broek los -> AF!")
			return StateMachine.LOSGELATEN
		return None

	def action(self, broekhanger):
		broekhanger.start_de_tijd()

class StateLosGelaten(State):
	def __init__(self):
		State.__init__(self, 'Losgelaten')

	def event(self, event):
		if (event == 'reset'):
			print ("Speler is klaar, opnieuw")
			return StateMachine.START
		return None

	def action(self, broekhanger):
		broekhanger.stop_de_tijd()



class StateMachine:
	START = StateStart()
	OP_PLANK = StateOpPlank()
	VAN_PLANK = StateVanPlank()
	OP_SCHERP = StateOpScherp()
	HANGT = StateHangt()
	LOSGELATEN = StateLosGelaten()

	def __init__(self, broekhanger):
		self.broekhanger = broekhanger
		self.states = [
			  StateMachine.START
			, StateMachine.OP_PLANK
			, StateMachine.VAN_PLANK
			, StateMachine.OP_SCHERP
			, StateMachine.HANGT
			, StateMachine.LOSGELATEN
		]
		self.set_state(StateMachine.START)

	def reset(self):
		self.event('reset')

	def hangen(self):
		self.event('broek_p')

	def loslaten(self):
		self.event('broek_r')

	def opstappen(self):
		self.event('plank_p')

	def afstappen(self):
		self.event('plank_r')

	def event(self, event):
		state = self.state.event(event)
		self.set_state(state)

	def set_state(self, state):
		if (state != None):
			state.action(self.broekhanger)
			self.state = state

	def __str__(self):
		return ", ".join(('*'+str(s)+'*') if s == self.state else str(s) for s in self.states)

