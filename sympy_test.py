import sympy

# Define the two lines
l1 = sympy.Line((0, 0), (1, 1))
l2 = sympy.Line((0, 1), (1, 0))

# Find the intersection point
intersection = l1.intersection(l2)

# Print the intersection point
print(intersection)

# Define symbols
x = sympy.Symbol('x')
y = sympy.Symbol('y')


# Basic operations
print(x + y)  # Outputs: x + y
print(x * y)  # Outputs: x*y
print(x**2)  # Outputs: x**2

# Calculus
print(sympy.diff(x**2, x))  # Outputs: 2*x
print(sympy.integrate(x**2, x))  # Outputs: x**3/3 + C

# Matrices
A = sympy.Matrix([[1, 2], [3, 4]])
print(A)  # Outputs: Matrix([[1, 2], [3, 4]])
print(A.det())  # Outputs: -2

# Solving equations
print(sympy.solve(x**2 - 1, x))  # Outputs: [-1, 1]
