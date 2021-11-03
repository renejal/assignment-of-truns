from data.SiteDataFile import SiteDataFile
from data.VigilantsDataFile import VigilantsDataFile
from dominio.Vigilant import Vigilant
import operator


class VigilantAssigment:
    totalVigilantes = 0
    totalPlaces=0 
    totalWeeks=0
    totalPeriods=0
    
    maxShiftDuration: int = 12
    minShiftDuration=6
    minBreakDuration=18
    maxOvertimeWorkHoursPerWeek=12
    maxWorkHoursPerWeek=48
    minWorkHoursPerWeek=40
    idealWorkHoursPerWeek=48

    periodEndByWeek = []
    cantVigilantsByPeriod = []
    vigilantes = []
    cantNecesaryVigilantesforSite = {}
    workingDay={}
    __workingDay = None

    vigilantExpectedPlaces = {}
    vigilantsWithOutPreference = []
    orderSitesForCantVigilantes = []
    obj_site_data_file: SiteDataFile = None


    def __init__(self, pathInterface, pathVigilants, weeks):
        self.totalWeeks = weeks
        self.obj_site_data_file = None
        self.__workingDay = None
        self.totalPeriods = 168*self.totalWeeks
        self.readData(pathInterface,pathVigilants)
        self.initProblem()

    def readData(self, pathInterface , pathVigilants):
        self.readDataInterface(pathInterface)
        self.readVigilantData(pathVigilants)

    def readDataInterface(self,pathInterface):
        self.obj_site_data_file: SiteDataFile = SiteDataFile(pathInterface, self.totalWeeks)
        self.SitesData=self.obj_site_data_file.get_data_problem()
        self.__workingDay = self.obj_site_data_file.get_working_day()
        self.totalPlaces = len(self.SitesData)

    def readVigilantData(self, pathVigilants):
        data = VigilantsDataFile(pathVigilants)
        self.VigilantsData = data.vigilantsInfo
        self.totalVigilantes = data.numberVigilants

    def initProblem(self):
        '''
        inicialize empty default problem
        :return: None
        '''
        self.identifiesWeekStartPeriod()
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
       if self.__workingDay[site-1] != 0:
          return [self.__workingDay[site-1]]
       return self.workingDay[key]


    def getSite(self, siteId):
        return self.SitesData[siteId-1]

    def generateResults(self,path,solution):
        SiteDataFile.generateResultBySite(self.cantVigilantsByPeriod,path,solution)
        VigilantsDataFile.generateResultByVigilant(path,solution)

    def get_workig_day(self):
        return self.__workingDay