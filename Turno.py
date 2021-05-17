import random

assigmentVigilants = []

class Turno:

    def __init__(self, cantVigilantsPerPeriod, listVigilantes):
        self.cantVigilantsPerPeriod = cantVigilantsPerPeriod
        self.assigmentVigilants = listVigilantes

    def getCantVigilantsPerPeriod(self):
        return self.cantVigilantsPerPeriod;
    def getCantAssigmentVigilants(self):
        return len(self.assigmentVigilants);
    def addVigilant(self, vigilant):
        for i in vigilant:
         self.assigmentVigilants.append(i)

    def vigilantAssigment(self):
        ListVigilantes = self.aleatoryVigilantes()

