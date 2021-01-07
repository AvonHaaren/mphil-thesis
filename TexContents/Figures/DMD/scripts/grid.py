import imageio
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import json
from pathlib import Path
import cmocean as cmo

from mpl_toolkits.axes_grid1 import make_axes_locatable

mpl.rc('text', usetex=True)


colourPath = Path().home() / \
    "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/colours.json"
with open(colourPath) as f:
    j = json.load(f)
    src = j["cmap_src"]
    name = j["cmap"]
    if src == "mpl":
        cmap = mpl.cm.get_cmap(name)
    elif src == "cmocean":
        cmap = cmo.cm.cmap_d[name]

    clist = j["crgb_list"]


# color = clist[1]
# newC = mpl.colors.rgb_to_hsv(color[:3])
# newC[2] = 0.5
# newC = mpl.colors.hsv_to_rgb(newC)
# color = newC
# N = 256
# vals = np.ones((N, 4))
# vals[:, 0] = np.linspace(color[0], 1, N)
# vals[:, 1] = np.linspace(color[1], 1, N)
# vals[:, 2] = np.linspace(color[2], 1, N)
# newcmp = ListedColormap(vals)

# newcmp = cmo.cm.ice

figPath = Path().home() / \
    "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/DMD"
im = imageio.imread(figPath / 'grid-unmapped.bmp')

dpi = 72
scale = 1
imageextent = (220 * scale, 454 * scale, 140 * scale, 318 * scale)

im = np.asarray(im).astype(float)
im = im[imageextent[2]:imageextent[3], imageextent[0]:imageextent[1]]
fig = plt.figure()
spaceRight = 1.25
ax = plt.Axes(fig, [0., 0., 1. / spaceRight, 1.])
sh = np.shape(im)
fig.set_size_inches(sh[1] * spaceRight / dpi, sh[0] / dpi)
ax.set_axis_off()
fig.add_axes(ax)
ax.imshow(im, cmap='gray', extent=imageextent, interpolation='nearest')
# ax.imshow(np.array([[[255, 255, 255, 0]]], dtype='uint8'),
#           cmap='gray', extent=imageextent)


# trans = mpl.transforms.offset_copy(ax.transAxes,
#                                    fig=fig, x=0.06, y=-0.06, units='inches')

axins = ax.inset_axes([0.73,  # 0.65,
                       0.5, 0.47, 0.47])
x1, x2, y1, y2 = 318, 354, 188, 224
x1 = scale * x1
x2 = scale * x2
y1 = scale * y1
y2 = scale * y2

vmax = int(np.max(im[y1 - imageextent[2]:y2 - imageextent[2],
                     x1 - imageextent[0]:x2 - imageextent[0]]))

vmin = 0

vmax = vmax if (vmax - vmin) % 2 == 0 else vmax + 1
plot = axins.imshow(im, extent=imageextent, cmap=cmap,
                    vmin=vmin, vmax=vmax, interpolation='nearest')
# sub region of the original image

axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels('')
axins.set_yticklabels('')
axins.set_axis_off()

divider = make_axes_locatable(axins)
cax = divider.append_axes("right", size="12%", pad=0.04)

plt.colorbar(plot, cax=cax, ticks=[vmin, (vmax + vmin) // 2, vmax])

ax.indicate_inset_zoom(axins)


plt.show()

fig.savefig(figPath / "gridWithInset.pdf")
