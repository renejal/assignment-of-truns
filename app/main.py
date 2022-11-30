from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import random
import time
from utils.non_dominated_sorting import NonDominatedSorting
from conf.settings import SEEDS,MAX_TIME_DURATION
from dominio.model.problem import DataUser
from views.general_shift_view import GenerateShiftView
from utils.print_xls import generate_results
from nds import ndomsort
from services.reference_point import Reference_point
from utils.hipervolumen import Hipervolumen
from utils.igd import IGD
import numpy as np



class Main:
    def __init__(self,data) -> None: 

          
       
        random.seed(SEEDS[0])   
        view = GenerateShiftView(data, MAX_TIME_DURATION)
        # # dataGrasp = None
        # # dataNsga = None
        # dataNsga = view.executeNsga()
        # dataGrasp = view.executeGrasp()
        # generate_results(dataGrasp,dataNsga,DataUser.from_dict(data).id_user)
        # generate_results(dataGrasp,None,DataUser.from_dict(data).id_user)
        # filesData = ['facil-fulltime.json','facil-parcial.json','medio-fulltime.json','medio-parcial.json','hard-fulltime.json','hard-parcial.json']
        filesData = ['datareal.json']
        casos = []
        for file in filesData:
            datanew = open('./dataset/casoreal/'+file)
            datanew = json.load(datanew)
            casos.append(datanew)
        self.pruebaGrasp(casos)
        self.pruebaNSGA(casos)
        print("exit")


    def pruebaNSGA(self, casos):
        executor = ThreadPoolExecutor(max_workers=30)
        argsList = []
        responses = []
        sol = 0
        for i in range(1):
            for data in casos:
                view = GenerateShiftView(data, MAX_TIME_DURATION)
                argsList.append([view,i])
        futures = [executor.submit(self.executeNSGA, view[0], view[1]) for view in argsList]
        for future in as_completed(futures):
            sol+=1
            # get the result for the next completed task
            response = future.result()
            responses.append(response)
            print("Finalizo metodo Nsga")
        executor.shutdown() # blocks
        print("paso shutdown")
        for i in responses:
            print("entro")
            generate_results(None,i,DataUser.from_dict(data).id_user)
        print("Finalizo metodo Nsga")

    def pruebaGrasp(self, casos):
        executor = ThreadPoolExecutor(max_workers=30)
        argsList = []
        responses = []
        sol = 0
        for i in range(1):
            for data in casos:
                view = GenerateShiftView(data, MAX_TIME_DURATION)
                argsList.append([view,i])
        futures = [executor.submit(self.executeGrasp, view[0], view[1]) for view in argsList]
        futures =+ [executor.submit(self.executeNSGA, view[0], view[1]) for view in argsList]
        for future in as_completed(futures):
            sol+=1
            # get the result for the next completed task
            response = future.result()
            responses.append(response)
            print("Finalizo metodo GRasp")
        executor.shutdown() # blocks
        print("paso shutdown")
        for i in responses:
            print("entro")
            generate_results(i,None,DataUser.from_dict(data).id_user)
        print("termino")

    def execute_algoritm(self, view: GenerateShiftView, seed):
        result = []
        result.append(view.executeGrasp())
        result.append(view.executeNsga())
        return result

    def executeGrasp(self, view: GenerateShiftView, seed):
        random.seed(SEEDS[seed])   
        return view.executeGrasp()
    
    def executeNSGA(self, view: GenerateShiftView, seed):
        random.seed(SEEDS[seed])   
        return view.executeNsga()


    def calculateMetrics():
        reference_points_IGD = Reference_point().get_reference_points_from_IGD()
        data = [[0.000,0.063,0.506,0.036],
            [0.000,0.073,0.485,0.036],
]
        index = 0
        fitness = []
        solucion = 0
        evoluciones = []
        for i in data:
            evoluciones.append(i)
            solucion+=1
            if solucion == 10:
             fitness.append(evoluciones)
             solucion = 0
             evoluciones = []
        paretoFronts = []

        strings = ""
        for index,i in enumerate(fitness):
            fronts = ndomsort.non_domin_sort(i)
            strings+= str(index) + ","
            front = np.array(fronts[0])
            if index == 93:
                print(fronts[0])
            strings+= str(Hipervolumen.calculate_hipervolumen(front))+ ","
            strings+= str(IGD.calculate_igd(front, reference_points_IGD))+ "\n"
            # for sol in fronts[0]:
            #     for obj in sol:
            #         strings+= str(obj)+ ","
            #     strings+= str(index) + "\n"
            # paretoFronts.append(fronts[0])
        # print(paretoFronts)
        f = open("app/dataset/front"+".txt", "w")
        f.write(strings)
        f.close()