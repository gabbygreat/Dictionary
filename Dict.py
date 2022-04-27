import json
import random

class Dictionary:
	def __init__(self, fileName):
		self.fileName = fileName
		with open(self.fileName) as file:
			self.file = json.load(file)

	def turn(self, lis):
		return lis.casefold()
	
	def meaning(self, key):
		if key.casefold() in list(map(self.turn, list(self.file.keys()))):
			try:
				return self.file[key.title()]
			except KeyError:
				return self.file[key]
		else:
			return []

	def getRandom(self):
		rand = list(self.file.keys())
		random.shuffle(rand)
		return rand[random.randint(0, len(rand)+1)]