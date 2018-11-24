import numpy as np
import matplotlib.pyplot as plt

#ln, = plt.plot([], [], animated=True)

t=4

def x_func(i):
    if i < 0:
        return 0
    elif i > 0 and i < 5:
        return i
    elif i > 5 and i < 10:
        return 5
    else:
        return 0

def x2(i):
    return x_func(t-i)

def k(i):
    if i < 4:
        return 0
    elif i >= 4 and i < 6:
        return 2
    elif i < 8:
        return 1
    elif i < 12:
        return 4
    else:
        return 0


def h_func(i):
    if i > 0:
        return 2*np.exp(-0.5*i)
    else:
        return 0

x = np.linspace(0, 14, num=300)
y1 = [x_func(i) for i in x]
y2 = [h_func(i) for i in x]
y3 = [x2(i) for i in x]
y4 = [k(i) for i in x]
# ax = plt.subplot(2, 1, 1)
# plt.plot(x, y1)
# plt.legend(["x(τ)"])
# plt.xlabel("τ")
# ax = plt.subplot(2, 1, 2)
# plt.plot(x, y2, 'r')
# plt.legend(["h(τ)"])
# plt.xlabel("τ")

plt.plot(x, y4)
plt.legend(["k(t)"])
plt.xlabel("t")


plt.tight_layout()
plt.show()
