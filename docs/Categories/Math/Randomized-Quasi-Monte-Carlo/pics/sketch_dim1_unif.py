import matplotlib.pyplot as plt
from math import sqrt
from random import random as uniform

def diff(a, N):
  points = (uniform() for i in range(0, N))
  density = sum((1 for x in points if x < a)) / N
  return abs(density - a)

def discrepancy(N, e):
  return max((diff(i/e, N) for i in range(0, e)))

xs = [i for i in range(10, 100)]
ys = [discrepancy(N, 10000) for N in xs]
zs = [1/sqrt(N) for N in xs]

## PLOT

fig, ax = plt.subplots()
ax.plot(xs, ys, color='b')
ax.plot(xs, zs, color='r')
ax.set(xlabel='N', ylabel='D*', title="Discrepancy estimate of regular-grid, dimension=1")

plt.show()

