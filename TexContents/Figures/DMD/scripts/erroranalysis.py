import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
import cmocean as cmo
from latexplot import latexplot


pgf_preamble = "\\usepackage[utf8]{inputenc}\n" + \
    "\\usepackage[T1]{fontenc}\n" + \
    "\\usepackage[detect-all,locale=UK]{siunitx}\n" + \
    "\\usepackage{lmodern}\n" + \
    "\\usepackage{amsmath}\n" + \
    "\\DeclareUnicodeCharacter{2212}{$-$}"

pgf_with_latex = {                      # setup matplotlib
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "pgf.preamble": pgf_preamble
}
mpl.rcParams.update(pgf_with_latex)


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

c5x = clist[1]
c2x = clist[0]


def desaturate(color, amount, alpha=1):
    hsv = mpl.colors.rgb_to_hsv(color[:3])
    hsv = (hsv[0], hsv[1] * amount, hsv[2])
    return tuple(mpl.colors.hsv_to_rgb(hsv)) + (alpha,)


source = Path().home() / \
    "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/DMD/Results/ErrorAnalysis"
output = Path().home() / \
    "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/DMD/Results/"

edgeOld = pd.read_csv(source / "edgeOld.csv", header=None)
edgeNew = pd.read_csv(source / "edgeNew.csv", header=None)
resOld = pd.read_csv(source / "resOld.csv", header=None)
resNew = pd.read_csv(source / "resNew.csv", header=None)


fig, ax = plt.subplots(nrows=1, ncols=2, sharey='all', figsize=(6.5, 2.5))
ax1 = fig.add_subplot(111, frame_on=False)
plt.tick_params(top=False, bottom=False, left=False, right=False,
                labeltop=False, labelbottom=False,
                labelleft=False, labelright=False)
plt.grid(False)
plt.xlabel(r"$(I - \langle I\rangle)$/255", labelpad=19)

old = False
logscale = True
yLimBottom = 2e-7
for old in [False, True]:
    print("2.2:1" if old else "5:1")
    data = np.append(resOld, edgeOld) if old else np.append(resNew, edgeNew)

    nBins = 25
    bins = np.linspace(data.min(), data.max(), nBins)
    binwidth = bins[1] - bins[0]
    binsLower = np.arange(0.5 * binwidth, - data.min() +
                          binwidth, step=binwidth)
    binsHigher = np.arange(0.5 * binwidth, data.max() +
                           binwidth, step=binwidth)
    bins = np.append(-binsLower[::-1], binsHigher)

    values, bins = np.histogram(data, bins=bins, density=False)
    print(len(values))
    values = values / len(data)

    binwidth = bins[1] - bins[0]

    for threshold in [0.9, 0.95, 0.99, 0.999, 0.9998]:
        print(threshold, np.quantile(np.abs(data), threshold))

    # threshold95 = 0.0315 if old else 0.0298
    # threshold99 = 0.0487 if old else 0.0457
    # center = values.argmax()
    # print(r"95%:", len(data[np.abs(data) > threshold95]) / len(data))
    # print(r"99%:", len(data[np.abs(data) > threshold99]) / len(data))
    # for i in range(1, 20):
    #     print(i * binwidth, values[center - i:center + i].sum())

    c = c2x if old else c5x

    axI = 1 if old else 0
    label = "Magnification 2.2:1" if old else "Magnification 5:1"

    plotbins = bins[:-1] + binwidth / 2
    if logscale:
        plotbins = np.delete(plotbins, np.where(values == 0))
        values = np.delete(values, np.where(values == 0))

        ax[axI].set_yscale('log', nonpositive='clip')
        ax[axI].set_ylim(bottom=yLimBottom, top=2)
    bars = ax[axI].bar(plotbins, values, bottom=yLimBottom / 2 if logscale else None,
                       width=binwidth * 0.8,
                       color=desaturate(c, 0.3, alpha=0.35),
                       edgecolor=c, linewidth=1.5, label=label)
    print(data.std())

    # ax[axI].plot(np.NaN, np.NaN, '-', color='none',
    #              label="$\\Delta_\\mathrm{{RMS}}=\\num{{{:.2e}}}$".format(data.std()))

    ax[axI].text(s="$\\Delta_\\mathrm{{RMS}}=\\SI{{{:1.2f}}}{{\\percent}}$".format(100 * data.std()),
                 x=0.98, y=0.98, ha="right",
                 va="top", transform=ax[axI].transAxes)
    # ax[axI].text(s="$\\Delta_\\mathrm{{RMS}}=\\num{{{:.2e}}}$".format(data.std()),
    #              x=0, y=1.01, ha="left",
    #              va="bottom", transform=ax[axI].transAxes)
    # print(bars.patches[10])
    # bars.patches[10].set_y(bars.patches[10].get_y() + 0.001)
    # print(bars.patches[10])
    # bars.patches[10].set_height(bars.patches[10].get_height() - 0.001)
    # print(bars.patches[10])


ax[0].set_ylabel("Fraction of pixels", labelpad=9)
locmaj = mpl.ticker.LogLocator(base=10, numticks=12)
ax[0].yaxis.set_major_locator(locmaj)
locmin = mpl.ticker.LogLocator(
    base=10.0, subs=(0.2, 0.4, 0.6, 0.8), numticks=12)
ax[0].yaxis.set_minor_locator(locmin)
ax[0].yaxis.set_minor_formatter(mpl.ticker.NullFormatter())
plt.setp(ax[0].get_yticklabels()[::2], visible=False)

handles0, labels0 = ax[0].get_legend_handles_labels()
handles1, labels1 = ax[1].get_legend_handles_labels()
# ax[0].legend(handles0, ["2.2:1"])
# ax[1].legend(handles1, ["5:1"])
handles0.extend(handles1)
labels0.extend(labels1)

ax[0].legend(handles=handles0, labels=labels0, loc='lower center',
             bbox_to_anchor=(1.0375, 1.0), ncol=2, framealpha=0.7)
fig.subplots_adjust(wspace=0.075)

fig.savefig(output / 'ErrorAnalysis.pgf',
            bbox_inches="tight", pad_inches=0.05)
latexplot(output / 'ErrorAnalysis.pgf')
