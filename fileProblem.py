import numpy
import numpy as np
import pandas as pd
from pandas import DataFrame


class FileProblem:
    column= 0
    Row = 0
    UrlFile = ""
    Weeks = int
    NumberSites = int
    Dataset = None
    DataProblem = pd.DataFrame()  # Data procedure for problem

    def __init__(self, urlFile, weeks):
        self.UrlFile = urlFile
        self.Weeks = weeks
        self.Dataset = pd.read_csv(urlFile, sep=",")
        self.NumberSites = len(self.Dataset)
        self.DataProblem = np.zeros((self.NumberSites, self.Weeks*168), dtype=int)

    def procedureData(self):
        #data = self.Dataset.copy(deep=True)
        data = pd.DataFrame(self.Dataset)
        #data = data.dropna()  #clear empty data
        for i in data.index:
            site = data["sitio"][i]
            day = data["lunes"][i]
            numGuard = data["numero guardias"][i]
            self.dataInitialization(numGuard,i)
            hoursInitGuard, hoursFinitGuard =self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 0, i, numGuard)
            day = data["martes"][i]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 1, i, numGuard)
            day = data["miercoles"][i]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 2, i, numGuard)
            day = data["jueves"][i]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 3, i, numGuard)
            day = data["viernes"][i]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 4, i, numGuard)
            day = data["sabado"][i]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 5, i, numGuard)
            day = data["domingo"][i]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 6, i, numGuard)


        dataframe = pd.DataFrame(self.DataProblem)
        dataframe.to_csv("data.csv")



    def proceduresplit(self, hoursdayList):
        if hoursdayList == '0':
            return [0, 0]
        listTemp = hoursdayList.split(",")
        return int(listTemp[0]),int(listTemp[1])


    def hoursConverst(self, inithour, finithour, day, row, numGuards):
        listAssignedShifts=self.assignedShifts(inithour, finithour, day)
        for i in range(len(listAssignedShifts)):
            self.DataProblem[row][listAssignedShifts[i]] = 0


    def assignedShifts(self, parInihour, parFinithour ,day):
        shift = []
        shiftResult = []
        for i in range(parInihour,parFinithour+1):
            shift.append(i)

        for i in range(25):
            if i not in shift:
                shiftResult.append(i+(day*25))
        return shiftResult


    def dataInitialization(self, numGuards, row):
        self.DataProblem[row] = numGuards



























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























