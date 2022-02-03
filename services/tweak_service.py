from dominio.Solution import Solution
from services.tweak_extra_hours import Tweak_extra_hours
from utils import aleatory
from services.tweak_missing_shifts import Tweak_missing_shifts

class Tweak_service:

    tweak_missing_shifts: Tweak_missing_shifts = Tweak_missing_shifts()
    tweak_extra_hours: Tweak_extra_hours = Tweak_extra_hours()

    def Tweak(self, solution: Solution):
        solution = self.tweak_missing_shifts.missing_shifts_tweak(solution) 
        # solution.calculate_fitness()
        solution = self.tweak_extra_hours.extra_hours_tweak(solution)
        solution.calculate_fitness()

        #solution = self.tweakVigilants(solution)
        #self.calculateFitness(solution)
        return solution
    
   
    def tweakVigilants(self, solucion):
        if self.is_empty(solucion.vigilantesForPlaces):
            listSite = aleatory.get_aleatory(0, len(solucion.vigilantesForPlaces) - 1, 2)
            vigilantOne = aleatory.get_aleatory(0, len(solucion.vigilantesForPlaces[listSite[0]]), 1)
            vigilantTwo = aleatory.get_aleatory(0, len(solucion.vigilantesForPlaces[listSite[1]]), 1)
            self.toExchageVigilants(listSite[0], vigilantOne[0], listSite[1], vigilantTwo[0], solucion)
        return solucion
 

    def toExchageVigilants(self, parIdSiteOne, parIdVigilantOne, parIdSiteTwo, parIdVigilantsTwo,solucion):
        '''
        to Exchage vigilantes between sites
        :param parSiteOne: site one select ramdoly
        :param parVigilantOne: vigilant one select the site one ramdoly
        :param parSiteTwo:
        :param parVigilantsTwo:
        :return: None
        '''
        try:
            objVigilantOne = solucion.vigilantesForPlaces.get(parIdSiteOne)[
                parIdVigilantOne]
            objVigilantTwo = solucion.vigilantesForPlaces.get(parIdSiteOne)[
                parIdVigilantOne]
            self.updateFitnees(objVigilantOne, parIdSiteOne,
                               parIdSiteTwo, solucion)
            self.updateFitnees(objVigilantTwo, parIdSiteTwo,
                               parIdSiteOne, solucion)
            temVigilanOne = solucion.vigilantesForPlaces.get(parIdSiteOne)[
                parIdVigilantOne]
            solucion.vigilantesForPlaces.get(parIdSiteOne)[
                parIdVigilantOne] = solucion.vigilantesForPlaces.get(parIdSiteTwo)[parIdVigilantsTwo]
            solucion.vigilantesForPlaces.get(
                parIdSiteTwo)[parIdVigilantsTwo] = temVigilanOne
        except:
            print("exception")
    
    def getAleatory(self, parInit, parEnd, parNumber):
        '''
        generate n number aleatory between  nunber init and number end
        :param init: number init
        :param end: number end
        :param number: quantity the number aleatory
        :return: list number aleatory
        '''
        k = 0
        listAleatory = []
        while True:
            if parNumber > k:
                numAleatory = random.randint(parInit, parEnd)
                if numAleatory not in listAleatory:
                    listAleatory.append(numAleatory)
                    k = k+1
            else:
                break
        return listAleatory
    
    def is_empty(self, list):
        varResult = True
        for i in list:
            if i is None:
                varResult = False
                break
        return varResult