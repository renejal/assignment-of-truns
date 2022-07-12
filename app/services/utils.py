from app.dominio.Component import Component
from conf import settings
from app.dominio.Solution import Solution

def get_random_gens(parent_for_exchange_new: Solution, parent_for_exchange: Solution) -> List[Component]:
    "El metodo debe retornas la lista de vigilantes del componente y el componente del cual fue sacado"
    gen_parent_for_exchange_new: Component = None
    gen_parent_exchange: Component = None
    iteration = 0
    while iteration <= settings.NUMBER_ITERATION_SELECTION_COMPONENTE:
        gen_parent_for_exchange_new = parent_for_exchange_new.get_random_gen([])
        gen_parent_exchange = parent_for_exchange.get_random_gen([gen_parent_for_exchange_new.site_id])
        result = PopulationServices.is_validation_and_repartion(gen_parent_for_exchange_new, gen_parent_exchange)
        if not result:
            return False
        if (result[0] and result[1]) != [] and (result[0] and result[1]) is not None:
            return result[0], result[1]
        iteration += 1
    return False
    raise("Error no se encontro vigilantes disponibles")