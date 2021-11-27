import pandas as pd


class VigilantsDataFile:
    numberVigilantes = int
    Dataset = None
    vigilantesInfo = []

    def __init__(self, urlFile):
        self.Dataset = pd.read_csv(urlFile)
        self.numberVigilantes = len(self.Dataset)
        self.Dataset = pd.DataFrame(self.Dataset)    
        self.procedureData()

    def procedureData(self):
        infoVigilantesColums = 5
        cantPlaces = self.Dataset.columns.size - infoVigilantesColums
        for posicionVigilant in range(0,self.numberVigilantes):
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
            self.vigilantesInfo.append(vigilant)

