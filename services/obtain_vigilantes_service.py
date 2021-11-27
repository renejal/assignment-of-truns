class obtain_vigilantes_service:
    
    @staticmethod
    def getPossibleVigilantsToAssign(self, siteId, shifts):
        necesaryVigilantsByPeriodInAWeek = self.getNecesaryVigilantsByPeriodInAWeek(
            shifts, vigilantesByPeriod)
        cantNecesaryVigilantsInWeek = sum(necesaryVigilantsByPeriodInAWeek)
        porcentajeDeTrabajo = 3.5  # Un porcentaje obtenido de el trabajo promedio que se saca para una cantidad de turnos dependiendo de la cantidad usual de los dias que un guardia trabaja en el año
        cantVigilantsNecesaryInSite = math.floor(
            cantNecesaryVigilantsInWeek/porcentajeDeTrabajo)
        expectedvigilantesInPlace = []
        orderVigilantsByDistance = []
        if siteId in self.__problem.__vigilantExpectedPlaces:
            if len(self.__problem.__vigilantExpectedPlaces[siteId]) >= cantVigilantsNecesaryInSite:
                expectedvigilantesInPlace = self.__problem.__vigilantExpectedPlaces[siteId][:cantVigilantsNecesaryInSite].copy(
                )
            else:
                expectedvigilantesInPlace = self.__problem.__vigilantExpectedPlaces[siteId].copy(
                )
            for iteration in range(0, len(expectedvigilantesInPlace)):
                expectedvigilantesInPlace[iteration] = self.vigilantesSchedule[expectedvigilantesInPlace[iteration]-1]
            cantVigilantsNecesaryInSite -= len(expectedvigilantesInPlace)
        if cantVigilantsNecesaryInSite > 0:
            orderVigilantsInPlaceByDistance = self.orderVigilantsInPlaceByDistance(
                self.vigilantes, siteId)
            pos = 0
            while cantVigilantsNecesaryInSite > 0:
                if (orderVigilantsInPlaceByDistance[pos] in expectedvigilantesInPlace) == False:
                    orderVigilantsByDistance.append(
                        self.vigilantesSchedule[orderVigilantsInPlaceByDistance[pos].id-1])
                    cantVigilantsNecesaryInSite -= 1
                pos += 1
        return [expectedvigilantesInPlace, orderVigilantsByDistance]

    def getNecesaryVigilantsByPeriodInAWeek(self, shifts, vigilantesByPeriod):
        vigilantesByPeriodInAWeek = []
        for shift in shifts:
            if shift[0] > 168:
                break
            vigilantesByPeriodInAWeek.append(vigilantesByPeriod[shift[0]])
        return vigilantesByPeriodInAWeek

    def orderVigilantsInPlaceByDistance(self, vigilantes, place):
        for iteration in range(0, len(vigilantes)-1):
            swapped = False
            for pos in range(0, len(vigilantes)-1-iteration):
                if(vigilantes[pos + 1].distancesBetweenPlacesToWatch[place-1] < vigilantes[pos].distancesBetweenPlacesToWatch[place-1]):
                    aux = vigilantes[pos]
                    vigilantes[pos] = vigilantes[pos+1]
                    vigilantes[pos + 1] = aux
                    swapped = True
            if swapped == False:
                break
        return vigilant