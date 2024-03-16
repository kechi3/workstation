from step1 import Function
from step1 import Variable
import numpy as np

print("unchi")
class Exp(Function):
    def forward(self,x):
        return np.exp(x)

data = np.array(5)
x = Variable(data)
print(x.data)
f = Exp()
y = f(x)
print(y.data)

