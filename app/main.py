from tkinter.messagebox import NO
from views.general_shift_view import GenerateShiftView
from utils.print_xls import generate_results

class Main:
    def __init__(self,data) -> None:    
        view = GenerateShiftView(data)
        dataGrasp = view.executeGrasp()
        dataNsga = view.executeNsga()
        print(dataGrasp)
        print(dataNsga)
        # dataNsga = None
        # generate_results(dataGrasp,dataNsga,data.idUser)







