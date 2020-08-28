# %%
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


def mb(v,m,T):
    return np.power(m/(2*np.pi*kB * T), 3/2) * 4*np.pi*v**2 * np.exp(-m*v**2/(2*kB*T))


def vp(m,T):
    return np.sqrt(2*kB*T/m)


v = np.linspace(0,0.28,400)

c1 = 'red'
c2 = 'blue'
ymax = 17

# %%
gs_kw=dict(width_ratios=[1,1,1], height_ratios=[2,1.4])
Fig, axes = plt.subplots(2,3, figsize=(6.5,3), sharey='row', gridspec_kw=gs_kw)

T1 = mb(v, 87*u, 50e-6)
T2 = mb(v, 87*u, 15e-6)
for i in range(3):
    axes[0,i].set_xlim(0,0.28)
    axes[0,i].set_ylim(bottom=0, top=ymax)

axes[0,0].plot(v, T1, color=c1)
axes[0,0].fill_between(v, T1, color=c1, alpha=0.3)
v_p = vp(87*u,50e-6)
axes[0,0].text(v_p, 0.5*mb(v_p, 87*u, 50e-6),
               r'$T_0$',ha='center',va='center')

cutoff = mb(0.2,87*u,50e-6)
axes[0,1].plot(v, T1, color=c1)
axes[0,1].fill_between(v, 0, T1, where=v<=0.2, alpha=0.3, color=c1)
axes[0,1].axvline(0.2,0,cutoff/ymax,
                  color='black', alpha=0.9, ls=':')
axes[0,1].annotate('Cutoff', (0.2,cutoff), xytext=(5,20),            
                   textcoords='offset points', arrowprops={'arrowstyle': '->'})

axes[0,2].plot(v, T1, alpha=0.6, color=c1)
axes[0,2].fill_between(v, 0, T1, where=v<=0.2, alpha=0.18, color=c1)
axes[0,2].plot(v, T2, color=c2)
axes[0,2].fill_between(v, 0, T2, alpha=0.3, color=c2)
axes[0,2].axvline(0.2,0,cutoff/ymax,
                  color='black', alpha=0.54, ls=':')
v_p = vp(87*u,15e-6)
axes[0,2].text(v_p, 0.5*mb(v_p, 87*u, 15e-6),
               r"$T'$",ha='center',va='center')

xTrap = np.linspace(-1,1,400)
yTrap = xTrap**2

axes[1,0].plot(xTrap, yTrap, color='black')
np.random.seed(1)
xpoints = np.random.randn(2000)
ypoints = np.random.exponential(scale=0.4, size=2000)
xplot = xpoints[ypoints > 1.1*xpoints**2]
yplot = ypoints[ypoints > 1.1*xpoints**2]
xplot = xplot[yplot < 1.15]
yplot = yplot[yplot < 1.15]
axes[1,0].scatter(xplot,yplot,color='red',alpha=0.7,s=45,marker='.',edgecolors='none')

axes[1,1].plot(xTrap, yTrap, color='black')
axes[1,1].plot(xTrap, np.ma.masked_where(yTrap <= 0.7, yTrap), color=(1,1,1),alpha=0.78)
axes[1,1].plot(xTrap, 0.7*np.ones(len(xTrap)), linestyle=':', color='black', alpha=0.9)
axes[1,1].text(1.03,0.7,r"$U'$",va='center')
xNew = xplot[yplot <= 0.7]
yNew = yplot[yplot <= 0.7]
axes[1,1].scatter(xNew,yNew,color='red',alpha=0.7,s=45,marker='.',edgecolors='none')
xNew = xplot[yplot > 0.7]
yNew = yplot[yplot > 0.7]
axes[1,1].scatter(xNew,yNew,color='red',alpha=0.3,s=45,marker='.',edgecolors='none')

np.random.seed(2)
xpoints = np.random.randn(1500)
ypoints = np.random.exponential(scale=0.15, size=1500)
xNew = xpoints[ypoints > 1.1*xpoints**2]
yNew = ypoints[ypoints > 1.1*xpoints**2]
# xNew = xNew[yNew < 0.86]
# yNew = yNew[yNew < 0.86]
axes[1,2].plot(xTrap, np.ma.masked_where(yTrap >= 0.7, yTrap), color='black')
axes[1,2].scatter(xplot,yplot,color='red',alpha=0.2,s=30,marker='.',edgecolors='none')
axes[1,2].scatter(xNew,yNew,color='blue',alpha=0.7,s=45,marker='.',edgecolors='none')


for i in range(3):
    axes[1,i].set_xlim(-1.2,1.2)
    axes[1,i].set_ylim(-0.05,1.2)
    axes[1,i].tick_params(bottom=False,labelbottom=False,
                          left=False,labelleft=False)
    axes[0,i].tick_params(bottom=False,labelbottom=False,
                          left=False,labelleft=False)
    axes[1,i].fill_between(xTrap,yTrap,-1,color='white')
    axes[0,i].axis("off")
    axes[1,i].axis("off")
    axes[0,i].text(-0.03,1,r'$n(v)$',transform=axes[0,i].transAxes, ha='right',va='center')
    axes[0,i].text(1.05,-0.03,r'$v$',transform=axes[0,i].transAxes, ha='center',va='top')
    axes[1,i].text(-0.03,1,r'$U$',transform=axes[1,i].transAxes, ha='right',va='center')
    astyle = '-|>, head_width=0.12'
    axes[0,i].annotate('', xy=(0,1), xycoords='axes fraction', xytext=(0,-0.03), 
            arrowprops=dict(arrowstyle=astyle, color='black'))
    axes[0,i].annotate('', xy=(1.05,0), xycoords='axes fraction', xytext=(-0.03,0), 
            arrowprops=dict(arrowstyle=astyle, color='black'))
    axes[1,i].annotate('', xy=(0,1), xycoords='axes fraction', xytext=(0,0), 
            arrowprops=dict(arrowstyle=astyle, color='black'))


Fig.savefig('EvaporationSketch.pgf', bbox_inches='tight',pad_inches=0.02)
latexplot('EvaporationSketch')

# plt.show()
# %%
