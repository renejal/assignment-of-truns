from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import random
import time
from conf.settings import SEEDS,MAX_TIME_DURATION
from dominio.model.problem import DataUser
from views.general_shift_view import GenerateShiftView
from utils.print_xls import generate_results


class Main:
    def __init__(self,data = None) -> None:   
        filesData = ['facil-fulltime.json','facil-parcial.json','medio-fulltime.json','medio-parcial.json','hard-fulltime.json','hard-parcial.json']
        casos = []
        for file in filesData:
            datanew = open('./app/dataset/datosSinteticos/'+file)
            datanew = json.load(datanew)
            casos.append(datanew)
        # self.pruebaGrasp(casos)
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


    def executeGrasp(self, view: GenerateShiftView, seed):
        random.seed(SEEDS[seed])   
        return view.executeGrasp()
    
    def executeNSGA(self, view: GenerateShiftView, seed):
        random.seed(SEEDS[seed])   
        return view.executeNsga()


Main(None)