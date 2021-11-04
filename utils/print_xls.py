import pandas as pd
from dominio.Solution import Solution

def from_dataFrame(solucion: Solution):
    #todo implemantar from_data frame para solucion
    #matriz de relacion vigilante vs periodo donde periodo termina el sitio en el cual trabajo el vigilante en ese periodo
    #1: obtener de la solucion los vigilantes sus schedules
        #1.1

    #2:

    pass
def generateResultByVigilant(path, solution):
    writer = pd.ExcelWriter(path + "results.xlsx", engine='openpyxl')
    wb = writer.book
    for vigilantId in range(0, len(solution.vigilantsSchedule)):
        sheduleVigilant = {}
        if solution.vigilantsSchedule[vigilantId] != None:
            numerDay = 1
            period = 0
            scheduleByDay = []
            workingHoursByDay = 0
            totalHoursWork = 0
            for assignedSiteInPeriod in solution.vigilantsSchedule[vigilantId].shifts:
                if assignedSiteInPeriod != 0:
                    workingHoursByDay += 1
                scheduleByDay.append(assignedSiteInPeriod)
                period += 1
                if period == 24:
                    totalHoursWork += workingHoursByDay
                    scheduleByDay.append(str(workingHoursByDay) + 'Hours')
                    sheduleVigilant['day' + str(numerDay)] = scheduleByDay
                    if numerDay % 7 == 0:
                        scheduleByDay.append(str(totalHoursWork) + 'Total Hours')
                        totalHoursWork = 0
                    else:
                        scheduleByDay.append('')

                    scheduleByDay = []
                    period = 0
                    numerDay += 1
                    workingHoursByDay = 0

        df = pd.DataFrame(sheduleVigilant)
        df.style.background_gradient(cmap='YlOrRd', axis=1, subset=df.index[-1])
        df.to_excel(writer, sheet_name='vig' + str(vigilantId + 1))
        vigilantId += 1
    wb.save(path + "Vigilant.xlsx")
    writer.close()
