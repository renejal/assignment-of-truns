from views.general_shift_view import GenerateShiftView
#Minimizar la cantidad de turnos faltantes.
#Minimzar la distancia del vigilante al puesto de trabajo.
#Minimizar la cantidad de guardias a utilizar para el problema.
#Minimizar numero de horas extras trabajadas.
from dominio.model.site import Site
# Separar el fitness por funcion objetivo
view = GenerateShiftView("views/sites2.json","views/vigilantes.json")
view.execute()
#Validara como calcular el fitness
