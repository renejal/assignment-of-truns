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
        evolutions = dataGrasp.get("evolutions")
        bestPopulationIndex = len(evolutions)-1
        for index, solution in enumerate(evolutions[bestPopulationIndex]):
            generate_excel_site(
                solution, path+"/grasp/siteSolution"+str(index))
            generate_excel_vigilantes(
                solution, path+"/grasp/vigilantSolution"+str(index))
        dataGrasp.get("fig").write_image(path+"/figGrasp.png")
        dataGrasp.get("fig").write_html(path+"/figGraspHtml.html")
    if(dataNsga != None):
        os.makedirs(path+"/nsgaii")
        evolutions = dataNsga.get("evolutions")
        bestPopulationIndex = len(evolutions)-1
        for index, solution in enumerate(evolutions[bestPopulationIndex]):
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
    colums = ["evolution", "solution"]
    fitnessesGrasp = None
    fitnessesNsga = None

    if dataGrasp != None:
        colums.extend(["turnosFalGrasp", "vigilantesExGrasp", "horasExFrasp", "distanceGrasp"])
        fitnessesGrasp = dataGrasp.get("fitnesses")
    if dataNsga != None:
        colums.extend(["turnosFalNsgaII", "vigilantesExNsgaII", "horasExNsgaII", "distanceNsgaII"])
        fitnessesNsga = dataNsga.get("fitnesses")

    data = []
    if dataGrasp != None and dataNsga != None: 
        colums.extend(["hvGrasp","hvNsgaII","igdGrasp","igdNsgaII","timeGrasp","timeNsgaII"])
        amountEvolutionGrasp = len(fitnessesGrasp)
        amountEvolutionNSGA = len(fitnessesNsga)
        maxEvolution = amountEvolutionGrasp if amountEvolutionGrasp > amountEvolutionNSGA else amountEvolutionNSGA
        for i in range(maxEvolution):
            populationGrasp = fitnessesGrasp[i] if i < amountEvolutionGrasp else None
            populationNSGA = fitnessesNsga[i] if i < amountEvolutionNSGA else None
            amountPopulationGrasp = len(populationGrasp) if populationGrasp != None else 0
            amountPopulationNSGA = len(populationNSGA) if populationNSGA != None else 0
            if amountPopulationGrasp >= amountPopulationNSGA:
                for s in range(amountPopulationGrasp):
                    fitnessShiftNsga =  fitnessesNsga[i][s][0] if s < amountPopulationNSGA and populationNSGA != None  else None
                    fitnessVigilantsNsga = fitnessesNsga[i][s][1] if s < amountPopulationNSGA and populationNSGA != None else None
                    fitnessHoursNsga = fitnessesNsga[i][s][2] if s < amountPopulationNSGA and populationNSGA != None else None
                    fitnessDistanceNsga = fitnessesNsga[i][s][3] if s < amountPopulationNSGA and populationNSGA != None else None
                    hvNsga = dataNsga.get("hv")[i] if s < amountPopulationNSGA and populationNSGA != None else None
                    igdNsga = dataNsga.get("igd")[i] if s < amountPopulationNSGA and populationNSGA != None else None
                    data.append([i, s+1, fitnessesGrasp[i][s][0], fitnessesGrasp[i][s][1], fitnessesGrasp[i][s][2], fitnessesGrasp[i][s][3]
                        , fitnessShiftNsga, fitnessVigilantsNsga, fitnessHoursNsga, fitnessDistanceNsga,
                        dataGrasp.get("hv")[i], hvNsga, dataGrasp.get("igd")[i], igdNsga, dataGrasp.get("time"), dataNsga.get("time")
                    ])
            else:
                for s in range(amountPopulationNSGA):
                    fitnessShiftGRASP =  fitnessesGrasp[i][s][0] if s < amountPopulationGrasp and populationGrasp != None else None
                    fitnessVigilantsGRASP = fitnessesGrasp[i][s][1] if s < amountPopulationGrasp and populationGrasp != None else None
                    fitnessHoursGRASP = fitnessesGrasp[i][s][2] if s < amountPopulationGrasp and populationGrasp != None else None
                    fitnessDistanceGRASP = fitnessesGrasp[i][s][3] if s < amountPopulationGrasp and populationGrasp != None else None
                    hvGrasp = dataGrasp.get("hv")[i] if s < amountPopulationGrasp and populationGrasp != None else None
                    igdGrasp = dataGrasp.get("igd")[i] if s < amountPopulationGrasp and populationGrasp != None else None
                    data.append([i, s+1, fitnessShiftGRASP, fitnessVigilantsGRASP, fitnessHoursGRASP, fitnessDistanceGRASP
                        , fitnessesNsga[i][s][0], fitnessesNsga[i][s][1], fitnessesNsga[i][s][2], fitnessesNsga[i][s][3],
                        hvGrasp,  dataNsga.get("hv")[i], igdGrasp,  dataNsga.get("hv")[i], dataGrasp.get("time"), dataNsga.get("time")
                    ])
    
    elif dataGrasp != None and dataNsga ==  None:
        colums.extend(["hvGrasp","igdGrasp","timeGrasp"])
        for i, fitnessesPopulation in enumerate(fitnessesGrasp):
            for s, fitnessSolution in enumerate(fitnessesPopulation):
                data.append([i,s+1, fitnessSolution[0], fitnessSolution[1], fitnessSolution[2],
                        fitnessSolution[3], dataGrasp.get("hv")[i], dataGrasp.get("igd")[i], dataGrasp.get("time")])
    else:
        colums.extend(["hvNsgaII","igdNsgaII","timeNsgaII"])
        for i, fitnessesPopulation in enumerate(fitnessesNsga):
                    for s, fitnessSolution in enumerate(fitnessesPopulation):
                        data.append([i,s+1, fitnessSolution[0], fitnessSolution[1], fitnessSolution[2],
                                fitnessSolution[3], dataNsga.get("hv")[i], dataNsga.get("igd")[i], dataNsga.get("time")])
    df = pd.DataFrame(data, columns=colums)
    df.to_excel(writer, sheet_name='metrics')
    wb.save(path+"/metrics.xlsx")
    writer.close()
