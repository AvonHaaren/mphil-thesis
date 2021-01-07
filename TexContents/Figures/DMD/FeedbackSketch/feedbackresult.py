import imageio
import os
import subprocess
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import json
from pathlib import Path
import cmocean as cmo
from matplotlib.colors import ListedColormap


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


color = clist[1]
newC = mpl.colors.rgb_to_hsv(color[:3])
newC[2] = 0.5
newC = mpl.colors.hsv_to_rgb(newC)
color = newC
N = 256
vals = np.ones((N, 4))
vals[:, 0] = np.linspace(color[0], 1, N)
vals[:, 1] = np.linspace(color[1], 1, N)
vals[:, 2] = np.linspace(color[2], 1, N)
newcmp = ListedColormap(vals)

# newcmp = cmo.cm.ice

figPath = Path().home() / \
    "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/DMD"
dev = imageio.imread(figPath / '100percent-uncorrected-EXP160microseconds.bmp')
corr = imageio.imread(figPath / '100percent-corrected-EXP500microseconds.bmp')

dpi = 72
for i, im in enumerate([dev, corr]):
    im = np.asarray(im[:, :, 1]).astype(float)
    fig = plt.figure()
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    sh = np.shape(im)
    fig.set_size_inches(sh[1]/dpi, sh[0]/dpi)
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(im, cmap=newcmp, vmin=(100 if i == 0 else -40),
              vmax=(290 if i == 0 else 375))
    newPath = figPath / ("FeedbackSketch/feedback" +
                         ("Before" if i == 0 else "After") + "Cmap.png")
    fig.savefig(newPath, dpi=dpi)


# fig = plt.figure(figsize=(5.5,3),dpi=300)
# ax = plt.gca()
# im = ax.imshow(c-t, cmap='inferno')
# plt.tick_params(bottom=False,labelbottom=False,
# left=False,labelleft=False)

# divider = make_axes_locatable(ax)
# cax = divider.append_axes("right", size="7%", pad=0.1)

# plt.colorbar(im, cax=cax)
# fig.savefig("twoshapes-error.pgf", bbox_inches="tight", pad_inches=0.0)
# latexplot('twoshapes-error')
