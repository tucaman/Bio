from sympy import symbols

# ======================================================================================================================
# SYMPY TUTORIAL
# https://pythonforundergradengineers.com/sympy-expressions-and-equations.html

# ----------------------------------------------------------------------------------------------------------------------
# Defining Variables in SymPy

# The output of the symbols() function are SymPy symbols objects. These output objects are separated by commas
# with no quotation marks.
x, y = symbols('x y')

# Now that the symbols x and y are instantiated, a symbolic math expression using x and y can be created.
#
# A symbolic math expression is a combination of symbolic math variables with numbers
# and mathematical operators, such as +,-,/ and *. The standard Python rules for
# working with numbers apply in SymPy symbolic math expressions.
expr = 2*x + y
# Use the .subs() method to insert a numerical value into a symbolic math expression.
# The first argument of the .subs() method is the symbols object (the variable) and
# the second argument is the numerical value. In the expression above:
# If we substitute:
#
# x=2
#
# The resulting expression is:
expr.subs(x, 2)
# The .subs() method does not replace variables in place, .subs() only completes a one-time substitution. If we call
# expr after the .subs() method is applied, the original expr expression is returned.
expr
# In order to make the substitution permanent, a new expression object needs to be assigned to the output of the
# .subs() method.
expr = 2*x + y
expr2 = expr.subs(x, 2)
expr2
# SymPy variables can also be substituted into SymPy expressions
x, y, z = symbols('x y z')
expr = 2*x + y
expr2 = expr.subs(x, z)
expr2
# More complex substitutions can also be completed. Consider the following:
# 2x+y
# Substitute in:
# y=2x^2+z^(-3)
# Results in:
expr3 = expr.subs(y, 2*x**2 + z**(-3))
expr3
# Multiple SymPy subs() methods can be chained together to substitue multiple variables in one line of code.
#
# To evaluate an expression as a floating point number (get a numerical answer out),
# use Sympy's .evalf() method.
expr.subs(x,1).subs(y,2).evalf()

# ----------------------------------------------------------------------------------------------------------------------
# Defining Equations in Sympy
#
# We can define equations in SymPy using symbolic math variables. Equations in SymPy are different than expressions in
# SymPy. An expression does not have equality. An equation has equality. An equation is equal to something.
from sympy import symbols, Eq, solve
x, y = symbols('x y')
# SymPy equations are instantiated as an object of the Eq class. After SymPy symbols are created, the symbols can be
# passed into an equation object. Let's create the equation:
# 2x+y−1=0
eq1 = Eq(2*x - y - 1, 0)
# Now let's create a second equation:
# x+y−5=0
eq2 = Eq(x + y - 5, 0)
# To solve the two equations for the two variables x and y, we'll use SymPy's
# solve() function. The solve() function takes two arguments, a tuple of the
# equations (eq1, eq2) and a tuple of the variables to solve for (x, y).
sol = solve((eq1, eq2), (x,y))
print(sol)
# The SymPy solution object is a Python dictionary. The keys are the SymPy variable objects and the values are the
# numerical values these variables correspond to.
print(f'The solution is x = {sol[x]}, y = {sol[y]}')

x, y, alpha= symbols('x y alpha')
eq1 = Eq(2*x - y - alpha, 0)
# Now let's create a second equation:
# x+y−5=0
eq2 = Eq(x + y - 5, 0)
# To solve the two equations for the two variables x and y, we'll use SymPy's
# solve() function. The solve() function takes two arguments, a tuple of the
# equations (eq1, eq2) and a tuple of the variables to solve for (x, y).
sol = solve((eq1, eq2), (x,y))
print(sol)

# ----------------------------------------------------------------------------------------------------------------------
# Chained substitutions
from sympy import symbols, Eq, solve, simplify, expand
x, y, z, a, b = symbols('x y z a b')
eq1 = Eq(x**2 + y**2, z)
expr_x = a + b
# substitute eq2 into eq1
eq2 = eq1.subs(x, expr_x)
eq2
expand(eq2)

