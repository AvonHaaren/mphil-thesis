# %%
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.colors import LightSource
from matplotlib import cm
from itertools import combinations, product
import matplotlib as mpl

mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = "Computer Modern Roman"
mpl.rcParams['font.size'] = 12



s = np.linspace(0, 1, 200)


def makeXY(s, alpha, costheta):
    xmax = np.sin(np.arccos(costheta)) / np.sin(alpha*np.pi/360)
    ymax = np.sin(np.arccos(costheta)) / np.cos(alpha*np.pi/360)
    x = np.where(s >= 0.75, xmax*(s-0.75)/0.25, 
                    np.where(s >= 0.5, -xmax *(1 - (s-0.5)/.25),
                             np.where(s >= 0.25, -xmax*(s-0.25)/0.25, 
                                      xmax*(1 - s/0.25))))
    y = np.where(s >= 0.75, ymax*(1 - (s-0.75)/0.25), 
                    np.where(s >= 0.5, ymax *((s-0.5)/.25),
                             np.where(s >= 0.25, -ymax*(1 - (s-0.25)/0.25), 
                                      -ymax*s/0.25)))
    return (x,y)


# plt.plot(*makeXY(s,157.5, -1))
# plt.show()
# %%






u = np.linspace(0,1,5)
v = np.cos(np.linspace(np.pi,0,201))

uu, vv = np.meshgrid(u, v)

for angle in [90, 157.5]:
    fig = plt.figure(figsize=(3,2.5))
    ax = fig.add_subplot(111, projection='3d')

    X, Y = makeXY(uu, angle, vv)
    Z = np.outer(v, np.ones(len(u)))


    Z_light = np.outer(np.linspace(-1,1,len(v)), np.ones(len(u)))
    Z_light = 10 - Z_light
    light = LightSource(0,50)
    rgb = np.ones((Z.shape[0], Z.shape[1], 3))
    c = '#1f77b4' if angle < 100 else '#ff7f0e'
    rgbC = mpl.colors.to_rgb(c)
    illuminated_surface = light.shade_rgb(rgb*np.array(rgbC), Z_light)
    other_color = light.shade(Z_light, plt.get_cmap('Oranges'))





    # Create cubic bounding box to simulate equal aspect ratio
    max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')


    multi = 1.2
    rX = [multi*X.min(), multi*X.max()]
    rY = [multi*Y.min(), multi*Y.max()]
    rZ = [multi*Z.min(), multi*Z.max()]
    # for s, e in combinations(np.array(list(product(rX, rY, rZ))), 2):
    #     r = np.sum(np.abs(s-e))
    #     if r == rX[1]-rX[0] or r == rY[1]-rY[0] or r == rZ[1]-rZ[0]:
    #         ax.plot(*zip(s, e), color="black")
    length = 1.5
    offset = 0.1 if angle < 100 else 0.25
    ax.plot([rX[0],rX[0]+length], [rY[0],rY[0]], [rZ[0],rZ[0]], color='black', lw=0.7)
    ax.text(rX[0]+length + offset,rY[0],rZ[0],r"$x$",va='center')
    ax.plot([rX[0],rX[0]], [rY[0],rY[0]+length], [rZ[0],rZ[0]], color='black', lw=0.7)
    ax.text(rX[0],rY[0]+length + offset,rZ[0],r"$y$",va='bottom', ha='left')
    ax.plot([rX[0],rX[0]], [rY[0],rY[0]], [rZ[0],rZ[0]+length], color='black', lw=0.7)
    ax.text(rX[0],rY[0],rZ[0]+length + offset,r"$z$",ha='center')


    # ax.plot_wireframe(X, Y, Z, color='black', rcount=8, ccount=8, alpha=1)
    ax.plot_surface(X, Y, Z, facecolors=illuminated_surface, alpha=1)
    # ax.xaxis.pane.fill = False
    # ax.xaxis.pane.set_edgecolor('white')
    # ax.yaxis.pane.fill = False
    # ax.yaxis.pane.set_edgecolor('white')
    # ax.zaxis.pane.fill = False
    # ax.zaxis.pane.set_edgecolor('white')
    # ax.grid(False)
    ax.set_axis_off()
    ax.view_init(azim=-67, elev=38)
    ax.dist = 4.2 if angle > 100 else 6.7

    fig.tight_layout()
    fig.savefig('SteinMetzPython' + ('_Angle' if angle > 100 else '') + ".pdf")


# %%
