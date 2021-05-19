import random

assigmentVigilants = []
state = 0
cantVigilantsPerPeriod = 0
assigmentVigilants = 0

class Turno:

    def getCantVigilantsPerPeriod(self):
        return self.cantVigilantsPerPeriod;
    def getCantAssigmentVigilants(self):
        return len(self.assigmentVigilants);
    def addVigilant(self, vigilant):
        for i in vigilant:
         self.assigmentVigilants.append(i)

    def vigilantAssigment(self):
        ListVigilantes = self.aleatoryVigilantes()

