from dominio.model.problem import DataUser
from views.general_shift_view import GenerateShiftView
from utils.print_xls import generate_results

class Main:
    def __init__(self,data) -> None:  
        view = GenerateShiftView(data)
        dataGrasp = view.executeGrasp()
        # dataNsga = view.executeNsga()
        # dataNsga = None
        # generate_results(dataGrasp,dataNsga,DataUser.from_dict(data).id_user)







