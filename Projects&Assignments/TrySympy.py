import sympy as sy
T = sy.symbols('T')
R = sy.symbols('R')
V = sy.symbols('V')
L = sy.symbols('L')
h = sy.symbols('h')
A=(2*L-V*R)/(2*V)#T
B=(3*L-3*T*V)/(2*V)#R
C=(6*L*T+3*L*R)/(6*T**2+6*R*T+2*R**2)#V
a = sy.solve([(2*L-V*R)/(2*V)-T,(3*L-3*T*V)/(2*V)-R,((6*L*T+3*L*R)/(6*T**2+6*R*T+2*R**2))-V],[T,R,V])
print(a)