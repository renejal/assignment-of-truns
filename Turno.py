class Turno:
    
    def __init__(self,cantVigilantsPerPeriod):
        self.cantVigilantsPerPeriod = cantVigilantsPerPeriod
        self.assigmentVigilants = []

    def getCantVigilantsPerPeriod(self):
        return self.cantVigilantsPerPeriod;
    def getCantAssigmentVigilants(self):
        return len(self.assigmentVigilants);
    def addVigilant(self,vigilant):
        self.assigmentVigilants.append(vigilant)

