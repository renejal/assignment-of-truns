from typing import Dict, List
from data.SiteDataFile import SiteDataFile
from data.VigilantsDataFile import VigilantsDataFile
from dominio.Shift import Shift
from dominio.Site import Site
from dominio.Vigilant3 import Vigilant
import operator

class VigilantAssigment:
    # maxShiftDuration: int = 12
    # minShiftDuration: int = 4
    # minBreakDuration: int = 18
    # maxOvertimeWorkHoursPerWeek=12
    # maxWorkHoursPerWeek=48
    # minWorkHoursPerWeek=40
    # idealWorkHoursPerWeek=48

    __vigilants: List[Vigilant]
    __sites: List[Site]
    __total_vigilantes: int
    __total_sites: int
    __total_weeks: int 
    __vigilantExpectedPlaces: Dict[int , List[int]]
    __order_sites_by_vigilants_amount: List[int]
        

    def __init__(self, vigilants : List[Vigilant], sites: List[Site] , weeks ) -> None:
        self.__vigilants = vigilants
        self.__sites = sites
        self.__total_weeks = weeks
        # TO DO OrderSites 
        self.initProblem()

    def initProblem(self) -> None:
        for vigilant in self.__vigilants:
            if vigilant.__expected_place_to_work !=0:
                if vigilant.__expected_place_to_work in self.__vigilantExpectedPlaces:
                    self.__vigilantExpectedPlaces[vigilant.__expected_place_to_work].apppend(vigilant.__vigilant_id)
                else:
                    self.__vigilantExpectedPlaces[vigilant.__expected_place_to_work]= vigilant.__vigilant_id
        self.createShiftsBySite()
        self.OrderSitesForCantVigilantes()

    def createShiftsBySite() -> List[List[Shift]]:
        workingDay = self.loadWorkingDay()
        return None
    def getShiftsBySite() -> List[Shift]:
        return None

    def getCantVigilantesforSite(self):
        cantNecesaryVigilantesforSite = {}
        indexSite = 1
        for place in self.SitesData:
            cantVigilantByPeriod = []
            sum = 0
            for cantByperiod in place:
                cantVigilantByPeriod.append(cantByperiod)
                sum = sum + cantByperiod
            self.cantVigilantsByPeriod.append(cantVigilantByPeriod)
            cantNecesaryVigilantesforSite[indexSite] = sum
            indexSite += 1
        return cantNecesaryVigilantesforSite

    def get_order_site_by_vigilants_amount()-> int:
        return None

    def OrderSitesForCantVigilantes(self):
        sites = self.getCantVigilantesforSite()
        sites = sorted(sites.items(), key=operator.itemgetter(1), reverse=True)
        site = []
        for i in sites:
            site.append(int(i[0]))
        self.__order_sites_by_vigilants_amount = site

    def loadWorkingDay(self) -> Dict[int,List[int]]: 
        return { 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6], 7:[7],8:[8],9:[9],10:[10],11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],20:[10,10],21:[7,7,7],22:[8,7,7],
                      23:[8,8,7],24:[8,8,8]}

    def get_working_day_with_constraints(self, key, site):
        response = self.workingDay[key]
        if self.__workingDay[site-1] != 0:
            response = [self.__workingDay[site-1]]
        return response


    def getSite(self, siteId):
        return self.SitesData[siteId-1]




    


     #PASARLO A VIGILANT ASSIGMNET
    def specialShifts(self, startWork, endWork, specialHours):
        shifts = []
        while(startWork < endWork):
            endHour = specialHours+startWork-1
            if(endHour+specialHours > endWork):
                endHour = endWork
            shifts.append([startWork, endHour])
            startWork = endHour+1
        return shifts
    #PASARLO A VIGILANT ASSIGMNET
    def getSpecialShifts(self, siteId,parSite):
        specialhours = self.__problem.specialSites[siteId]
        shifts = []
        start = -1
        working = 0
        for i in range(0, len(parSite)):
            if(parSite[i] != 0 and working + 1 != 24):
                if start == -1:
                    start = i
                working += 1
                if i == len(parSite)-1:
                    shifts += self.specialShifts(start, i, specialhours)
            elif(working > 0):
                if working == 23:
                    shifts += self.specialShifts(start, i, specialhours)
                else:
                    shifts += self.specialShifts(start, i-1, specialhours)
                start = -1
                working = 0
        return shifts
    #PASARLO A VIGILANT ASSIGMNET
    def obtainShiftBySite(self, siteId):
        parSite = self.__problem.getSite(siteId)
        if siteId in self.__problem.specialSites:
            return self.getSpecialShifts(siteId,parSite)
        else:
            site = np.copy(parSite)
            working_day = []
            init = -1
            start = False
            k = 0
            for index, t in enumerate(site):
                if t == 0 and start == False:
                    continue
                if t != 0:
                    if init == -1:
                        init = index
                    start = True
                    if k < 24:
                        k += 1

                if (t == 0 and start == True) or k == 24:
                    workindaytimes = self.__problem.workingDay[k]
                    if workindaytimes == None:
                        print(
                            "el numero de horas no puede establecerce a un vigilantes revice EL DATASET")
                    start = False
                    if workindaytimes == 9:
                        return
                    working_day = working_day + \
                        (self.calculateworkinday(workindaytimes, init))
                    init = -1
                    k = 0

            return working_day
    #PASARLO A VIGILANT ASSIGMNET
    def calculateworkinday(self, workinday, indexWorkingDay):
        dayShiftS = []
        for durationShift in workinday:
            dayShiftS.append(
                [indexWorkingDay, indexWorkingDay+durationShift-1])
            indexWorkingDay += durationShift
        return dayShiftS