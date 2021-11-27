from typing import List
from dominio.Component import Component
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift
import random

class generate_site_schedule_service:
    
    @staticmethod
    def getSchedule(self,component: Component, shifts: List[Shift] , possibleVigilantsToAssign: List[Vigilant]):
            assignedVigilantsInActualShift: List[Vigilant] = []
            for shift in shifts:
                assignedVigilantsInActualShift.clear()
                for iteration in range(0, shift.__necesary_vigilantes):
                    vigilant = self.getAvaibleVigilant(shift, assignedVigilantsInActualShift, possibleVigilantsToAssign)
                    if vigilant == None:
                        continue
                    self.assignVigilant(vigilant, shift, component)
                    assignedVigilantsInActualShift.append(vigilant)
            
    def assignVigilant(self, objVigilant, site, shift, component: Component):
            """
            assigment vigilantes with constraint number hours permanent for sites
            """

            if objVigilant not in component.assignedVigilants:
                component.assignedVigilants.append(objVigilant)

            """udpate shifts sites whit vigilantes"""

            for i in range(shift[0], shift[1]+1):
                objVigilant.setShift(i, site)
                component.siteSchedule[i].append(objVigilant.id)
        
    def getAvaibleVigilant(self, shift: Shift, assignedVigilantsInShift, vigilantList: List[List[Vigilant]]):
            ObjResultado = None
            for vigilantes in vigilantList:
                indexVigilants = [*range(len(vigilantes))]
                while indexVigilants:
                    rand = random.choice(indexVigilants)
                    objVigilant = vigilantes[rand]
                    if objVigilant not in assignedVigilantsInShift and objVigilant.isVigilantAvailable(shift , self.__problem.maxWorkHoursPerWeek):
                        ObjResultado = objVigilant
                        return ObjResultado
                    indexVigilants.remove(rand)
            return ObjResultado

   
