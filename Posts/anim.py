import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata, ydata2 = [], [], []
#ln, = plt.plot([], [], animated=True)

lobj = ax.plot([],[],lw=2,color='r')[0]
lobj2 = ax.plot([],[],lw=2,color='b')[0]
lines = [lobj, lobj2]

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    lines[0].set_data([],[])
    lines[1].set_data([],[])
    
    return lines

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ydata2.append(-np.sin(frame))
    lines[0].set_data(xdata, ydata)
    lines[1].set_data(xdata, ydata2)

    return lines

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 255),
                    init_func=init, blit=True, interval=1)

plt.show()
