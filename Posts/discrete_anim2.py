import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure(num = 0, figsize = (10, 6))
ax1 = plt.subplot2grid((2, 2), (0, 0))
ax2 = plt.subplot2grid((2, 2), (0, 1))
ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)

# Set titles of subplots
ax1.set_title('Convolving h with x')
ax2.set_title('Convolving h with k')
ax3.set_title('Final output, sum of above two figures')
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

#fig, (ax1, ax2, ax3) = plt.subplots(3,1)
tau_data = []
xdata = []
hdata = []
ydata = []
y2data = []
yfinaldata = []
#ln, = plt.plot([], [], animated=True)

t_range = np.linspace(-2, 16, num=20)

ax1_lobj = ax1.plot([],[],lw=1, drawstyle='steps-pre')[0]
ax1_lobj2 = ax1.plot([],[],lw=1,color='r', drawstyle='steps-pre')[0]
ax1_lobj3 = ax1.plot([],[], '--', lw=1, color='g', drawstyle='steps-pre')[0]
lines1 = [ax1_lobj, ax1_lobj2, ax1_lobj3]

ax2_lobj = ax2.plot([],[],lw=1, color='y', drawstyle='steps-pre')[0]
ax2_lobj2 = ax2.plot([],[],lw=1, color='r', drawstyle='steps-pre')[0]
ax2_lobj3 = ax2.plot([],[], '--', lw=1, color='g', drawstyle='steps-pre')[0]
lines2 = [ax2_lobj, ax2_lobj2, ax2_lobj3]

ax3_lobj, = ax3.plot([],[],lw=2, color='g', drawstyle='steps-pre')

ax1.legend(["x(t-τ)", 'h(τ)', 'y1(t)'])
ax1.set_xlabel('t')
ax2.legend(["k(t-τ)", 'h(τ)', 'y2(t)'])
ax2.set_xlabel('t')
ax3.legend(["y = y1(t) + y2(t)",])
ax3.set_xlabel("t")

ax1.set_xlim(-2, 16)
ax1.set_ylim(-0.1, 18)
ax2.set_xlim(-2, 16)
ax2.set_ylim(-0.1, 12)
ax3.set_ylim(-1, 27)
ax3.set_xlim(-1, 16)

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

def k_func2(i):
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

def k_func(i, t):
    return k_func2(t-i)

def h_func(i):
    if i > 0:
        return 2*np.exp(-0.5*i)
    else:
        return 0

def update(frame):
    global tau_data
    global xdata
    global hdata
    global ydata
    global y2data
    global yfinaldata

    tau_data.append(frame)
    xdata = [x2(i, frame) for i in t_range]
    hdata = [h_func(i) for i in t_range]
    ydata.append(np.sum(np.multiply(xdata, hdata)*(t_range[1] - t_range[0])))
    lines1[0].set_data(t_range, xdata)
    lines1[1].set_data(t_range, hdata)
    lines1[2].set_data(tau_data, ydata)

    kdata = [k_func(i, frame) for i in t_range]
    y2data.append(np.sum(np.multiply(kdata, hdata)*(t_range[1] - t_range[0])))
    lines2[0].set_data(t_range, kdata)
    lines2[1].set_data(t_range, hdata)
    lines2[2].set_data(tau_data, y2data)

    #print(yfinaldata, tau_data)
    #print("Scilene = ", yfinaldata)
    yfinaldata.append(y2data[-1] + ydata[-1])
    ax3_lobj.set_data(tau_data, yfinaldata)

    return lines1 + lines2 + [ax3_lobj]

plt.tight_layout()

ani = FuncAnimation(fig, update, frames=t_range,
            blit=False, interval=250)

lol = ani.to_html5_video()
with open('k.html', 'w') as f:
   f.write(lol)


plt.show()
