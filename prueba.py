import operator
diciona = {}
diciona[1]=10
diciona[2]=30
diciona[3]=5
cliente_short = sorted(diciona.items(),key = operator.itemgetter(1),reverse=True)

print(cliente_short[0][1])