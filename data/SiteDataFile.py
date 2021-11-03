import numpy as np
import pandas as pd
from pandas import DataFrame


class SiteDataFile:
    __data_problem = pd.DataFrame()  # dataset procedure for problem
    __workingDay:int

    def __init__(self, urlFile, weeks):
        Dataset = pd.read_csv(urlFile, sep=",")
        self.weeks = weeks
        self.__workingDay = []
        numberSites = len(Dataset)
        self.__data_problem = np.zeros((numberSites, self.weeks * 168), dtype=int)
        self.procedureData(Dataset)



    def procedureData(self,Dataset):
        data = pd.DataFrame(Dataset)
        for row in data.index:
            day = data["lunes"][row]
            numGuard = data["numero guardias"][row]
            self.dataInitialization(numGuard,row)
            hoursInitGuard, hoursFinitGuard =self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 0, row, numGuard)
            day = data["martes"][row]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 1, row, numGuard)
            day = data["miercoles"][row]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 2, row, numGuard)
            day = data["jueves"][row]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 3, row, numGuard)
            day = data["viernes"][row]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 4, row, numGuard)
            day = data["sabado"][row]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 5, row, numGuard)
            day = data["domingo"][row]
            hoursInitGuard, hoursFinitGuard = self.proceduresplit(day)
            self.hoursConverst(hoursInitGuard, hoursFinitGuard, 6, row, numGuard)
            workinday = data["jornada"][row]
            self.__workingDay.append(workinday)


        dataframe = pd.DataFrame(self.__data_problem)
        dataframe.to_csv("dataset/Inputdata.csv")

    def proceduresplit(self, hoursdayList):
        if hoursdayList == '0':
            return [0, 0]
        listTemp = hoursdayList.split(",")
        return int(listTemp[0]),int(listTemp[1])

    def hoursConverst(self, inithour, finithour, day, row, numGuards):
        listAssignedShifts=self.assignedShifts(inithour, finithour, day)
        for i in range(len(listAssignedShifts)):
            self.__data_problem[row][listAssignedShifts[i]] = 0

    def assignedShifts(self, parInihour, parFinithour ,day):
        shiftResult = []
        for i in range(24):
            if i < parInihour or i > parFinithour:
                for j in range (0,self.weeks):
                    shiftResult.append(i+(day*24)+(169*j))
        return shiftResult
    def dataInitialization(self, numGuards, row):
        self.__data_problem[row] = numGuards

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
                self.__data_problem[rows][0] = i
                posInt = posInt + 1
            else:

                posInt = posInt * day
                dayLimit = dayLimit + 1

                if i > 0 and dayLimit == 1:
                    for k in range(int(i)):
                        self.__data_problem[rows][k + 1] = 0
                else:
                    if i < 24 and dayLimit == 2:
                        for j in range(int(i), 24):
                            self.__data_problem[rows][j] = 0

        if dayLimit == 2:
            day = day + 1
            dayLimit = 1

    def get_data_problem(self):
        return self.__data_problem

    def get_working_day(self):
        return self.__workingDay
    def generateResultBySite(cantVigilantsByPeriod,path,solution):
        writer = pd.ExcelWriter(path+"Site.xlsx", engine='openpyxl') 
        wb  = writer.book
        for sideId in range(0,len(solution.sitesSchedule)):
            sheduleSite = {}
            if len(solution.sitesSchedule[sideId]) > 0:
                cantMissingVigilants = 0
                numerDay = 1
                period = 0
                vigilantsByDay = []
                siteSchedule = solution.sitesSchedule[sideId]
                for assignedVigilantsInPeriod in range(0,len(siteSchedule)):
                    vigilantsByDay.append(siteSchedule[assignedVigilantsInPeriod])
                    cantMissingVigilants+= cantVigilantsByPeriod[sideId][assignedVigilantsInPeriod] - len(siteSchedule[assignedVigilantsInPeriod]) 
                    period+=1
                    if period == 24:
                        vigilantsByDay.append(cantMissingVigilants)
                        sheduleSite['day'+str(numerDay)] = vigilantsByDay
                        vigilantsByDay = []
                        period = 0
                        cantMissingVigilants = 0
                        numerDay+=1
            df = pd.DataFrame(sheduleSite)
            df.to_excel(writer, sheet_name = 'site'+str(sideId+1))
            sideId += 1
        wb.save(path+"Site.xlsx")
        writer.close()
























