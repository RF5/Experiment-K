import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
tau_data = []
xdata = []
hdata = []
ydata = []
#ln, = plt.plot([], [], animated=True)

t_range = np.linspace(-2, 15, num=20)

lobj = ax.plot([],[],lw=2)[0]
lobj2 = ax.plot([],[],lw=2,color='r')[0]
lobj3 = ax.plot([],[], lw=2, color='g')[0]
lines = [lobj, lobj2, lobj3]

def x_func(i):
    if i <= 0:
        return 0
    elif i > 0 and i <= 5:
        return i
    elif i > 5 and i <= 10:
        return 5
    else:
        return 0

def x2(i, t):
    return x_func(t-i)

def h_func(i):
    if i > 0:
        return 2*np.exp(-0.5*i)
    else:
        return 0

ax.legend(["x(t-τ)", 'h(τ)', 'y(t)'])

def init():
    ax.set_xlim(-2, 16)
    ax.set_ylim(-0.1, 20)
    lines[0].set_data([],[])
    lines[1].set_data([],[])
    lines[2].set_data([],[])
    #xtxt = ax.text(0.9, 0.95, 'w', transform=ax.transAxes)
    #htxt = ax.text(0.9, 0.90, 'e', transform=ax.transAxes)
    #ytxt = ax.text(0.9, 0.85, 'f', transform=ax.transAxes)
    return lines

def update(frame):

    tau_data.append(frame)
    xdata = [x2(i, frame) for i in t_range]
    hdata = [h_func(i) for i in t_range]
    ydata.append(np.sum(np.multiply(xdata, hdata)*(t_range[1] - t_range[0])))
    lines[0].set_data(t_range, xdata)
    lines[1].set_data(t_range, hdata)

    lines[2].set_data(tau_data, ydata)

    return lines

ani = FuncAnimation(fig, update, frames=t_range,
                init_func=init, blit=True, interval=100)

# lol = ani.to_html5_video()
# with open('k.html', 'w') as f:
#    f.write(lol)


plt.show()
