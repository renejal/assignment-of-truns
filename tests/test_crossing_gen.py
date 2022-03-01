from curses import noecho
import pytest
from pprint import pp, pprint
from dominio.model.vigilant import Vigilant
from dominio.population import Population
from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.vigilant_assigment import VigilantAssigment
from services.population_services import PopulationServices
from dominio.Component import Component
from dominio.model.shift import Shift
from dominio.model.site import Site
from tests import generate_pyckle

population: Population = generate_pyckle.read_file("tests/population.pickle")
children_for_comparate = None


# def test_crosing_vigilant():
#     soluction = population.populations[0]
#     vigilant_new_id: int = 1
#     vigilant_for_exchange_id: int = 5
#     # pprint(vars(soluction))
#     gen=soluction.get_gen(1)
#     print(gen.assigned_Vigilantes)
#     gen= gen.assigned_Vigilantes
#     pprint(vars(gen))
#     vigilant_new_id_temp = id(soluction.get_gen(vigilant_new_id))
#     vigilant_for_exchange_id_temp = id(soluction.get_gen(vigilant_for_exchange_id))
#     soluction.crossing_vigilant(vigilant_new_id, vigilant_for_exchange_id)



@pytest.mark.parametrize("parent_for_exchange_new","children", 
[
    #todo pruebas
        
])
def test_parent_crossing(parent_for_exchange_new: SoluctionNsgaII, children: int):
    print(parent_for_exchange_new)

    # children = PopulationServices.crossing_vigilant(parent_for_exchange_new, children)
    # pprint(children)
    
    

# def test_reparate_soluction():
#     pass

# @pytest.mark.parametrize("parent_for_exchange_new, children",
# [
#     (population.populations[0]),
#     (population.populations[1])
# ])
# def test_parent_crossing(parent_for_exchange_new: SoluctionNsgaII, 
#                          children: SoluctionNsgaII):
#     Soluction_children = PopulationServices.parent_crossing(parent_for_exchange_new, children)
#     assert Soluction_children == children_for_comparate
    