from dominio.model.problem import DataUser
from views.general_shift_view import GenerateShiftView
from utils.print_xls import generate_results
from utils.optimizerParameters import OptimizerParamets

class Main:
    def __init__(self,data) -> None:   

        view = GenerateShiftView(data)
        dataGrasp = view.executeGrasp()
        # dataNsga = view.executeNsga()
        # dataGrasp = None
        dataNsga = None
        # generate_results(dataGrasp,dataNsga,DataUser.from_dict(data).id_user)
        # OptimizerParamets().calculate_best_parameters(view)







