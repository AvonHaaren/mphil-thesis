import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import subprocess
from mpl_toolkits.axes_grid1 import make_axes_locatable



mpl.use('pgf')
pgf_with_latex = {                      # setup matplotlib to use latex output
    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex
    "font.family": "serif",
    "pgf.preamble": [
        r'\usepackage[utf8]{inputenc}',    # use utf8 fonts
        r'\usepackage[T1]{fontenc}',
        r'\usepackage{amsmath}',
        r'\DeclareUnicodeCharacter{2212}{$-$}'
    ]
}
# plots will be generated using this preamble
mpl.rcParams.update(pgf_with_latex)


def latexplot(filename, keeppgf=False, keeptex=False):
    header = r'''\documentclass[11pt]{standalone}

\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[UKenglish]{babel}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{gensymb}
\usepackage{graphicx}
\usepackage{siunitx}
\sisetup{locale = UK,
    per-mode = fraction,
    range-phrase = {~to~}}
\usepackage{pgfplots}
\pgfplotsset{compat=1.14}
\DeclareUnicodeCharacter{2212}{$-$}

\begin{document}
'''

    footer = r'''
\end{document}'''

    main = r'   \input{'+filename+'.pgf}'

    content = header + main + footer

    with open(filename+'.tex', 'w') as f:
        f.write(content)

    subprocess.check_output(
        'pdflatex '+filename+'.tex',
        shell=True)

    if keeppgf is False:
        os.unlink(filename+'.pgf')

    if keeptex is False:
        os.unlink(filename+'.tex')
    os.unlink(filename+'.aux')
    os.unlink(filename+'.log')

    return



def myGauss(x):
    return 0.2 + 0.8*np.exp(-(x-6.5)**2 / 100)


def myOffset(x):
    return 0.01*(x-2.9)*(x-3.4)*(x-5.3)*(x-6.3)*(x-7.1) + 0.12

x = np.linspace(0,10,5000)
yT = np.asarray([1.0 if x < 3 or x > 7 else 0.0 for x in x])
yC = np.asarray([myGauss(x) if x < 3 or x > 7 else myOffset(x) for x in x])


size = (3.6,2.2)


fig = plt.figure(figsize=size)

plt.plot(x, yC, color='black')
plt.plot(x, yT, color='black', ls='-.', alpha=0.7)

plt.fill_between(x, yC, yT, where=(yT > yC), facecolor='blue', alpha=0.5)
plt.fill_between(x, yT, yC, where=(yT <= yC), facecolor='red', alpha=0.5)
plt.box()
plt.tick_params(bottom=False,left=False,labelleft=False,labelbottom=False)

# div = make_axes_locatable(ax)
# arrowax = div.append_axes("left", size="3%", pad=0, frameon=False)
plt.arrow(-0.6, -0.05, 0, 1.1, fc='k', ec='k', lw = 1., 
             head_width=0.2, head_length=0.05, overhang = 0.3, 
             length_includes_head= True, clip_on = False)
plt.ylabel(r"Intensity (arb.\ units)", labelpad=10)

fig.savefig('sketch.pgf', bbox_inches="tight", pad_inches=0.022)
latexplot("sketch")


fig2 = plt.figure(2, figsize=size)
plt.box()
plt.tick_params(bottom=False,left=False,labelleft=False,labelbottom=False)
diff = yC - yT
yNT = np.where(yC > yT, -diff + np.max(diff), 1 + np.min(diff) - diff)
yNC = np.where(yC > yT, np.max(diff), 1 + np.min(diff))
plt.plot(x, yNT, color='black', ls='-.', alpha=0.7)
plt.plot(x, yNC, color='black')
fig2.savefig('sketch1.pgf', bbox_inches="tight", pad_inches=0.022)
latexplot("sketch1")


fig3 = plt.figure(3, figsize=size)
plt.box()
plt.tick_params(bottom=False,left=False,labelleft=False,labelbottom=False)
diff = yC - yT
yNT = np.where(yC > yT, -diff + np.max(diff), (1 + np.min(diff))/yC)
yNC = np.where(yC > yT, np.max(diff), 1 + np.min(diff))
plt.plot(x, yNT, color='black', ls='-.', alpha=0.7)
plt.plot(x, yNC, color='black')
fig2.savefig('sketch1_correct.pgf', bbox_inches="tight", pad_inches=0.022)
latexplot("sketch1_correct")
