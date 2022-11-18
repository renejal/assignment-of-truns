from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import time
from conf.settings import SEEDS,MAX_TIME_DURATION
from dominio.model.problem import DataUser
from views.general_shift_view import GenerateShiftView
from utils.print_xls import generate_results

class Main:
    def __init__(self,data) -> None:   
        random.seed(SEEDS[0])   
        # view = GenerateShiftView(data, MAX_TIME_DURATION)
        # dataGrasp = None
        # dataNsga = None
        # # dataNsga = view.executeNsga()
        # dataGrasp = view.executeGrasp()
        # generate_results(dataGrasp,dataNsga,DataUser.from_dict(data).id_user)
        self.pruebaGrasp(data)
        self.pruebaNSGA(data)
        print("exit")


    def pruebaNSGA(self, data):
        executor = ThreadPoolExecutor(max_workers=10)
        argsList = []
        responses = []
        for i in range(10):
            view = GenerateShiftView(data, MAX_TIME_DURATION)
            argsList.append([view,i])
        futures = [executor.submit(self.executeNSGA, view[0], view[1]) for view in argsList]
        for future in as_completed(futures):
            # get the result for the next completed task
            response = future.result()
            responses.append(response)
            print("Finalizo metodo")
            generate_results(response,None,DataUser.from_dict(data).id_user)
        executor.shutdown() # blocks
        for i in responses:
            generate_results(None,i,DataUser.from_dict(data).id_user)

    def pruebaGrasp(self, data):
        executor = ThreadPoolExecutor(max_workers=10)
        argsList = []
        responses = []
        sol = 0
        for i in range(10):
            view = GenerateShiftView(data, MAX_TIME_DURATION)
            argsList.append([view,i])
        futures = [executor.submit(self.executeGrasp, view[0], view[1]) for view in argsList]
        for future in as_completed(futures):
            sol+=1
            # get the result for the next completed task
            response = future.result()
            responses.append(response)
            print("Finalizo metodo")
        executor.shutdown() # blocks
        for i in responses:
            generate_results(i,None,DataUser.from_dict(data).id_user)


    def executeGrasp(self, view: GenerateShiftView, seed):
        random.seed(SEEDS[seed])   
        return view.executeGrasp()
    
    def executeNSGA(self, view: GenerateShiftView, seed):
        random.seed(SEEDS[seed])   
        return view.executeNsga()


