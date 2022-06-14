from ast import arg
from scipy.fftpack import shift
from dominio.model.shift import Shift
import pandas as pd

def ConvertWorkingDay(par_function):
    def function_inter(*args):
        list = []
        for i in args:
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
    var_inner = function_inner(list_a, list_b)
    var_left = function_left(list_a, list_b)
    var_right = function_ringht(list_a, list_b)
    return var_left, var_inner, var_right
    
# i = inner(Shift(0,0,4,0),Shift(0,4,10,0))
# print("inner",i)
# l = left(Shift(0,0,4,0),Shift(0,4,10,0))
# print("left", l)
# r = right(Shift(0,0,4,0),Shift(0,4,10,0))
# print("ringth", r)
# # la = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# # lb = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
# # a = inner(la,lb)
# print(a)






        
        




