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


source = figPath / "Results/NoiseExamples"
im = imageio.imread(source / '35.png')

dpi = 72 * 4
scale = 1


im = np.asarray(im[:, :, 1]).astype(float)

w = im.shape[1]
h = im.shape[0]

imageextent = ((w - 300 * scale) // 2, (w + 300 * scale) // 2,
               (h - 300 * scale) // 2, (h + 300 * scale) // 2)
imageextent = (0, w, 0, h)
print(imageextent)
im = im[imageextent[2]:imageextent[3], imageextent[0]:imageextent[1]]
fig = plt.figure()
spaceRight = 1.24  # 1.18
ax = plt.Axes(fig, [0., 0., 1. / spaceRight, 1.])
sh = np.shape(im)
fig.set_size_inches(sh[1] * spaceRight / dpi, sh[0] / dpi)
ax.set_axis_off()
fig.add_axes(ax)
ax.imshow(im, cmap='gray', extent=imageextent,
          interpolation='nearest', vmax=255)
# ax.imshow(np.array([[[255, 255, 255, 0]]], dtype='uint8'),
#           cmap='gray', extent=imageextent)

trans = mpl.transforms.offset_copy(ax.transAxes,
                                   fig=fig, x=0.06, y=-0.06, units='inches')

axins = ax.inset_axes([0.73,  # 0.65,
                       0.5, 0.47, 0.47])
insetsize = 100
x1, y1 = imageextent[0] + 50 * scale, imageextent[2] + 50 * scale
x2, y2 = x1 + insetsize * scale, y1 + insetsize * scale

x1, x2 = (w - 300 * scale) // 2 + 1, (w + 300 * scale) // 2 - 1
y1, y2 = (h - 300 * scale) // 2 + 1, (h + 300 * scale) // 2 - 1

print(x1, x2, y1, y2)

print(im[234:234,
         362:362].shape)
vmax = int(np.max(im[y1:y2,
                     x1:x2]))

vmin = int(np.min(im[y1:y2,
                     x1:x2]))

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

fig.savefig(figPath / "noiseExample.pdf")
