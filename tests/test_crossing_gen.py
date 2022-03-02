import pytest
from pprint import pp, pprint
from dominio.model.vigilant import Vigilant
from dominio.population import Population
from dominio.Component import Component
from dominio.soluction_nsga_ii import SoluctionNsgaII
from services.population_services import PopulationServices
from tests import generate_pyckle

population: Population = generate_pyckle.read_file("tests/population.pickle")
children_for_comparate = None

def test_parent_crossing():
    Soluction_children:SoluctionNsgaII = PopulationServices.parent_crossing(population.populations[0], population.populations[1])
    vigilants_sites = []
    for gen in Soluction_children.sites_schedule:
        Vigilants_id = [vigilant.id for vigilant in gen.assigned_Vigilantes]
        vigilants_sites.append(Vigilants_id)
        print(Vigilants_id)
    
    assert len(vigilants_sites[0]) == len(set(vigilants_sites[0]))
    assert len(vigilants_sites[1]) == len(set(vigilants_sites[1]))
       

    
