from numpy.core.numeric import NaN
from Vigilant import Vigilant
import numpy as np
import pandas as pd
from pandas import DataFrame

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

    def generateResultByVigilant(path,solution):
        writer = pd.ExcelWriter(path+"Vigilant.xlsx", engine='openpyxl') 
        wb  = writer.book
        for vigilantId in range(0,len(solution.vigilantsSchedule)):
            sheduleVigilant = {}
            if solution.vigilantsSchedule[vigilantId] != None:
                numerDay = 1
                period = 0
                scheduleByDay = []
                workingHoursByDay = 0
                totalHoursWork = 0
                for assignedSiteInPeriod in solution.vigilantsSchedule[vigilantId].shifts:
                    if assignedSiteInPeriod != 0:
                        workingHoursByDay+=1
                    scheduleByDay.append(assignedSiteInPeriod)
                    period+=1
                    if period == 24:
                        totalHoursWork+=workingHoursByDay
                        scheduleByDay.append(str(workingHoursByDay)+'Hours')
                        sheduleVigilant['day'+str(numerDay)] = scheduleByDay
                        if numerDay % 7 == 0:
                            scheduleByDay.append(str(totalHoursWork)+'Total Hours')
                            totalHoursWork = 0
                        else:
                            scheduleByDay.append('')

                        scheduleByDay = []
                        period = 0
                        numerDay+=1
                        workingHoursByDay = 0
            
            df = pd.DataFrame(sheduleVigilant)
            df.style.background_gradient(cmap='YlOrRd', axis=1, subset=df.index[-1])
            df.to_excel(writer, sheet_name = 'vig'+str(vigilantId+1))
            vigilantId += 1
        wb.save(path+"Vigilant.xlsx")
        writer.close()
