import pandas as pd

from dominio.Solution import Solution

PATH_FILE: str = "./results/Vigilantes.xlsx"
TOTAL_HOURS: int = 24

def generate_excel_vigilantes(solution: Solution):
    writer = pd.ExcelWriter(PATH_FILE, engine='openpyxl')
    wb = writer.book
    columnas = ["Hours Week"] + list("day"+str(day) for day in range(1,solution.problem.max_total_weeks*7+1))
    data = []
    for vigilant in solution.vigilantes_schedule:
        hours_by_week_colum = [vigilant.total_hours_worked_by_week]
        days_schedule= [[]]*solution.problem.max_total_weeks*7
        for shift in vigilant.shifts:
            start_day = int(shift.shift_start/TOTAL_HOURS)
            end_day =  int(shift.shift_end/TOTAL_HOURS)
            if start_day == end_day:
                days_schedule[start_day] = [vigilant.shifts[shift], [shift.shift_start - start_day*TOTAL_HOURS,shift.shift_end - start_day*TOTAL_HOURS]]
            else:
                pass
        data.append(hours_by_week_colum+days_schedule)
    df = pd.DataFrame(data,columns = columnas, index= range(1,len(solution.vigilantes_schedule)+1))
    df.index.name = "Vigilant"
    df.to_excel(writer, sheet_name='vig')
    wb.save(PATH_FILE)
    writer.close()
