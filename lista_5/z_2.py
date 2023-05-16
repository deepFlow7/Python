from itertools import combinations
from collections import OrderedDict
from tokenize import String
from xmlrpc.client import Boolean

class Formula:
    def calculate(self, variables):
        ...
    def __str__(self):
        ...
    def __add__(e_1, e_2):
        return Or(e_1, e_2)
    def __mul__(e_1, e_2):
        return And(e_1, e_2)
    def simplify(self):
        return self
    def variables(self):
        return list()
    def Tautology(self):
        vars = self.variables()
        comb = list(OrderedDict.fromkeys(combinations([True, False], len(vars))))
        for l in list(comb):
            dict = {}
            for i in range(0, len(l)):
                dict[vars[i]] = l[i]
            if self.calculate(dict) == False:
                return False
        return True

class Two_args_formula(Formula):
    def __init__(self, f_1, f_2):
        if not(isinstance(f_1, Formula) and isinstance(f_2, Formula)):
            raise TypeError("Arguments must be instances of Formula")
        self.f_1 = f_1
        self.f_2 = f_2
    def calculate(self, variables, function):
        return function(self.f_1.calculate(variables), self.f_2.calculate(variables))
    def __str__(self, op):
        s = self.f_1.__str__()
        if isinstance(self.f_1, Two_args_formula):
            s = '(' + s + ') '
        s += ' ' + op + ' '
        if isinstance(self.f_2, Two_args_formula):
            s += '(' + self.f_2.__str__() + ') '
        else:
            s += self.f_2.__str__()
        return s
    def variables(self):
        return self.f_1.variables() + self.f_2.variables()

class Or(Two_args_formula):
    def __init__(self, f_1, f_2):
       super().__init__(f_1, f_2)
    def calculate(self, variables):
        f = lambda x, y : x or y
        return super().calculate(variables, f)
    def __str__(self):
       return super().__str__('v')
    def simplify(self):
        if isinstance(self.f_1, Constant) and self.f_1.calculate({}) == False:
            return self.f_2
        if isinstance(self.f_2, Constant) and self.f_2.calculate({}) == False:
            return self.f_1
        return Or(self.f_1.simplify(), self.f_2.simplify())

class And(Two_args_formula):
    def __init__(self, f_1, f_2):
       super().__init__(f_1, f_2)
    def calculate(self, variables):
        return super().calculate(variables, lambda x, y : x and y)
    def __str__(self):
        return super().__str__('∧')
    def simplify(self):
        if isinstance(self.f_1, Constant) and self.f_1.calculate({}) == False:
            return Constant(False)
        if isinstance(self.f_2, Constant) and self.f_2.calculate({}) == False:
            return Constant(False)
        return And(self.f_1.simplify(), self.f_2.simplify())

class Not(Formula):
    def __init__(self, f):
        if not(isinstance(f, Formula)):
            raise TypeError("Argument must be an instance of Formula")
        self.f = f
    def calculate(self, variables):
        return not self.f.calculate(variables)
    def __str__(self):
        s = self.f.__str__()
        if isinstance(self.f, Two_args_formula):
            s = "(" + s + ")"
        s = "¬" + s
        return s
    def variables(self):
        return self.f.variables()

class Constant(Formula):
    def __init__(self, c):
        if not(isinstance(c, Boolean)):
            raise TypeError("Constant must be Boolean")
        self.c = c
    def calculate(self, variables):
        return self.c
    def __str__(self):
        return self.c.__str__()

class Variable(Formula):
    def __init__(self, v):
        if not(isinstance(v, str)):
           raise TypeError("Variable must be a string")
        self.v = v
    def calculate(self, variables):
        if self.v in variables:
            return variables[self.v]
        raise Variable_without_value()
    def __str__(self):
        return self.v.__str__()
    def variables(self):
        return [self.v]

class Variable_without_value(Exception):
    pass

a = And(Variable('x'), Or (Constant(False), Constant(False)))
print (a, " = ", a.calculate({'x' : True}), " [for 'x' -> True]")

b = Constant(True) + Constant(False)
print (b, " = ", b.calculate({}))

c = Or(Variable('x'), Not(Variable('x'))) 
print("Is ", c, " a tautology? ", c.Tautology())