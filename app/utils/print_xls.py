
import os
from dominio.Solution import Solution 
from utils.print_sites_xls import generate_excel_site
from utils.print_vigilants_xls import generate_excel_vigilantes
from conf.settings import PATH_RESULTS

def generate_results(dataGrasp: dict[str,object],dataNsga: dict[str,object], idUser:str ):
    os.mkdir(PATH_RESULTS+idUser)
    if(dataGrasp != None):
        generate_excel_site(solution)
    if(dataNsga != None):
        generate_excel_vigilantes(solution)    


