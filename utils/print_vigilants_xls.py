import pandas as pd
def generateResultByVigilant(path, solution):
    writer = pd.ExcelWriter(path + "Vigilant.xlsx", engine='openpyxl')
    wb = writer.book
    for vigilantId in range(0, len(solution.vigilantesSchedule)):
        sheduleVigilant = {}
        if solution.vigilantesSchedule[vigilantId] != None:
            numerDay = 1
            period = 0
            scheduleByDay = []
            workingHoursByDay = 0
            totalHoursWork = 0
            for assignedSiteInPeriod in solution.vigilantesSchedule[vigilantId].shifts:
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
