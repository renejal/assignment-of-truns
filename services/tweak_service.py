class tweak_service:

    @staticmethod
    def Tweak(self, solution):
        solution = self.tweakMissingShifts(solution, True)
        self.__problem.maxWorkHoursPerWeek = 56
        solution = self.tweakMissingShifts(solution, False)
        self.__problem.maxWorkHoursPerWeek = 48
        #solution = self.tweakVigilants(solution)
        self.calculateFitness(solution)
        return solution
    
    def tweakMissingShifts(self, solution, order):
        solution = self.tweakMissingHoursVigilants(solution,order)
        return solution

    def tweakVigilants(self, solucion):
        if self.is_empty(solucion.vigilantesForPlaces):
            listSite = aleatory.getAleatory(0, len(solucion.vigilantesForPlaces)-1, 2)
            vigilantOne = aleatory.getAleatory(0, len(solucion.vigilantesForPlaces[listSite[0]]), 1)
            vigilantTwo = aleatory.getAleatory(0, len(solucion.vigilantesForPlaces[listSite[1]]), 1)
            self.toExchageVigilants(listSite[0], vigilantOne[0], listSite[1], vigilantTwo[0], solucion)
        return solucion


    def tweakMissingHoursVigilants(self,solution,order):
        vigilantesByHours = self.GetVigilatsByHours(solution.vigilantesSchedule)
        vigilantesByHours = collections.OrderedDict(
            sorted(vigilantesByHours.items(), reverse=order))
        listTempVigilant = []
        for indexSite in range(0, len(self.missingShiftsBySite)):
            for shift in self.missingShiftsBySite[indexSite]:
                listTempVigilant.clear()
                cantNecessariVigilantsInShift = self.__problem.cantVigilantsByPeriod[indexSite][shift[0]] - len(
                    self.sitesSchedule[indexSite][shift[0]])
                numberIterations = cantNecessariVigilantsInShift
                for i in range(0, numberIterations):
                    objViglant = self.getAvaibleVigilant(
                        shift[0], shift[1], listTempVigilant, vigilantesByHours.values())
                    if objViglant == None:
                        continue
                    objViglant.setShifts(shift, indexSite+1)
                    cantNecessariVigilantsInShift -= 1
                    for i in range(shift[0], shift[1]+1):
                        solution.sitesSchedule[indexSite][i].append(
                            objViglant.id)
                        # solution.Fitness-=10000
                    listTempVigilant.append(objViglant)
                if cantNecessariVigilantsInShift == 0:
                    self.missingShiftsBySite[indexSite].remove(shift)
                self.updateHours(shift, listTempVigilant)
                # for vigilan in listTempVigilant:
                #     for week in vigilan.HoursWeeks:
                #         if week > 48:
                #             solution.Fitness+= (week-48)*100
        return solution
    

    # def missingShiftsFormat(self, missingShiftsBySite):
    #     shiftsFormat = []
    #     for missingShiftsInSite in missingShiftsBySite:
    #         shifts = []
    #         nHoras = 0
    #         if missingShiftsInSite:
    #             indexShift = 0
    #             cantMissingShifts = len(missingShiftsInSite)
    #             for i in range(0, cantMissingShifts-1):
    #                 if missingShiftsInSite[i]+1 != missingShiftsInSite[i+1] or nHoras == 23 or i == cantMissingShifts-2:

    #                     nHoras += 1
    #                     shifts = shifts + \
    #                         self.calculateworkinday(
    #                             self.__problem.workingDay[nHoras], missingShiftsInSite[indexShift])
    #                     indexShift += nHoras
    #                     nHoras = 0
    #                 else:
    #                     nHoras += 1
    #             shifts[len(shifts)-1][1] += 1
    #         shiftsFormat.append(shifts)
    #     self.missingShiftsBySite = shiftsFormat

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

    def GetVigilatsByHours(self, vigilantes):
        vigilantByHours = {}
        for vigilant in vigilantes:
            if vigilant.HoursWorked in vigilantByHours:
                vigilantByHours[vigilant.HoursWorked].append(vigilant)
            else:
                vigilantByHours[vigilant.HoursWorked] = [vigilant]
        return vigilantByHours