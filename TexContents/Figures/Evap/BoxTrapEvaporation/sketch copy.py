# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import k as kB, u
from latexplot import latexplot
import matplotlib as mpl
from pathlib import Path
import json
import cmocean as cmo

pgf_with_latex = {                      # setup matplotlib
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "pgf.preamble": [
        r"\usepackage[utf8]{inputenc}",    # use utf8 fonts
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[detect-all,locale=UK]{siunitx}",
        r"\usepackage{amsmath}",
        r"\DeclareUnicodeCharacter{2212}{$-$}",
        r"\usepackage{lmodern}"
    ]
}
mpl.rcParams.update(pgf_with_latex)


def mb(v, m, T):
    return np.power(m / (2 * np.pi * kB * T), 3 / 2) * 4 * np.pi * v**2 * np.exp(-m * v**2 / (2 * kB * T))


def vp(m, T):
    return np.sqrt(2 * kB * T / m)


v = np.linspace(0, 0.28, 400)


file = Path().home() / \
    "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/colours.json"
with open(file) as f:
    j = json.load(f)
    src = j["cmap_src"]
    name = j["cmap"]
    if src == "mpl":
        cmap = mpl.cm.get_cmap(name)
    elif src == "cmocean":
        cmap = cmo.cm.cmap_d[name]
    crgbList = j["crgb_list"]


hot = cmap(0.99)[:3]  # (0.75, 0.14, 0.14)
hot = mpl.colors.rgb_to_hsv(hot)
hot[2] = 0.65
hot = tuple(mpl.colors.hsv_to_rgb(hot))
print(hot)
cold = tuple(crgbList[1][:3])  # (0, 0.2, 1)

c1 = hot  # 'red'
c2 = cold  # 'blue'
ymax = 17

# %%
# gs_kw = dict(width_ratios=[1, 1, 1], height_ratios=[2, 1.4])
Fig, axes = plt.subplots(1, 3, figsize=(
    6.5, 1.5), sharey='row')  # og fig height=3

insets = [ax.inset_axes(bounds=(0.5, 0.59, 0.56, 0.37)) for ax in axes]

T1 = mb(v, 87 * u, 50e-6)
T2 = mb(v, 87 * u, 15e-6)
for i in range(3):
    axes[i].set_xlim(0, 0.28)
    axes[i].set_ylim(bottom=0, top=ymax)

axes[0].plot(v, T1, color=c1)
axes[0].fill_between(v, T1, color=c1, alpha=0.3)
v_p = vp(87 * u, 50e-6)
axes[0].text(v_p, 0.5 * mb(v_p, 87 * u, 50e-6),
             r'$T_0$', ha='center', va='center')

cutoff = mb(0.2, 87 * u, 50e-6)
axes[1].plot(v, T1, color=c1)
axes[1].fill_between(v, 0, T1, where=v <= 0.2, alpha=0.3, color=c1)
axes[1].axvline(0.2, 0, cutoff / ymax,
                color='black', alpha=0.9, ls=':')
astyle = '-|>, head_width=0.12'
axes[1].annotate('Cutoff', (0.2, cutoff), xytext=(5, 20),
                 textcoords='offset points', arrowprops=dict(arrowstyle=astyle, color='black'))

axes[2].plot(v, T1, alpha=0.6, color=c1)
axes[2].fill_between(v, 0, T1, where=v <= 0.2, alpha=0.18, color=c1)
axes[2].plot(v, T2, color=c2)
axes[2].fill_between(v, 0, T2, alpha=0.3, color=c2)
axes[2].axvline(0.2, 0, cutoff / ymax,
                color='black', alpha=0.54, ls=':')
v_p = vp(87 * u, 15e-6)
axes[2].text(v_p, 0.5 * mb(v_p, 87 * u, 15e-6),
             r"$T'$", ha='center', va='center')


xTrap = np.linspace(-1, 1, 400)
yTrap = xTrap**2

linewidth = 1.1

