from curses.ascii import SO
from typing import List, Dict
from xmlrpc.client import Boolean
from dominio.Solution import Solution

class SoluctionNsgaII(Solution):

    __dominate: List[int] 
    __dominate_me_account: int 
    __range_soluction: int

    # def is_dominate(self, soluction: SoluctionNsgaII):
    #     # se obitene el finter y se compara si domina o no la solucioon
    #     if super().calculate_fitness < soluction.
    #     pass

    def add_dominate(self, soluction):
        if soluction is not self.__dominate:
            self.__dominate.append(soluction)

    # get 
    
    @property
    def dominate(self, position):
        return self.__dominate
    
    @property
    def dominate_me(self):
        return self.__dominate_me

    @property
    def range_soluction(self):
        return self.__range_soluction

    # set
    @dominate.setter
    def dominate(self, soluction_id):
       if soluction_id not in self.__dominate:
           self.__dominate.append(soluction_id)
    
    @dominate.setter
    def dominate_me(self, dominate_me_account):
        return self.__dominate_me_account


    
