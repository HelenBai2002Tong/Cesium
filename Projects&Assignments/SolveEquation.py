import sympy
a=sympy.Symbol("a")#p1
b=sympy.Symbol("b")#p2
c=sympy.Symbol("c")#p3
d=sympy.Symbol("d")#pm
e=sympy.Symbol("e")#r0
f1=(a/e**3)-(2*d/(2*e)**3)-(2*b/(2*e)**3)-(2*c/(4*e)**3)
f2=(b/e**3)-(2*d/(4*e)**3)-(2*a/(2*e)**3)-(2*c/(2*e)**3)
f3=(c/e**3)-(2*d/(6*e)**3)-(2*a/(4*e)**3)-(2*b/(2*e)**3)
a=sympy.solve([f1,f2,f3],[a,b,c])
print(a)