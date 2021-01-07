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


figPath = Path().home() / \
    "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/DMD"


source = figPath / "Results/NoiseExamples"
for i in [35]:
    im = imageio.imread(source / (str(i) + '.png'))

    dpi = 72 * 3
    scale = 1

    im = np.asarray(im[:, :, 1]).astype(float)

    w = im.shape[1]
    h = im.shape[0]

    imageextent = (363, 662, 235, 534)
    im = im[imageextent[2]:imageextent[3], imageextent[0]:imageextent[1]]
    fig = plt.figure()
    spaceRight = 1.18  # 1.18
    ax = plt.Axes(fig, [0., 0., 1. / spaceRight, 1.])
    sh = np.shape(im)
    fig.set_size_inches(sh[1] * spaceRight / dpi, sh[0] / dpi)
    ax.set_axis_off()
    fig.add_axes(ax)

    vmax = int(np.max(im))

    vmin = int(np.min(im))

    vmax = vmax if (vmax - vmin) % 4 == 0 else vmax + 1
    vmin = vmin if (vmax - vmin) % 4 == 0 else vmin - 1

    plot = ax.imshow(im, cmap=cmap, extent=imageextent, vmin=vmin, vmax=vmax,
                     interpolation='nearest')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="12%", pad=0.04)

    plt.colorbar(plot, cax=cax, ticks=[
                 vmin,
                 vmin + 1 * (vmax - vmin) // 4,
                 vmin + 2 * (vmax - vmin) // 4,
                 vmin + 3 * (vmax - vmin) // 4,
                 vmax])

    plt.show()

    fig.savefig(figPath / ("height" + str(i) + ".pdf"))
