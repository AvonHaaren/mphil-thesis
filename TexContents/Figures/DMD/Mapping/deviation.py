import imageio
import os
import subprocess
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
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



target = imageio.imread('twoshapes-target.png')
camera = imageio.imread('twoshapes-mapped.png')



t = np.asarray(target).astype(float)
c = np.asarray(camera[:,:,1]).astype(float)

fig = plt.figure(figsize=(5.5,3),dpi=300)
ax = plt.gca()
im = ax.imshow(c-t, cmap='inferno')
plt.tick_params(bottom=False,labelbottom=False,
left=False,labelleft=False)

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="7%", pad=0.1)

plt.colorbar(im, cax=cax)
fig.savefig("twoshapes-error.pgf", bbox_inches="tight", pad_inches=0.0)
latexplot('twoshapes-error')

