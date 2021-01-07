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

example = "25"

histogram = True


source = Path().home() / \
    "Google Drive/Studium/Cambridge/DMD/Tests"

bigData = [np.array([]).astype(float), np.array([]).astype(float)]
for old in [True, False]:
    # old = True

    numbers = np.arange(1, 21) if old else np.arange(1, 41)
    numbers = numbers.astype(int)
    Nsource = source / \
        "Old Magnification/LengthScale" if old else (source / "LengthScale")

    for n in numbers:
        example = str(n) if n >= 10 else "0" + str(n)

        offs = imageio.imread(Nsource / (example + '-offs.bmp'))
        offs = np.asarray(offs[:, :, 1]).astype(float)
        corr = imageio.imread(Nsource / (example + '-final.bmp'))
        corr = np.asarray(corr[:, :, 1]).astype(float)

        names = {0: "-offs", 1: "-corr", 2: "-add"}

        if not histogram:
            for i, im in enumerate([offs, corr, offs + corr]):
                dpi = 72 * 3
                scale = 1

                im = np.asarray(im).astype(float)
                edges = True
                off = 7 if edges else 0
                imageextent = (363 + off, 662 - off, 235 + off, 534 - off)
                im = im[imageextent[2]:imageextent[3],
                        imageextent[0]:imageextent[1]]

                fig = plt.figure()
                spaceRight = 1.23 if dpi == 72 * 3 else 1.16  # 1.18
                ax = plt.Axes(fig, [0., 0., 1. / spaceRight, 1.])
                sh = np.shape(im)
                fig.set_size_inches(sh[1] * spaceRight / dpi, sh[0] / dpi)
                ax.set_axis_off()
                fig.add_axes(ax)

                vmax = int(np.max(im))

                vmin = int(np.min(im))

                vmax = vmax if (vmax - vmin) % 4 == 0 else (vmax // 4 + 1) * 4
                vmin = vmin if (vmax - vmin) % 2 == 0 else vmin - 1

                plot = ax.imshow(im, cmap=cmap, extent=imageextent,
                                 vmin=vmin,
                                 vmax=vmax,
                                 interpolation='nearest')

                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size="12%", pad=0.04)

                plt.colorbar(plot, cax=cax, ticks=[
                    vmin,
                    vmin + 1 * (vmax - vmin) // 4,
                    vmin + 2 * (vmax - vmin) // 4,
                    vmin + 3 * (vmax - vmin) // 4,
                    vmax])

                # print(im[7:-7, 7:-7].mean(), im[7:-7, 7:-7].std())

                print(example)
                # plt.show()
                fig.savefig(
                    Nsource / (example + names[i] + ".pdf"))
                plt.close()
        else:

            threshold = 8 if old else 18

            if n > threshold:
                # fig = plt.figure()
                data = offs + corr
                data = data[242:-242, 370:-370].flatten()

                data = (data - data.mean()) / 255

                index = 0 if old else 1
                bigData[index] = np.append(bigData[index], data)

                # values, bins = np.histogram(data, bins=30)
                # values = values / values.max()

                # binwidth = bins[1] - bins[0]

                # plt.plot(bins[:-1] + binwidth / 2, values)
                # plt.title(("2.2:1 " if old else "5:1 ") +
                #           example + " RMS: {:2.2f} \%".format(100 * data.std()))
                # plt.xlabel("(I - Imean) / 255")
                # plt.ylabel("occurrences")

                # fig.set_tight_layout(True)
                # plt.show()
                # plt.close()

output = Path().home() / \
    "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/DMD/Results/ErrorAnalysis"
for i, data in enumerate(bigData):
    pd.DataFrame(data).to_csv(
        output / ("resOld.csv" if i == 0 else "resNew.csv"),
        header=None, index=None)
    print(len(data))
    fig = plt.figure()
    values, bins = np.histogram(data, bins=50)
    values = values / len(data)

    binwidth = bins[1] - bins[0]

    plt.plot(bins[:-1] + binwidth / 2, values)
    print(("2.2:1 " if i == 0 else "5:1 ") +
          " RMS: {:2.2f} \%".format(100 * data.std()))
    plt.xlabel(r"$(I - \langle I\rangle)$/255")
    plt.ylabel("Statistic frequency")

    fig.set_tight_layout(True)
    fig.savefig(output / ("resOld.pdf" if i == 0 else "resNew.pdf"))
    plt.close()
