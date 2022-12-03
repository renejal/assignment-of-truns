import os
import pandas as pd
from conf.settings import MAX_TIME_DURATION
from utils.print_sites_xls import generate_excel_site
from utils.print_vigilants_xls import generate_excel_vigilantes
from conf.settings import PATH_RESULTS
from typing import Dict, List
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
    data = []

    if dataGrasp != None and dataNsga != None:
        colums.extend(["mShiftG","mShiftN","extraVigG","extraVigN","extraHoG","extraHoN","distanceG", "distanceN"])
        colums.extend(["hvGrasp","hvNsgaII","igdGrasp","igdNsgaII","timeGrasp","timeNsgaII"])
        fitnessesGrasp = dataGrasp.get("fitnesses")
        fitnessesNsga = dataNsga.get("fitnesses")
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
                        hvGrasp,  dataNsga.get("hv")[i], igdGrasp,  dataNsga.get("igd")[i], dataGrasp.get("time"), dataNsga.get("time")
                    ])
    
    elif dataGrasp != None and dataNsga ==  None:
        colums.extend(["mShiftG", "extraVigG", "extraHoG", "distanceG","hvGrasp","igdGrasp","timeGrasp"])
        fitnessesGrasp = dataGrasp.get("fitnesses")
        for i, fitnessesPopulation in enumerate(fitnessesGrasp):
            for s, fitnessSolution in enumerate(fitnessesPopulation):
                data.append([i,s+1, fitnessSolution[0], fitnessSolution[1], fitnessSolution[2],
                        fitnessSolution[3], dataGrasp.get("hv")[i], dataGrasp.get("igd")[i], dataGrasp.get("time")])
    else:
        colums.extend(["mShiftN", "extraVigN", "extraHoN", "distanceN","hvNsgaII","igdNsgaII","timeNsgaII"])
        fitnessesNsga = dataNsga.get("fitnesses")
        for i, fitnessesPopulation in enumerate(fitnessesNsga):
                    for s, fitnessSolution in enumerate(fitnessesPopulation):
                        data.append([i,s+1, fitnessSolution[0], fitnessSolution[1], fitnessSolution[2],
                                fitnessSolution[3], dataNsga.get("hv")[i], dataNsga.get("igd")[i], dataNsga.get("time")])
    df = pd.DataFrame(data, columns=colums)
    df.to_excel(writer, sheet_name ='metrics')
    worksheet = wb['metrics']
    columns  = worksheet.max_column
    rows = worksheet.max_row
    for c in range(4,columns+1):
        worksheet.column_dimensions[chr(c+63)].bestFit = True
        for r in range(2,rows+1):
            worksheet.cell(row=r, column=c).number_format = '0.000'

    wb.save(path+"/metrics.xlsx")
    writer.close()

def generate_parameter_optimizacion(evolutions: List[List[object]], data_solutions,columns, name):
    print("******************Entro a save*********************")
    time = datetime.datetime.now()
    time = str(time.year)+"-"+str(time.month)+"-"+str(time.day) + \
        "-"+str(time.hour)+"-"+str(time.minute)+"-"+str(time.second)
    path = PATH_RESULTS+"optimizations/"+name+time
    writer = pd.ExcelWriter(path +".xlsx", engine='openpyxl')
    data = []
    for p, population in enumerate(evolutions):
        for s in range(len(population[0])):
            list = [p+1,s+1]
            list.extend(population[0][s])
            list.append(MAX_TIME_DURATION)
            list.append(population[1][s])
            data.append(list)
    wb = writer.book
    df = pd.DataFrame(data,columns=columns)
    df.to_excel(writer, sheet_name ='optimizacion')
    print(f" se guardo en {path}.xlsx")
    wb.save(path+".xlsx")
    print("exitoso")
    writer.close()
    strings = ""
    for index,generation in enumerate(data_solutions):
        for solutionsData in generation:
            solutionsEvolution = solutionsData[0]
            hv_averageGa = solutionsData[1]
            indexSolutionGA = solutionsData[2]
            for solutions_normalize_fitnesss in solutionsEvolution:
                hvEvolution = solutions_normalize_fitnesss[1]
                for solution in solutions_normalize_fitnesss[0]:
                    string = ""
                    for fitness in solution:
                        string+= str(fitness) + ","
                    string+= str(hvEvolution)
                    string+= ","+str(indexSolutionGA)
                    string+= ","+str(hv_averageGa)
                    string+= ","+str(index)
                    strings+= string+"\n"
    f = open(path+".txt", "w")
    f.write(strings)
    f.close()

def generate_results(dataGrasp: Dict[str, object], dataNsga: Dict[str, object], idUser: str):
    time = datetime.datetime.now()
    time = str(time.year)+"-"+str(time.month)+"-"+str(time.day) + \
        "-"+str(time.hour)+"-"+str(time.minute)+"-"+str(time.second)
    path = PATH_RESULTS+idUser+"/empresaseguridad_normal/"+time
    if(dataGrasp != None):
        os.makedirs(path+"/grasp")
        evolutions = dataGrasp.get("evolutions")
        bestPopulationIndex = len(evolutions)-1
        for index, solution in enumerate(evolutions[bestPopulationIndex]):
            generate_excel_site(
                solution, path+"/grasp/siteSolution"+str(index))
            generate_excel_vigilantes(
                solution, path+"/grasp/vigilantSolution"+str(index))
        print("escribiendo imagenes Grasp")
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
        print("excribiendo imagenes Nsgaz")
        dataNsga.get("fig").write_image(path+"/figNsga.png")
        dataNsga.get("fig").write_html(path+"/figNsgaHtml.html")
    generate_metrics(dataGrasp, dataNsga, path)