import numpy as np
from matplotlib.patches import Rectangle


def make_percent_bar(ax, data, labels, extent, facecolor, edgecolor):

    data = np.array(data)
    data /= np.sum(data)

    xmin, xmax, ymin, ymax = extent
    dx = xmax - xmin
    dy = ymax - ymin

    x = xmin
    for i, frac in enumerate(data):
        ax.add_patch(Rectangle((x, ymin), dx * frac, dy, facecolor=facecolor[i], edgecolor=edgecolor[i]))

        if frac > 0.07:
            ax.text(x + dx * frac / 2., ymin + dy * 2. / 3., "%s" % labels[i], color='0.25', ha='center', va='center', size=7)
            ax.text(x + dx * frac / 2., ymin + dy * 1. / 3., "%i%s" % (int(round(frac * 100., 0)), '%'), color='0.25', ha='center', va='center', size=6)

        x += frac * dx

    print data.sum()
