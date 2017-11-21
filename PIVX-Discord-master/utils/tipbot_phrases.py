import json, requests, random
from utils import parsing

class TBPhrases:
    def __init__(self, bot):
        self.bot = bot

    def phrases():
        phrase1 = "You must construct additional Pylons"
        phrase2 = "Need more vespene gas"
        phrase3 = "Not enough Minerals"
        phrase4 = "You must construct additional Pylons"
        phrase5 = "You must construct additional Pylons"
	
        all_phrases = (phrase1, phrase3, phrase4, phrase5, phrase2)

        return all_phrases[random.randint(1,5)]