# ======================================================================================================================
# SONNETTE  - BUBBLES

# https://boulderinvestment.tech/blog/2018/log-periodic-power-law-lppl-model-for-bubble-detection

from sympy import *
A, B, C, t_c, beta, omega, phi, t, y_t= symbols('A B C t_c beta omega phi t y_t')
# ORIGINAL - has non-linear terms...
MSE = (y_t - A - B*(t_c-t)**beta * (1 + C * cos(omega * ln(t_c-t) + phi)))**2
deriv_MSE_A = diff(MSE, A)
deriv_MSE_B = diff(MSE, B)
deriv_MSE_C = diff(MSE, C)
# solve derv_MSE_A for A
sol_A = solve(deriv_MSE_A, A)
# replace A in deriv_MSE_B
deriv_MSE_B = deriv_MSE_B.subs(A, sol_A[0])
sol_B = solve(deriv_MSE_B, B)

linsolve([deriv_MSE_A, deriv_MSE_B, deriv_MSE_C], [A, B, C])

# SIMAG
# https://boulderinvestment.tech/blog/2018/log-periodic-power-law-lppl-model-for-bubble-detection
A, B, C_1, C_2, t_c, beta, omega, t, y_t, y_t_1, y_t_2, t_1, t_2 = symbols('A B C_1 C2 t_c beta omega t y_t y_t_1 y_t_2 t_1 t_2')
# MSE = (y_t - A - B*(t_c-t)**beta + (t_c-t)**beta * (C_1 * cos(omega * ln(t_c-t)) + C_2 * sin(omega * ln(t_c-t))))**2
MSE = (y_t_1 - A - B * t_1 + C_1 * t_1 * cos(t_1) + t_1*C_2 * sin(t_1))**2 \
      + (y_t_2 - A - B * t_2 + C_1* t_2 * cos(t_2) + C_2* t_2 * sin(t_2))**2
deriv_MSE_A = diff(MSE, A)
deriv_MSE_B = diff(MSE, B)
deriv_MSE_C_1 = diff(MSE, C_1)
deriv_MSE_C_2 = diff(MSE, C_2)

linsolve([deriv_MSE_A, deriv_MSE_B, deriv_MSE_C_1, deriv_MSE_C_2], [A, B, C_1, C_2])

# Necessary condition for a local minimum is that first derivatives vanish. Hence, we will equate above partial
# derivatives to zero, and then solve the system for A, B and C
eqA = Eq(deriv_MSE_A, 0)
eqB = Eq(deriv_MSE_B, 0)
eqC_1 = Eq(deriv_MSE_C_1, 0)
eqC_2 = Eq(deriv_MSE_C_2, 0)
sol = linsolve((eqA, eqB, eqC_1, eqC_2), (A, B, C_1, C_2))

linsolve([deriv_MSE_A, deriv_MSE_B, deriv_MSE_C_1, deriv_MSE_C_2], (A, B, C_1, C_2))







# ======================================================================================================================
# https://github.com/Boulder-Investment-Technologies/lppls
from lppls import lppls, data_loader
import numpy as np
import pandas as pd
# %matplotlib inline

# read example dataset into df
data = data_loader.sp500()

# convert index col to evenly spaced numbers over a specified interval
time = np.linspace(0, len(data)-1, len(data))

# create list of observation data, in this case,
# daily adjusted close prices of the S&P 500
price = [p for p in data['Adj Close']]

# create Mx2 matrix (expected format for LPPLS observations)
observations = np.array([time, price])

# set the max number for searches to perform before giving-up
# the literature suggests 25
MAX_SEARCHES =50

# instantiate a new LPPLS model with the S&P 500 dataset
lppls_model = lppls.LPPLS(use_ln=True, observations=observations)

# fit the model to the data and get back the params
tc, m, w, a, b, c = lppls_model.fit(observations, MAX_SEARCHES, minimizer='Nelder-Mead')

# visualize the fit
lppls_model.plot_fit(observations, tc, m, w)

# should give a plot like the following...

