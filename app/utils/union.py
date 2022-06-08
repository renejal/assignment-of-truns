from numpy import inner
import pandas as pd

class Union:
    
    @classmethod
    def inner(self, list_a, list_b):
        d1 = {"key":list_a}
        d2 = {"key": list_b}
        df1 = pd.DataFrame(data=d1)
        df2 = pd.DataFrame(data=d2)
        df = pd.merge(df1,df2,on="key")
        inner = list(df["key"])
        return inner
    
    @classmethod
    def left(self, list_a, list_b):
        "lista - inner "
        inner=self.inner(list_a, list_b)
        left = list(set(list_a)- set(inner))
        return left

    @classmethod
    def right(self, list_a, list_b):
        inner = self.inner(list_a, list_b)
        right = list(set(list_b) - set(inner))
        return right

        
        
a = [1,2,3,4,5]
b = [4,5,6,7,8]

print("inner", Union.inner(a,b))
print("left", Union.left(a,b))
print("right", Union.right(a,b))



