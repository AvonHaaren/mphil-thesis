import imageio
import os
import subprocess
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable



dev = imageio.imread('100percent-uncorrected-EXP160microseconds.bmp')
corr = imageio.imread('100percent-corrected-EXP500microseconds.bmp')

for im in [dev,corr]:
    fig = plt.figure()
    ax = plt.gca()
    im = ax.imshow(im, cmap='Blues')
    ax.axis('off')
    fig.tight_layout()
    plt.show()



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

