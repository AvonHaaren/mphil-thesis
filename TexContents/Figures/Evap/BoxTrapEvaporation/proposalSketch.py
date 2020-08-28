import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import k as kB, u
from latexplot import latexplot
import matplotlib as mpl

pgf_with_latex = {                      # setup matplotlib
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "pgf.preamble": [
        r"\usepackage[utf8]{inputenc}",    # use utf8 fonts
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[detect-all,locale=UK]{siunitx}",
        r"\usepackage{amsmath}",
        r"\DeclareUnicodeCharacter{2212}{$-$}"
    ]
}
mpl.rcParams.update(pgf_with_latex)

