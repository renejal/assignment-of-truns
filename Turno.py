import random
class Turno:



    def __init__(self):
        self.assigmentVigilantes = []
        self.state = 0
        self.cantVigilantesPerPeriod = 0
        self.assigmentVigilantes = 0

    def getCantVigilantsPerPeriod(self):
        return self.cantVigilantsPerPeriod;
    def getCantAssigmentVigilants(self):
        return len(self.assigmentVigilants);
    def addVigilant(self, vigilant):
        for i in vigilant:
         self.assigmentVigilants.append(i)

    def vigilantAssigment(self):
        ListVigilantes = self.aleatoryVigilantes()

