import pandas as pd

def generateResultBySite(cantVigilantsByPeriod, path, solution):

    writer = pd.ExcelWriter(path + "Site.xlsx", engine='openpyxl')
    wb = writer.book
    for sideId in range(0, len(solution.sitesSchedule)):
        sheduleSite = {}
        if len(solution.sitesSchedule[sideId]) > 0:
            cantMissingVigilants = 0
            numerDay = 1
            period = 0
            vigilantsByDay = []
            siteSchedule = solution.sitesSchedule[sideId]
            for assignedVigilantsInPeriod in range(0, len(siteSchedule)):
                vigilantsByDay.append(siteSchedule[assignedVigilantsInPeriod])
                cantMissingVigilants += cantVigilantsByPeriod[sideId][assignedVigilantsInPeriod] - len(
                    siteSchedule[assignedVigilantsInPeriod])
                period += 1
                if period == 24:
                    vigilantsByDay.append(cantMissingVigilants)
                    sheduleSite['day' + str(numerDay)] = vigilantsByDay
                    vigilantsByDay = []
                    period = 0
                    cantMissingVigilants = 0
                    numerDay += 1
        df = pd.DataFrame(sheduleSite)
        df.to_excel(writer, sheet_name='site' + str(sideId + 1))
        sideId += 1
    wb.save(path + "Site.xlsx")
    writer.close()
