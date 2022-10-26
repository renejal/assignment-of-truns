import pandas as pd
from dominio.Solution import Solution 
from conf import settings

PATH_FILE: str = "./dataset/results/Vigilantes.xlsx"
TOTAL_HOURS: int = 24
DAYS_ON_WEEK: int = 7


def generate_excel_vigilantes(solution:  Solution, path: str):
    writer = pd.ExcelWriter(path+".xlsx", engine='openpyxl')
    wb = writer.book
    columnas = ["Hours Week"] + list("day"+str(day) for day in range(1,settings.MAX_TOTAL_WEEKS*DAYS_ON_WEEK+1))
    data = []
    for vigilant in solution.vigilantes_schedule:
        hours_by_week_colum = [vigilant.total_hours_worked_by_week]
        days_schedule= [[]]*settings.MAX_TOTAL_WEEKS*DAYS_ON_WEEK
        for shift_place in vigilant.shifts:
            hours_extra_last_week = solution.problem.sites[shift_place.site_id-1].hours_extra_last_week
            shift_start = shift_place.shift.shift_start+hours_extra_last_week
            shift_end = shift_place.shift.shift_end+hours_extra_last_week
            start_day = int(shift_start/TOTAL_HOURS)
            end_day =  int(shift_end/TOTAL_HOURS)
            if start_day == end_day:
                days_schedule[start_day] = [shift_place.site_id, [shift_start - start_day*TOTAL_HOURS,shift_end - start_day*TOTAL_HOURS]]
            else:
                days_schedule[start_day] = [shift_place.site_id, [shift_start - start_day*TOTAL_HOURS,shift_end - end_day*TOTAL_HOURS]]
        data.append(hours_by_week_colum+days_schedule)
    df = pd.DataFrame(data,columns = columnas, index= range(1,len(solution.vigilantes_schedule)+1))
    df.index.name = "Vigilant"
    df.to_excel(writer, sheet_name='vig')
    wb.save(path+".xlsx")
    writer.close()
