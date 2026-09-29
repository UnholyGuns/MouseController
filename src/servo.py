import random

class Servo:
    def __init__(self):
        self.location = 0
        self.freeMove = True
        self.referenced = False

    def init(self):
        pass

    def getLocation(self):
        self.location = random.randrange(0,5000)
        return self.location


    