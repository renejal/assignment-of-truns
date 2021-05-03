from VigilantAssigment import *
import random

problem = VigilantAssigment()
solution = []
for vigilant in range(0,1):
    shifts = []
    for period in range(0,168*4):
        #sitio = random.randint(0,1)
        sitio = 1
        if sitio != 0:
            problem.addVigilant(sitio-1,period,vigilant)
        shifts.append(sitio)
    solution.append(shifts)
problem.evalute(solution)


# = 0
#for place in shifts:
#    for turno in place:
#        pos += 1
#        print(str(pos)+ " " +str(turno.getCantAssigmentVigilants()))
        
