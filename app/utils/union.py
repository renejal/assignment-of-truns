from ast import arg
from numpy import inner
from dominio.model.shift import Shift
import pandas as pd

def ConvertWorkingDay(par_function):
    def function_inter(*args):
        list = []
        for i in args:
            if not isinstance(i,Shift):
                list.append(i)
            else:
                list.append(convert_continue(i))
        return par_function(list[0], list[1])
    return function_inter

def convert_continue(working_day: Shift):
    working_day_list = []
    for i in range(working_day.shift_start, working_day.shift_end + 1):
        working_day_list.append(i)
    return working_day_list

def innerv2(list_a, list_b):
    d1 = {"key":list_a}
    d2 = {"key": list_b}
    df1 = pd.DataFrame(data=d1)
    df2 = pd.DataFrame(data=d2)
    df = pd.merge(df1,df2,on="key")
    inner = list(df["key"])
    return inner

@ConvertWorkingDay
def function_left(list_a, list_b):
    "lista - inner "
    inner=innerv2(list_a, list_b)
    left = list(set(list_a)- set(inner))
    return left

@ConvertWorkingDay
def function_ringht(list_a, list_b):
    inner = innerv2(list_a, list_b)
    right = list(set(list_b) - set(inner))
    return right

@ConvertWorkingDay
def function_inner(list_a, list_b):
    d1 = {"key":list_a}
    d2 = {"key": list_b}
    df1 = pd.DataFrame(data=d1)
    df2 = pd.DataFrame(data=d2)
    df = pd.merge(df1,df2,on="key")
    inner = list(df["key"])
    return inner

def calculate(list_a, list_b):
    var_left = function_left(list_a, list_b)
    var_inner = function_inner(list_a, list_b)
    var_right = function_ringht(list_a, list_b)
    var_right.sort()
    var_inner.sort()
    var_left.sort()
    return var_left,var_inner,var_right

def print_working_day(shift):
    if isinstance(shift,Shift):
        return convert_continue(shift)
    else:
        return shift
    


# test whit list
# la = [1,2,3,4,5,6]
# lb = [1,2,3,4,5,6,7,8,9]
# a = calculate(la,lb)

# test whit shift
# la = Shift(None,1,6,0)
# lb = Shift(None,1,9,0)
# a = calculate(la,lb)
# print(a)






        
        




