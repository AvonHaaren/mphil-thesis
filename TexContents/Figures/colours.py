import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path
import cmocean as cmo
import matplotlib.cm as mplcm


f = Path().home() / "Google Drive/Studium/Cambridge/thesis/TexContents/Figures"
with open(f / "colours.json", "r+") as file:
    j = json.load(file)
    src = j["cmap_src"]
    name = j["cmap"]
    if src == "mpl":
        cmap = mplcm.get_cmap(name)
    elif src == "cmocean":
        cmap = cmo.cm.cmap_d[name]

    print(cmap)

    cr = j["crange"]
    clist = [cr[1], cr[0], (cr[0] + cr[1]) / 2, 1, 1]
    clist[4] = (clist[1] + clist[2]) / 2
    clist[3] = (clist[0] + clist[2]) / 2

    j["crgb_list"] = [cmap(i) for i in clist]
    clist = j["crgb_list"]
    file.seek(0)
    json.dump(j, file, indent=4)
    file.truncate()


tikz_paths = [f / "DMD/PointSorting", f / "DMD/Sketch", f /
              "DMD/FloydSteinberg", f / "Evap/DSMCFlowchart", f]


def definecolor_str(index, r, g, b):
    first = '\\definecolor{progression' + str(index) + '}{rgb}{%\n'

    def line(x): return "    {:f}".format(x)

    return first + line(r) + ',%\n' + line(g) + ',%\n' + line(b) + '%\n}\n'


tex_text = "\\usepackage{xcolor}\n"
for i, color in enumerate(clist):
    tex_text = tex_text + definecolor_str(i, color[0], color[1], color[2])

for path in tikz_paths:
    with open(path / "colours.tex", "w") as cfile:
        cfile.write(tex_text)


# x = np.arange(1024)
# y = np.arange(768)
# X, Y = np.meshgrid(x, y)
# z = np.abs((X - 512)**2 - (Y - 384)**2)


# plt.imshow(z, cmap=cmap)
# plt.colorbar()
# plt.show()


x = np.arange(100)
y1 = x**2
y2 = x * 100
y3 = 10000 / (x + 1)
y4 = np.exp(x / 11)
y5 = np.log(x) * 920


for i, n in enumerate([y1, y2, y3, y4, y5][:5]):
    plt.plot(x, n, c=clist[i], lw=3, label=str(i))


plt.legend()
plt.show()
