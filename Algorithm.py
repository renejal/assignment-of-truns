from abc import ABC, abstractmethod


class Algorithm(ABC):
    MaxEFOs = int
    CurrentEFOs = 0
    MyBestSolution = None
    VigilantAssigment = None


    @abstractmethod
    def Execute(self, problem, theAleatory):
        pass


