import pandas as pd


class VigilantsDataFile:
    numberVigilants = int
    Dataset = None
    vigilantsInfo = []

    def __init__(self, urlFile):
        self.Dataset = pd.read_csv(urlFile)
        self.numberVigilants = len(self.Dataset)
        self.Dataset = pd.DataFrame(self.Dataset)    
        self.procedureData()

    def procedureData(self):
        infoVigilantsColums = 5
        cantPlaces = self.Dataset.columns.size - infoVigilantsColums
        for posicionVigilant in range(0,self.numberVigilants):
            vigilant = []
            shiftPreferences = []
            distancesBetweenPlacesToWatch = []
            vigilant.append(self.Dataset['ID Vigilante'][posicionVigilant])
            if pd.isna(self.Dataset['Sitio Esperado'][posicionVigilant]):
                vigilant.append(0)
            else:
                vigilant.append(self.Dataset['Sitio Esperado'][posicionVigilant])
            if pd.isna(self.Dataset['Horario preferencia 6 a.m - 2 p.m'][posicionVigilant]) == False:
                shiftPreferences.append(self.Dataset['Horario preferencia 6 a.m - 2 p.m'][posicionVigilant])
                shiftPreferences.append(self.Dataset['Horario preferencia 2 p.m - 10 p.m'][posicionVigilant])
                shiftPreferences.append(self.Dataset['Horario preferencia 10 p.m - 6 a.m'][posicionVigilant])
            for place in range(0,cantPlaces):
                distancesBetweenPlacesToWatch.append(self.Dataset['D. Sitio '+str(place+1)][posicionVigilant])
            vigilant.append(shiftPreferences)
            vigilant.append(distancesBetweenPlacesToWatch)
            self.vigilantsInfo.append(vigilant)

