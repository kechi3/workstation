import numpy as np
import plotly.graph_objects as go
import numpy as np

def step_function(x):
    return np.array(x>0, dtype=int)

def sigmoid(x):
    return 1/(1+np.exp(-x))

x = np.arange(-5.0,5.0,0.1)
y = sigmoid(x)


fig = go.Figure(data=[
    go.Scatter(x=x, y=y, name="sin"),
])

fig.show()
print(x)
print(y)

