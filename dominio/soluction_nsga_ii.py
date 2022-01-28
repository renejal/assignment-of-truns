from typing import List, Dict
from xmlrpc.client import Boolean
from dominio.Solution import Solution

class SoluctionNsgaII(Solution):
    __dominate: List[Solution] 
    __dominate_me_account: int 
    __range: int

    def is_dominate(self, soluction):
        if soluction in self.__dominate:
            print("me dominan") 
        else:
            print("no me dominan")
            
    def is_dominate(self, soluction) -> Boolean:
        response = False
        if soluction in self.__dominate:
            response = True
        return response
    
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
    def range(self):
        return self.__range

    # set
    @dominate.setter
    def dominate(self, soluctions):
       self.__dominate = soluctions
    
    @dominate.setter
    def dominate_me(self, dominate_me_account):
        return self.__dominate_me_account


    
