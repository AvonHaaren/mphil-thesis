# %%
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib as mpl
from pathlib import Path
import json


mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage{lmodern}'
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = "Latin Modern"
mpl.rcParams['font.size'] = 12


fig = plt.figure(3, figsize=(5.5, 3.5))
ax = fig.add_subplot()


p = Path().home() / "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/colours.json"
with open(p) as f:
    j = json.load(f)
    clist = j["crgb_list"]

cPSD = tuple(clist[3][:3])
cT = tuple(clist[4][:3])
# cPSD = (0.15, 0.35, 0.15)
# cT = (0.125, 0.125, 0.125)
x = np.linspace(0, 1.1, 200)
yPSD = np.exp(x * 10) / np.exp(10)
yT = np.exp(-4 * x)

ax.tick_params(axis='y', labelcolor=cT)

ax.plot(x, yT, c=cT)
ax2 = ax.twinx()
ax2.plot(x, yPSD, c=cPSD)
ax2.set_ylabel(r"Phase space density", color=cPSD, rotation=-90, labelpad=10)
ax2.tick_params(axis='y', labelcolor='black')

ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])
ax.set_ylabel(r"Temperature (arb.\ units)", color=cT, labelpad=10)
ax2.get_yaxis().set_ticks([0, 1])
ax.set_xlabel(r"Time (arb.\ units)", labelpad=10)
plt.xlim(0, 1)
plt.ylim(bottom=-0.01, top=1.05)

fig.tight_layout()
fig.savefig(Path().home() /
            "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/Evap/BoxTrapEvaporation/baseplot.pdf")


# %%
