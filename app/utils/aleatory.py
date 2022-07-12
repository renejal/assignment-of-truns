import random
from typing import List

def get_aleatory(parInit, parEnd, parNumber):
    '''
    generate n number aleatory between number init and number end
    :param init: number init
    :param end: number end
    :param number: quantity the number aleatory
    :return: list number aleatory
    '''
    k = 0
    listAleatory = []
    while True:
        if parNumber > k:
            numAleatory = random.randint(parInit, parEnd)
            if numAleatory not in listAleatory:
                listAleatory.append(numAleatory)
                k = k + 1
        else:
            break
    return listAleatory

def get_object_ramdon_for_list(init: int, end: int, list: List) -> int:
    """get numero aleatory of list
    Args:
        init (int): value start
        end (int): value end 
        list (List): list of values

    Returns:
        int: return object 
    """
    numAletory = random.randint(init, end)
    if list[numAletory]:
        return list[numAletory]
    else:
        raise(f"error: no se encontro el objeto con el indice {numAletory}")

def  get_random_int(par_init: int, par_end: int, list: List):
    """obtain number aleatory between par_init and par_end
    Args:
        par_init (_type_): number start
        par_end (_type_): number end 
        list (_type_): list number not validate 
    """
    aleatory = None
    while True:
        aleatory = random.randint(par_init,par_end)
        if aleatory in list:
            continue
        else:
            break
    return aleatory


    