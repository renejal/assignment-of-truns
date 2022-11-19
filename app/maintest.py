from views.general_shift_view import GenerateShiftView

class Main:
    def __init__(self,data) -> None:    
        view = GenerateShiftView(data, None)
        view.executeNsga()

a = Main(None)
