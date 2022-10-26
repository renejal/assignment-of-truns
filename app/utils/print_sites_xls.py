import numpy as np
import pandas as pd
from dominio.Solution import Solution 

TOTAL_HOURS:int = 24
DAYS_ON_WEEK: int = 7

def generate_excel_site(solution:Solution, path:str):
    writer = pd.ExcelWriter(path+".xlsx", engine='openpyxl')
    wb = writer.book
    for site in solution.sites_schedule:
        dataSite = solution.problem.sites[site.site_id-1]
        hours_extra_last_week = dataSite.hours_extra_last_week
        total_days = dataSite.total_weeks*DAYS_ON_WEEK
        if hours_extra_last_week != 0:
            total_days +=1
        data = [[[]]*total_days]*TOTAL_HOURS
        data.append([0]*total_days)
        data = np.array(data, dtype=object).tolist()
        for shift in site.site_schedule:
            for period in range(shift.shift_start,shift.shift_end+1):
                day = int( (period+hours_extra_last_week)/TOTAL_HOURS)
                hour = (period+hours_extra_last_week) - day*TOTAL_HOURS
                data[hour][day] = shift.assigment_vigilantes
                data[TOTAL_HOURS][day] += shift.necesary_vigilantes - len(shift.assigment_vigilantes)
        df = pd.DataFrame(data,columns=list("day"+str(day)  for day in range(1,total_days+1)))
        df.to_excel(writer, sheet_name='site' + str(site.site_id))
        wb.save(path+".xlsx")
    writer.close()
