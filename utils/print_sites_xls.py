import numpy as np
import pandas as pd
from dominio.Solution import Solution

PATH_FILE: str = "./dataset/results/Site.xlsx"
TOTAL_HOURS:int = 24
TOTAL_DAYS: int = 7

def generate_excel_site(solution : Solution):
    writer = pd.ExcelWriter(PATH_FILE, engine='openpyxl')
    wb = writer.book
    for site in solution.sites_schedule:
        data = [[[]]*solution.problem.sites[site.site_id-1].total_weeks*TOTAL_DAYS]*TOTAL_HOURS
        data.append([0]*solution.problem.sites[site.site_id-1].total_weeks*TOTAL_DAYS)
        data = np.array(data, dtype=object).tolist()
        for shift in site.site_schedule:
            for period in range(shift.shift_start,shift.shift_end+1):
                day = int(period/TOTAL_HOURS)
                hour = period - day*TOTAL_HOURS
                data[hour][day] = shift.assigment_vigilantes
                data[TOTAL_HOURS][day] += shift.necesary_vigilantes - len(shift.assigment_vigilantes)
        df = pd.DataFrame(data,columns=list("day"+str(day)  for day in range(1,day+2)))
        df.to_excel(writer, sheet_name='site' + str(site.site_id))
        wb.save(PATH_FILE)
    writer.close()
