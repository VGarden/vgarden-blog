import matplotlib.pyplot as plt
from math import sqrt
from random import random as uniform

def diff(a, b, N):
  points = ((uniform(), uniform()) for i in range(0, N) for j in range(0, N))
  density = sum((1 for x in points if x[0] < a and x[1] < b)) / (N*N)
  return abs(density - a*b)

def discrepancy(N, e):
  return max((diff(i/e, j/e, N) for i in range(0, e) for j in range(0, e)))

xs = [i for i in range(2, 12)]
ys = [discrepancy(N, 100) for N in xs]
zs = [(0.7/0.5)/sqrt(N*N) for N in xs]

## PLOT

fig, ax = plt.subplots()
ax.plot(xs, ys, color="b")
ax.plot(xs, zs, color="r")
ax.set(xlabel='sqrt(N)', ylabel='D*', title="Discrepancy estimate of regular-grid, dimension=2")

plt.show()

