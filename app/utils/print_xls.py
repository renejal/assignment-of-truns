import os
import pandas as pd
from utils.print_sites_xls import generate_excel_site
from utils.print_vigilants_xls import generate_excel_vigilantes
from conf.settings import PATH_RESULTS
from typing import Dict
import datetime


def generate_results(dataGrasp: Dict[str, object], dataNsga: Dict[str, object], idUser: str):
    time = datetime.datetime.now()
    time = str(time.year)+"-"+str(time.month)+"-"+str(time.day) + \
        "-"+str(time.hour)+"-"+str(time.minute)+"-"+str(time.second)
    path = PATH_RESULTS+idUser+"/"+time
    if(dataGrasp != None):
        os.makedirs(path+"/grasp")
        population = dataGrasp.get("population")
        graspLen = len(population)-1
        for index, solution in enumerate(population[graspLen]):
            generate_excel_site(
                solution, path+"/grasp/siteSolution"+str(index))
            generate_excel_vigilantes(
                solution, path+"/grasp/vigilantSolution"+str(index))
        dataGrasp.get("fig")[graspLen].write_image(path+"/figGrasp.png")
        dataGrasp.get("fig")[graspLen].write_html(path+"/figGraspHtml.html")
    if(dataNsga != None):
        os.makedirs(path+"/nsgaii")
        for index, solution in enumerate(dataNsga.get("solutions")):
            generate_excel_site(
                solution, path+"/nsgaii/siteSolution"+str(index))
            generate_excel_vigilantes(
                solution, path+"/nsgaii/vigilantSolution"+str(index))
        dataNsga.get("fig").write_image(path+"/figNsga.png")
        dataNsga.get("fig").write_html(path+"/figNsgaHtml.html")
    generate_metrics(dataGrasp, dataNsga, path)


def generate_metrics(dataGrasp: Dict[str, object], dataNsga: Dict[str, object], path: str) -> None:
    writer = pd.ExcelWriter(path+"/metrics.xlsx", engine='openpyxl')
    wb = writer.book
    colums = ["solution"]
    fitnesssGrasp = None
    fitnesssNsga = None
    amountPopulationGrasp = None
    amountPopulationNsga = None

    if dataGrasp != None:
        colums.extend(["turnosFalGrasp", "vigilantesExGrasp",
                      "horasExFrasp", "distanceGrasp"])
        fitnesssGrasp = dataGrasp.get("fitnesses")
        amountPopulationGrasp = len(fitnesssGrasp)
    if dataNsga != None:
        colums.extend(["turnosFalNsgaII", "vigilantesExNsgaII",
                      "horasExNsgaII", "distanceNsgaII"])
        fitnesssNsga = dataNsga.get("fitnesses")
        amountSolutions = len(fitnesssNsga)
    data = []
    if dataGrasp != None and dataNsga != None: 
        colums.extend(["hvGrasp","hvNsgaII","igdGrasp","igdNsgaII","timeGrasp","timeNsgaII"])
        for i in range(amountSolutions):
            data.append([i+1, fitnesssGrasp[i][0], fitnesssGrasp[i][1], fitnesssGrasp[i][2], fitnesssGrasp[i][3], 
            fitnesssNsga[i][0], fitnesssNsga[i][1], fitnesssNsga[i][2], fitnesssNsga[i][3], 
            dataGrasp.get("hv"), dataNsga.get("hv"), dataGrasp.get("igd"), dataNsga.get("igd"), dataGrasp.get("time"), dataNsga.get("time")
                    ])
    elif dataGrasp != None and dataNsga ==  None:
        colums.extend(["hvGrasp","igdGrasp","timeGrasp"])
        for i in range(amountSolutions):
            data.append([i+1, fitnesssGrasp[i][0], fitnesssGrasp[i][1], fitnesssGrasp[i][2],
                        fitnesssGrasp[i][3], dataGrasp.get("hv"), dataGrasp.get("igd"), dataGrasp.get("time")])
    else:
        colums.extend(["hvNsgaII","igdNsgaII","timeNsgaII"])
        for i in range(amountSolutions):
            data.append([i+1, fitnesssNsga[i][0], fitnesssNsga[i][1], fitnesssNsga[i][2],
                        fitnesssNsga[i][3], dataNsga.get("hv"), dataNsga.get("igd"), dataNsga.get("time")])
    df = pd.DataFrame(data, columns=colums)
    df.to_excel(writer, sheet_name='metrics')
    wb.save(path+"/metrics.xlsx")
    writer.close()
