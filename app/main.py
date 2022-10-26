import random
from conf.settings import SEEDS
from dominio.model.problem import DataUser
from views.general_shift_view import GenerateShiftView
from utils.print_xls import generate_results

class Main:
    def __init__(self,data) -> None:   
        random.seed(SEEDS[0])   
        view = GenerateShiftView(data, None)
        dataGrasp = None
        dataNsga = None
        # dataNsga = view.executeNsga()
        dataGrasp = view.executeGrasp()
        generate_results(dataGrasp,dataNsga,DataUser.from_dict(data).id_user)
        print("exit")







