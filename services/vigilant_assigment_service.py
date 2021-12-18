import random
from typing import List
from dominio.model.site import Site
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift
from conf import settings
from utils import aleatory
from typing import List, Dict


from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant


class Vigilant_assigment_service:

    def is_vigilant_avaible(vigilant: Vigilant, shift:Shift) -> bool:
        return false
        

    @staticmethod
<<<<<<< HEAD:services/vigilant_assigment_service.py
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
=======
    def get_possible_vigilant_to_assign(site: Site, vigilantes: List[Vigilant]) -> int:
        """
        obtain random vigilant for parametr the settings
        vigilantes: list de vigilantes total
        Site: sitio a vigilar
        shift: los turnos del sitio a vigilar

        return the possible vigilantes avalaible for site
        """

        dict_vigilants_distance: Dict = ObtainVigilantesService.__order_vigilants_in_place_by_distance(vigilantes, site)
        vigilants_id: int = aleatory.get_ramdon_for_list(0, settings.WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE,
                                                         dict_vigilants_distance)
        return vigilants_id



    def __order_vigilants_in_place_by_distance(vigilantes: List[Vigilant], site_id: int) -> Dict:
        """
        :param vigilantes:
        :param site:
        :return: List the Dict {vigilans_id : vigilants.distancia }
        """
        dict_order_the_vigilants_for_distance: Dict = {}
        vigilant: Vigilant
        for vigilant in range(0, len(vigilantes)):
            dict_order_the_vigilants_for_distance[vigilant.id] = vigilant.distance[site_id]

        return dict_order_the_vigilants_for_distance

    def __obtain_vigilants_in_default_for_site(vigilants: List[Vigilant], site_id: int) -> List:
        """
        obtain vigilants for default for the site whit id = n

        :param vigilants: list the vigilants
        :param site_id: identy vigilants
        :return: vigilants for default
        """
        vigilant_for_default: List = []
        for vigilant in vigilants:
            if vigilant.default_place_to_look_out == site_id:
                vigilant_for_default[vigilant.id] = vigilant.distance[site_id]
        settings.random.shuffle(vigilant_for_default)
        return vigilant_for_default


>>>>>>> rafactor/possible_vigilant_to_assigment:services/obtainvigilantesservice.py