insets[0].plot(xTrap, yTrap, color='black', lw=linewidth)
np.random.seed(1)
xpoints = np.random.randn(2000)
ypoints = np.random.exponential(scale=0.4, size=2000)
xplot = xpoints[ypoints > 1.1 * xpoints**2]
yplot = ypoints[ypoints > 1.1 * xpoints**2]
xplot = xplot[yplot < 1.15]
yplot = yplot[yplot < 1.15]
xplot = xplot[::1]
yplot = yplot[::1]
insets[0].scatter(xplot, yplot, color=c1, alpha=0.7,
                  s=24, marker='.', edgecolors='none')

insets[1].plot(xTrap, yTrap, color='black', lw=linewidth)
insets[1].plot(xTrap, np.ma.masked_where(
    yTrap <= 0.7, yTrap), color=(1, 1, 1), alpha=0.78, lw=linewidth)
insets[1].plot(xTrap, 0.7 * np.ones(len(xTrap)),
               linestyle=':', color='black', alpha=0.9, lw=linewidth)
insets[1].text(1.03, 0.7, r"$U'$", va='center', fontsize=8)
xNew = xplot[yplot <= 0.7]
yNew = yplot[yplot <= 0.7]
insets[1].scatter(xNew, yNew, color=c1, alpha=0.7,
                  s=24, marker='.', edgecolors='none')
xNew = xplot[yplot > 0.7]
yNew = yplot[yplot > 0.7]
insets[1].scatter(xNew, yNew, color=c1, alpha=0.3,
                  s=24, marker='.', edgecolors='none')

np.random.seed(2)
xpoints = np.random.randn(1500)
ypoints = np.random.exponential(scale=0.15, size=1500)
xNew = xpoints[ypoints > 1.1 * xpoints**2]
yNew = ypoints[ypoints > 1.1 * xpoints**2]
xNew = xNew[::1]
yNew = yNew[::1]
insets[2].plot(xTrap, np.ma.masked_where(
    yTrap >= 0.7, yTrap), color='black', lw=linewidth)
insets[2].scatter(xplot, yplot, color=c1, alpha=0.2,
                  s=16, marker='.', edgecolors='none')
insets[2].scatter(xNew, yNew, color=c2, alpha=0.7,
                  s=24, marker='.', edgecolors='none')


axes[0].text(-0.04, 1, r'$n(v)$', transform=axes[0].transAxes,
             ha='right', va='top')
for i in range(3):
    insets[i].set_xlim(-1.2, 1.2)
    insets[i].set_ylim(-0.05, 1.2)
    insets[i].tick_params(bottom=False, labelbottom=False,
                          left=False, labelleft=False)
    axes[i].tick_params(bottom=False, labelbottom=False,
                        left=False, labelleft=False)
    insets[i].fill_between(xTrap, yTrap, -1, color='white')
    axes[i].axis("off")
    insets[i].axis("off")

    axes[i].text(1.05, -0.03, r'$v$', transform=axes[i].transAxes,
                 ha='center', va='top')
    insets[i].text(-0.04, 1, r'$U$', transform=insets[i].transAxes,
                   ha='right', va='top', fontsize=8)
    astyle = '-|>, head_width=0.12'
    axes[i].annotate('', xy=(0, 1), xycoords='axes fraction', xytext=(0, -0.03),
                     arrowprops=dict(arrowstyle=astyle, color='black'))
    axes[i].annotate('', xy=(1.05, 0), xycoords='axes fraction', xytext=(-0.03, 0),
                     arrowprops=dict(arrowstyle=astyle, color='black'))

    astyle = '-|>, head_width=0.12'
    insets[i].annotate('', xy=(0, 1), xycoords='axes fraction', xytext=(0, 0),
                       arrowprops=dict(arrowstyle=astyle, color='black'))


path = Path().home() / "Google Drive/Studium/Cambridge/thesis/TexContents/Figures/Evap/"
Fig.savefig(path / 'EvaporationSketch1.pgf',
            bbox_inches='tight', pad_inches=0.02)
latexplot('EvaporationSketch1', keeppgf=True)

# plt.show()
# %%
