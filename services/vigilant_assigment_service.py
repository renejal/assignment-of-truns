from dominio.model.site import Site
from conf import settings
from utils import aleatory
from typing import List, Dict
from dominio.model.vigilant import Vigilant


class Vigilant_assigment_service:

    def get_possible_vigilant_to_assign(site: Site, vigilantes: List[Vigilant]) -> int:
        """
        obtain random vigilant for parametr the settings
        vigilantes: list de vigilantes total
        Site: sitio a vigilar
        shift: los turnos del sitio a vigilar

        return the possible vigilantes avalaible for site
        """

        dict_vigilants_distance: Dict = Vigilant_assigment_service.__order_vigilants_in_place_by_distance(vigilantes, site)
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
