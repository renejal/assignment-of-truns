
from dominio.Solution import Solution
from utils.print_sites_xls import generate_excel_site
from utils.print_vigilants_xls import generate_excel_vigilantes

def generate_results(solution: Solution):
    generate_excel_site(solution)
    generate_excel_vigilantes(solution)    
