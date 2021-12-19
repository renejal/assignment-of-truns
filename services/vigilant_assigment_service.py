
from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant


class Vigilant_assigment_service:

    def is_vigilant_avaible(self,vigilant: Vigilant, shift:Shift) -> bool:
        if self.is_available_on_shift(shift) == False:
            return False           
    
    def isVigilantAvailable(self,startPeriod,endPeriod,maxWorkHoursPerWeek):
        if self.hasEnoughHoursToWorkInThisShift(startPeriod,endPeriod,maxWorkHoursPerWeek) == False:
            return False
        if self.is_available_on_shift(startPeriod,endPeriod) == False:
            return False        
        return self.canWorkThisSunday(startPeriod,endPeriod)
    
    def is_available_on_shift(self,vigilant: Vigilant,shift: Shift):
        if len(vigilant.shifts) ==0:
            return True
        for index,assigned_shift in enumerate(vigilant.shifts):
            if shift.shift_end < assigned_shift.shift_start:
                if index > 0:
                    return shift.shift_end + 18 <  assigned_shift.shift_start and shift.shift_start - 18 > vigilant.shifts[index].shift_end
                return shift.shift_end + 18 <  assigned_shift.shift_start
        return shift.shift_start - 18 > vigilant.shifts[index].shift_end


     #Check restrictions   
    def hasEnoughHoursToWorkInThisShift(self,startPeriod,endPeriod,maxHours):
        weekStarPeriod = math.floor(startPeriod/168)
        weekEndPeriod  =  math.floor(endPeriod/168)
        if weekStarPeriod == weekEndPeriod:
            if  (self.HoursWeeks[weekStarPeriod]+(endPeriod - startPeriod)) <= maxHours:
                return True
            return False
        else:
            if (self.HoursWeeks[weekStarPeriod]+(168*weekEndPeriod)-startPeriod) <= maxHours and (self.HoursWeeks[weekEndPeriod]+endPeriod-(168*weekEndPeriod)) <= maxHours:
                return True
        return False
    
    def canWorkThisSunday(self,startPeriod,endPeriod):
        weekToCheck = math.floor(startPeriod/168)
        if self.thereIsAPeriodInSunday(startPeriod,endPeriod,weekToCheck):
            return self.workLastSunday(weekToCheck)
        return True
    
    def workLastSunday(self,week):
        if week == 0:
            return True
        for period in range (168*week,(168*week)-24,-1):
            if self.shifts[period] != 0:
                return False
        return True
    
    def thereIsAPeriodInSunday(self,startPeriod,endPeriod,week):
        if (startPeriod > 144+ (168*week) and startPeriod < 168*(week+1)):
            return True
        else:
            if (endPeriod > 144+ (168*week)):
              return True
        return False
   

    @staticmethod
    def get_possible_vigilant_to_assign(siteId, shifts):
        necesaryVigilantsByPeriodInAWeek = Vigilant_assigment_service.get_necesary_vigilants_by_period_in_a_week(shifts, vigilantesByPeriod)
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

    def get_necesary_vigilants_by_period_in_a_week(self, shifts, vigilantesByPeriod):
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