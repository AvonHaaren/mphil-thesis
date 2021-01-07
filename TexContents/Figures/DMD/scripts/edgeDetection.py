import imageio
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import json
from pathlib import Path
import cmocean as cmo
import pandas as pd

from mpl_toolkits.axes_grid1 import make_axes_locatable

mpl.rc('text', usetex=True)
rcPreamble = '\\usepackage{lmodern}\n\\usepackage{amsmath}'
mpl.rc('text.latex', preamble=rcPreamble)
mpl.rc('font', family='serif')


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

examples = ["05", "15"]

histogram = True

if not histogram:
    source = Path().home() / \
        "Google Drive/Studium/Cambridge/DMD/Tests/Old Magnification/EdgeDetection"
    for i in examples:
        orig = imageio.imread(source / (i + '-orig.bmp'))
        orig = np.asarray(orig[:, :, 1]).astype(float)
        corr = imageio.imread(source / (i + '-final.bmp'))
        corr = np.asarray(corr[:, :, 1]).astype(float)
        im = corr - orig

        dpi = 72 * 3
        scale = 1

        im = np.asarray(im).astype(float)

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

        # vmin = int(np.min(im))
        vmin = 0

        vmax = vmax if (vmax - vmin) % 4 == 0 else (vmax // 4 + 1) * 4
        # vmin = vmin if (vmax - vmin) % 4 == 0 else vmin - 1

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
        fig.savefig(figPath / ("EdgeDetectionAddedIntensity" + i + ".pdf"))


else:
    output = Path().home() / \
        "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/DMD/Results/ErrorAnalysis"
    numbers = np.arange(1, 21)
    source = Path().home() / \
        "Google Drive/Studium/Cambridge/DMD/Tests/"
    for old in [True, False]:
        Nsource = (
            source / "Old Magnification/EdgeDetection") if old else (source / "EdgeDetection")

        bigData = np.array([]).astype(float)

        for n in numbers:
            example = str(n) if n >= 10 else "0" + str(n)
            corr = imageio.imread(Nsource / (example + '-final.bmp'))
            corr = np.asarray(corr[:, :, 1]).astype(float)

            im = corr.astype(float)
            im = im[235 + n: -235 - n, 363 + n: -363 - n].flatten()
            data = (im - im.mean()) / 255

            bigData = np.append(bigData, data)

            # values, bins = np.histogram(data, bins=30)
            # values = values / values.max()

            # binwidth = bins[1] - bins[0]

            # fig = plt.figure()

            # plt.plot(bins[:-1] + binwidth / 2, values)
            # plt.title(("2.2:1 " if old else "5:1 ") +
            #           example + " RMS: {:2.2f} \%".format(100 * data.std()))
            # plt.xlabel("(I - Imean) / 255")
            # plt.ylabel("occurrences")

            # fig.set_tight_layout(True)
            # fig.savefig(Nsource / (example + '-histogram.pdf'))
            # plt.close()

        pd.DataFrame(bigData).to_csv(
            output / ("edgeOld.csv" if old else "edgeNew.csv"),
            header=None, index=None)
        print(len(bigData))

        values, bins = np.histogram(bigData, bins=50)
        values = values / len(bigData)
        fig = plt.figure()

        binwidth = bins[1] - bins[0]

        plt.plot(bins[:-1] + binwidth / 2, values)
        print(("2.2:1 " if old else "5:1 ") +
              " RMS: {:2.2f} \%".format(100 * bigData.std()))
        plt.xlabel(r"$(I - \langle I\rangle)$/255")
        plt.ylabel("Statistic frequency")

        fig.set_tight_layout(True)
        fig.savefig(output / ("edgeOld.pdf" if old else "edgeNew.pdf"))
        plt.close()
