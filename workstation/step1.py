import numpy as np
import weakref
import unittest
import contextlib

@contextlib.contextmanager
def using_config(name, value):
    old_value = getattr(Config, name)
    setattr(Config,name,value)
    try:
        yield
    finally:
        setattr(Config, name, old_value)

def as_variable(obj):
    if isinstance(obj, Variable):
        return obj
    return Variable(obj)

def no_grad():
    return using_config('enable_backprop',False)

class Config:
    enable_backprop = True

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
    __array_priority__= 200
    def __init__(self,data, name = None):
        if data is not None:
            if not isinstance(data, np.ndarray):
                raise TypeError('{} is not supported'.format(type(data)))

        self.data = data
        self.name = name
        self.grad = None
        self.creator = None
        self.generation = 0

    def __len__(self):
        return len(self.data)

    def __mul__(self, other):
        return mul(self,other)

    def __repr__(self):
        if self.data is None:
            return 'valuable(None)'
        p = str(self.data).replace('\n','\n'+' '*9)
        return 'valuable('+p+')'

    @property
    def shape(self):
        return self.data.shape

    @property
    def ndim(self):
        return self.data.ndim

    @property
    def size(self):
        return self.data.size

    @property
    def dtype(self):
        return self.data.dtype

    def cleargrad(seld):
        self.grad = None

    def set_creator(self,func):
        self.creator = func
        self.generation = func.generation + 1

    def backward(self, retain_grad=False):
        if self.grad is  None:
            self.grad = np.ones_like(self.data)
        funcs = []
        seen_set = set()
        def add_func(f):
            if f not in seen_set:
                funcs.append(f)
                seen_set.add(f)
                funcs.sort(key=lambda x:x.generation)
        add_func(self.creator)

        while funcs:
            f = funcs.pop()
            gys = [output().grad for output in f.outputs]
            gxs = f.backward(*gys)
            if not isinstance(gxs, tuple):
                gxs = (gxs,)
            for x, gx in zip(f.inputs, gxs): 
                if x.grad is None:
                    x.grad = gx
                else:
                    x.grad = x.grad + gx
                if x.creator is not None:
                    add_func(x.creator)
            if not retain_grad:
                for y in f.outputs:
                    y().grad = None

class Function:
    def __call__(self,*inputs):
        inputs = [as_variable(x) for x in inputs]
        xs = [x.data for x in inputs]
        ys = self.forward(*xs)
        if not isinstance(ys,tuple):
            ys = (ys,)
        outputs = [Variable(as_array(y)) for y in ys]
        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs])
            for output in outputs:
                output.set_creator(self)
        self.inputs = inputs
        self.outputs = [weakref.ref(output) for output in outputs]
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

class Neq(Function):
    def forward(self,x):
        return -x
    def backward(self,gy):
        return -gy

class Mul(Function):
    def forward(self,x0,x1):
        y = x0*x1
        return y
    def backward(self,gy):
        x0,x1 = self.inputs[0].data,self.inputs[1].data
        return gy*x1,gy*x0

class Sub(Function):
    def forward(self,x0,x1):
        y = x0- x1
        return y
    def backward(self,gy):
        return gy,-gy

class Div(Function):
    def forward(self,x0,x1):
        y = x0 / x1
        return y
    def backward(self,gy):
        x0,x1 = self.inputs[0].data,self.inputs[0].data
        gx0 = gy /x1
        gx1 = gy*(-x0 /x1**2)
        return gy0,gy1

class Pow(Function):
    def __init__(self,c):
        self.c = c

    def forward(self,x):
        y = x**self.c
        return y
    def backward(self,gy):
        x = self.inputs[0].data
        c = self.c
        gx = c*x**(c-1)*gy
        return gx

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
    x1 = as_array(x1)
    return Add()(x0, x1)

def exp(x):
    return Exp()(x)

def neq(x):
    return Neq()(x)

def mul(x0,x1):
    x1 = as_array(x1)
    return Mul()(x0,x1)

def sub(x0,x1):
    x1 = as_array(x1)
    return Sub()(x0,x1)

def rsub(x0,x1):
    x1 = as_array(x1)
    return Sub()(x1,x0)

def div(x0,x1):
    x1 = as_array(x1)
    return Div()(x0,x1)

def rdiv(x0,x1):
    x1 = as_array(x1)
    return Div()(x1,x0)

def pow(x,c):
    return Pow(c)(x)

Variable.__add__ = add
Variable.__radd__ = add
Variable.__mul__ = mul
Variable.__rmul__ = mul
Variable.__neq__ = neq
Variable.__sub__ = sub
Variable.__rsub__ = rsub
Variable.__truediv__ = div
Variable.__rtruediv__ = rdiv
Variable.__pow__ = pow

x = Variable(np.array(0.5))

a = square(x)
b = exp(a)
y = square(b)

y.backward()
print(x.grad)

x = Variable(np.array(2.0))
y = x**3
print(y)

