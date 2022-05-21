import os
import pandas as pd
from utils.print_sites_xls import generate_excel_site
from utils.print_vigilants_xls import generate_excel_vigilantes
from conf.settings import PATH_RESULTS
from typing import Dict
import datetime


def generate_results(dataGrasp: Dict[str, object], dataNsga: Dict[str, object], idUser: str):
    time = datetime.datetime.now()
    time = str(time.year)+"-"+str(time.month)+"-"+str(time.day)+"-"+str(time.hour)+"-"+str(time.minute)+"-"+str(time.second)
    print(PATH_RESULTS, idUser, time)
    path = PATH_RESULTS+idUser+"/"+time
    if(dataGrasp != None):
        os.makedirs(path+"/grasp")
        for index, solution in enumerate(dataGrasp.get("solutions")):
            generate_excel_site(solution, path+"/grasp/siteSolution"+str(index))
            generate_excel_vigilantes(solution, path+"/grasp/vigilantSolution"+str(index))
    if(dataNsga != None):
        os.makedirs(path+"/nsgaii")
        for index, solution in enumerate(dataNsga.get("solutions")):
            generate_excel_site(solution, path+"/nsgaii/siteSolution"+str(index))
            generate_excel_vigilantes(solution, path+"/nsgaii/vigilantSolution"+str(index))
    print("FITNESS GRASP")
    print(dataGrasp.get("fitnesses"))
    # print("FITNESS NSGAII")
    # print(dataNsga.get("fitnesses"))
    # generate_metrics(dataGrasp, dataNsga, path)

def generate_metrics(dataGrasp: Dict[str, object], dataNsga: Dict[str, object],path:str) -> None:
    writer = pd.ExcelWriter(path+"/metrics.xlsx", engine='openpyxl')
    wb = writer.book
    colums= ["solution","turnosFalGrasp","vigilantesExGrasp","horasExFrasp","distanceGrasp",
    "turnosFalNsgaII","vigilantesExNsgaII","horasExNsgaII","distanceNsgaII","hvGrasp","hvNsgaII","igdGrasp","igdNsgaII","timeGrasp","timeNsgaII"]
    data = []
    fitnesssGrasp = dataGrasp.get("fitnesses")
    fitnesssNsga = dataNsga.get("fitnesses")
    for i in range(len(fitnesssGrasp)):
        data.append([i+1,fitnesssGrasp[i][0],fitnesssGrasp[i][1],fitnesssGrasp[i][2],fitnesssGrasp[i][3]
                ,fitnesssNsga[i][0],fitnesssNsga[i][1],fitnesssNsga[i][2],fitnesssNsga[i][3]
                ,dataGrasp.get("hv"), dataNsga.get("hv"),dataGrasp.get("igd"), dataNsga.get("igd")
                ,dataGrasp.get("time"), dataNsga.get("time")
        ])
    df = pd.DataFrame(data,columns=colums)
    df.to_excel(writer, sheet_name='metrics')
    wb.save(path+"/metrics.xlsx")
    writer.close()




