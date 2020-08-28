# %%
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.colors import LightSource
from matplotlib import cm
from itertools import combinations, product
import matplotlib as mpl
from numpy.random import uniform

mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = "Computer Modern Roman"
mpl.rcParams['font.size'] = 12








offs = 0.04
Rs = [1,0.5]

for i,R in enumerate(Rs):
    fig = plt.figure(i+1,figsize=(2.5,2.))
    ax = fig.add_subplot(111, projection='3d')

    size=1000 if R==1 else 250
    X = uniform(R*offs,R* (1-offs),size)
    Y = uniform(R*offs,R* (1-offs),size)
    Z = uniform(R*offs,R* (1-offs),size)



    # Create cubic bounding box to simulate equal aspect ratio
    max_range = 1
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')


    multi = 1
    rX = [0, R]
    rY = [0, R]
    rZ = [0, R]

    foreground = [
        [[rX[0],rX[1]],[rY[0],rY[0]],[rZ[0],rZ[0]]],
        [[rX[0],rX[1]],[rY[0],rY[0]],[rZ[1],rZ[1]]],
        [[rX[0],rX[1]],[rY[1],rY[1]],[rZ[1],rZ[1]]],
        [[rX[0],rX[0]],[rY[0],rY[1]],[rZ[1],rZ[1]]],
        [[rX[1],rX[1]],[rY[0],rY[1]],[rZ[0],rZ[0]]],
        [[rX[1],rX[1]],[rY[0],rY[1]],[rZ[1],rZ[1]]],
        [[rX[0],rX[0]],[rY[0],rY[0]],[rZ[0],rZ[1]]],
        [[rX[1],rX[1]],[rY[0],rY[0]],[rZ[0],rZ[1]]],
        [[rX[1],rX[1]],[rY[1],rY[1]],[rZ[0],rZ[1]]]
    ]
    background = [
        [[rX[0],rX[1]],[rY[1],rY[1]],[rZ[0],rZ[0]]],
        [[rX[0],rX[0]],[rY[0],rY[1]],[rZ[0],rZ[0]]],
        [[rX[0],rX[0]],[rY[1],rY[1]],[rZ[0],rZ[1]]],
    ]
    # for s, e in combinations(np.array(list(product(rX, rY, rZ))), 2):
    #     r = np.sum(np.abs(s-e))
    #     if r == rX[1]-rX[0] or r == rY[1]-rY[0] or r == rZ[1]-rZ[0]:
    #         ax.plot(*zip(s, e), color="black")

    for line in background:
        ax.plot(line[0],line[1],line[2], color=(0,0,0,0.6), linestyle=':')

    ax.plot(
        X, Y, Z, linestyle='none',
        markerfacecolor=(0.75,0.14,0.14,0.5) if R==1 else (0,0.2,1,0.5),
        markeredgecolor=(0.75,0.14,0.14,0.8) if R==1 else (0,0.2,1,0.8),
        markersize=4,
        markeredgewidth=1,
        marker='o'
    )

    for line in foreground:
        ax.plot(line[0],line[1],line[2], color=(0,0,0,0.6), linestyle=':')

    # length = 0.3
    # offset = 0.1
    # lo = -0.3
    # ax.plot([lo,lo+length], [lo,lo], [lo,lo], color='black', lw=1)
    # ax.text(lo+length + offset,lo,lo,r"\small$x$",va='center')
    # ax.plot([lo,lo], [lo,lo+length], [lo,lo], color='black', lw=1)
    # ax.text(lo,lo+length + offset,lo,r"\small$y$",va='bottom', ha='left')
    # ax.plot([lo,lo], [lo,lo], [lo,lo+length], color='black', lw=1)
    # ax.text(lo,lo,lo+length + offset,r"\small$z$",ha='center')



    # ax.xaxis.pane.fill = False
    # ax.xaxis.pane.set_edgecolor('white')
    # ax.yaxis.pane.fill = False
    # ax.yaxis.pane.set_edgecolor('white')
    # ax.zaxis.pane.fill = False
    # ax.zaxis.pane.set_edgecolor('white')
    # ax.grid(False)
    ax.set_axis_off()
    ax.view_init(azim=-75, elev=15)
    ax.dist = 9

    fig.tight_layout()
    # plt.show()
    fig.savefig(('Large' if R==1 else 'Small') + '.pdf',transparent=True)





# %%
