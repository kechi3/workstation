import numpy as np
import unittest

class SquareTest(unittest.TestCase):
    def test_forward(self):
        x = Variable(np.array(2.0))
        y = square(x)
        expected = np.array(4.0)
        self.assertEqual(y.data, expected)
    def test_backward(self):
        x = Variable(np.array(3.0))
        y = square(x)
        y.backward()
        expected = np.array(6.0)
        self.assertEqual(x.grad, expected)
    def test_gradient_check(self):
        x = Variable(np.random.rand(1))
        y = square(x)
        y.backward()
        num_grad = numerical_diff(square, x)
        flg = np.allclose(x.grad, num_grad)
        self.assertTrue(flg)

class Variable:
    def __init__(self,data):
        if data is not None:
            if not isinstance(data, np.ndarray):
                raise TypeError('{} is not supported'.format(type(data)))

        self.data = data
        self.grad = None
        self.creator = None
        self.generation = 0

    def cleargrad(seld):
        self.grad = None

    def set_creator(self,func):
        self.creator = func
        self.generation = func.generation + 1

    def backward(self):
        if self.grad is  None:
            self.grad = np.ones_like(self.data)
        funcs = [self.creator]
        while funcs:
            f = funcs.pop()
            gys = [output.grad for output in f.outputs]
            gxs = f.backward(*gys)
            if not isinstance(gxs, tuple):
                gxs = (gxs,)
            for x, gx in zip(f.inputs, gxs): 
                if x.grad is None:
                    x.grad = gx
                else:
                    x.grad = x.grad + gx
                if x.creator is not None:
                    funcs.append(x.creator)

class Function:
    def __call__(self,*inputs):
        xs = [x.data for x in inputs]
        ys = self.forward(*xs)
        if not isinstance(ys,tuple):
            ys = (ys,)
        outputs = [Variable(as_array(y)) for y in ys]
        self.generation = max([x.generation for x in inputs])
        for output in outputs:
            output.set_creator(self)
        self.inputs = inputs
        self.outputs = outputs
        return outputs if len(outputs)>1 else outputs[0]

    def forward(self, x):
        raise NotImplementedError()

    def backward(self, gy):
        raise NotImplementedError()

class Add(Function):
    def forward(self, x0, x1):
        y = x0 + x1
        return y
    def backward(self, gy):
        return gy,gy

class Square(Function):
    def forward(self, x):
        y = x**2
        return y
    def backward(self, gy):
        x = self.inputs[0].data
        gx = 2*x*gy
        return gx

class Exp(Function):
    def forward(self,x):
        return np.exp(x)
    def backward(self,gy):
        x = self.inputs[0].data
        return np.exp(x)*gy

def as_array(x):
    if np.isscalar(x):
        return np.array(x)
    return x

def numerical_diff(f, x, esp=1e-4):
    x0=f(Variable(x.data-esp))
    x1=f(Variable(x.data+esp))
    return (x1.data-x0.data)/(2*esp)

def f(x):
    A = Square()
    B = Exp()
    C = Square()
    return C(B(A(x)))

def square(x):
    f = Square()
    return f(x)

def add(x0, x1):
    return Add()(x0, x1)

def exp(x):
    return Exp()(x)

x = Variable(np.array(0.5))

a = square(x)
b = exp(a)
y = square(b)

y.backward()
print(x.grad)

x = Variable(np.array(3.0))
y = add(add(x,x),x)
y.backward()
print(y.data)
print(x.grad)

