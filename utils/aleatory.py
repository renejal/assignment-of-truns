import random

def getAleatory(parInit, parEnd, parNumber):
    '''
    generate n number aleatory between  nunber init and number end
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
