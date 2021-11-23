from typing import List
from data.SiteDataFile import SiteDataFile
from data.VigilantsDataFile import VigilantsDataFile
from dominio.Site import Site
from dominio.Vigilant import Vigilant
import operator

class VigilantAssigment:

    __total_vigilantes = 0
    totalPlaces=0 
    __total_weeks: int 
    totalPeriods=0

    __vigilants: List[Vigilant]
    
    maxShiftDuration: int = 12
    minShiftDuration: int = 4
    minBreakDuration: int = 18
    maxOvertimeWorkHoursPerWeek=12
    maxWorkHoursPerWeek=48
    minWorkHoursPerWeek=40
    idealWorkHoursPerWeek=48

    periodEndByWeek = []
    cantVigilantsByPeriod = []
    vigilantes = []
    cantNecesaryVigilantesforSite = {}
    workingDay={}
    __working_day_permanet = None

    specialSites={}
    vigilantExpectedPlaces = {}
    vigilantsWithOutPreference = []
    orderSitesForCantVigilantes = []
    obj_site_data_file: SiteDataFile = None


    def __init__(self, pathInterface, pathVigilants, weeks):
        self.__total_weeks = weeks
        self.obj_site_data_file = None
        self.__workingDay = None
        self.totalPeriods = 168*self.totalWeeks
        self.readData(pathInterface,pathVigilants)
        self.initProblem()

    def __init__(self, vigilants : List[Vigilant], sites: List[Site] , weeks ) -> None:
        self.__vigilants = vigilants
        self.__sites = sites
        self.__total_weeks = weeks

    ##Le pertenece a otra clase
    def readData(self, pathInterface , pathVigilants):
        self.readDataInterface(pathInterface)
        self.readVigilantData(pathVigilants)
    ##Le pertenece a otra clase

    def readDataInterface(self,pathInterface):
        self.obj_site_data_file: SiteDataFile = SiteDataFile(pathInterface, self.totalWeeks)
        self.SitesData= self.obj_site_data_file.get_data_problem()
        self.__workingDay = self.obj_site_data_file.get_working_day()
        self.specialSites = self.obj_site_data_file.specialSites
        self.totalPlaces = len(self.SitesData)
    ##Le pertenece a otra clase

    def readVigilantData(self, pathVigilants):
        data = VigilantsDataFile(pathVigilants)
        self.VigilantsData = data.vigilantsInfo
        self.totalVigilantes = data.numberVigilants

    def initProblem(self):
        #self.identifiesWeekStartPeriod()
        self.getCantVigilantesforSite()
        #init vigilantes and shift default
        for i in range(self.totalVigilantes):
            objVigilant = Vigilant(self.VigilantsData[i][0],self.VigilantsData[i][1],self.VigilantsData[i][2],self.VigilantsData[i][3],self.totalWeeks)
            if self.VigilantsData[i][1] != 0:
                if (self.VigilantsData[i][1] in self.vigilantExpectedPlaces) == False:
                    self.vigilantExpectedPlaces[self.VigilantsData[i][1]] = [objVigilant.id]
                else:
                    self.vigilantExpectedPlaces[self.VigilantsData[i][1]].append(objVigilant.id)
            self.vigilantes.append(objVigilant)
            if len(objVigilant.shiftPreferences) == 0:
                self.vigilantsWithOutPreference.append(objVigilant.id)
        self.OrderSitesForCantVigilantes()
        self.loadWorkingDay()
    
    ##eliminado
    def identifiesWeekStartPeriod(self):
        '''
        identify the shift the init for the week
        '''
        for i in range(0, self.totalWeeks):
            self.periodEndByWeek.append((i + 1) * 168)

    def getCantVigilantesforSite(self):
        indexSite = 1
        for place in self.SitesData:
            cantVigilantByPeriod = []
            sum = 0
            for cantByperiod in place:
                cantVigilantByPeriod.append(cantByperiod)
                sum = sum + cantByperiod
            self.cantVigilantsByPeriod.append(cantVigilantByPeriod)
            self.cantNecesaryVigilantesforSite[indexSite] = sum
            indexSite += 1

    def OrderSitesForCantVigilantes(self):
        sites = self.cantNecesaryVigilantesforSite
        sites = sorted(sites.items(), key=operator.itemgetter(1), reverse=True)
        site = []
        for i in sites:
            site.append(int(i[0]))
        self.orderSitesForCantVigilantes = site

    def loadWorkingDay(self):
        self.workingDay = { 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6], 7:[7],8:[8],9:[9],10:[10],11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],20:[10,10],21:[7,7,7],22:[8,7,7],
                      23:[8,8,7],24:[8,8,8]}

    def get_working_day_with_constraints(self, key, site):
        response = self.workingDay[key]
        if self.__workingDay[site-1] != 0:
            response = [self.__workingDay[site-1]]
        return response


    def getSite(self, siteId):
        return self.SitesData[siteId-1]


    def get_workig_day(self):
        return self.__workingDay