from numpy.core.numeric import NaN
from Vigilant import Vigilant
import numpy as np
import pandas as pd
from pandas import DataFrame

class VigilantsFile:
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
        for actualVigilant in range(0,self.numberVigilants):
            vigilant = []
            preferences = []
            disitancePlaces = []
            vigilant.append(self.Dataset['ID Vigilante'][actualVigilant])
            if pd.isna(self.Dataset['Sitio Esperado'][actualVigilant]):
                vigilant.append(0)
            else:
                vigilant.append(self.Dataset['Sitio Esperado'][actualVigilant])
            if pd.isna(self.Dataset['Horario preferencia 6 a.m - 2 p.m'][actualVigilant]) == False:
                preferences.append(self.Dataset['Horario preferencia 6 a.m - 2 p.m'][actualVigilant])
                preferences.append(self.Dataset['Horario preferencia 2 p.m - 10 p.m'][actualVigilant])
                preferences.append(self.Dataset['Horario preferencia 10 p.m - 6 a.m'][actualVigilant])
            for j in range(0,cantPlaces):
                disitancePlaces.append(self.Dataset['D. Sitio '+str(j+1)][actualVigilant])
            vigilant.append(preferences)
            vigilant.append(disitancePlaces)
            self.vigilantsInfo.append(vigilant)

#???????????????????????????????????????????????????????????????????????#???????????????????????????????????????????????????????????????????????
            #self.DataProblem[columns][i]
        #for index, row in data.iterrows():
        #    self.itemRow(row, rows, day)
        #    rows = rows + 1
        #    day = day + 1


        #dataF = pd.DataFrame(self.DataProblem)
        #dataF.to_csv('data.csv', index=False, header=False)
        #dataF.to_csv('data.csv')
    def itemRow(self, row, rows, day):
        dayLimit = 0
        upperLimit = 0
        hf = 24
        posInt = 0
        posFinit = 0
        for i in row:
            if posInt == 0:
                self.DataProblem[rows][0] = i
                posInt = posInt + 1
            else:

                posInt = posInt * day
                dayLimit = dayLimit + 1

                if i > 0 and dayLimit == 1:
                    for k in range(int(i)):
                        self.DataProblem[rows][k+1] = 0
                else:
                    if i < 24 and dayLimit == 2:
                        for j in range(int(i), 24):
                            self.DataProblem[rows][j] = 0
        if dayLimit == 2:
            day = day + 1
            dayLimit = 1