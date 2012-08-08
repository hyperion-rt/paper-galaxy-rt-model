import os
import glob

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from plot_settings import set_plot_parameters
set_plot_parameters(mpl)

import pyfits
from groups import groups_short, light_group_colors, group_colors
from stacked_bar import make_percent_bar

labels = ['IRAC 3.6$\mu$m', 'IRAC 4.5$\mu$m', 'IRAC 5.8$\mu$m', 'IRAC 8.0$\mu$m', 'MIPS 24$\mu$m', 'IRAS 60$\mu$m', 'IRAS 100$\mu$m']

w, h = 7.1, 4.0

nw = 7

ns = len(labels)
xmin = 0.15 / w
xmax = 1. - 0.15 / w
ymin = 0.25 / h
ymax = 1. - 0.25 / h
ddy = 0.25 / h
dy = 0.3 / h


def make_plot(model):

    # Extract model name
    model_name = os.path.basename(model).replace('_conv.fits', '').replace('images_total_', '')

    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0., 0., 1., 1.])
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)
    flux = pyfits.getdata(model)[:, 0, 0, :]
    for iw in range(nw):
        ax.text(xmin, ymax - iw * dy - iw * ddy, labels[iw],
                va='bottom', ha='left', size=8, color='black')
        make_percent_bar(ax, flux[iw, :], groups_short,
                         [xmin, xmax,
                          ymax - (iw + 1) * dy - iw * ddy,
                          ymax - iw * dy - iw * ddy],
                          light_group_colors, group_colors)

    fig.savefig('plots/fractions_%s.eps' % model_name, bbox_inches='tight')
    fig.savefig('plots/fractions_%s.png' % model_name, bbox_inches='tight')

from multiprocessing import Pool
p = Pool()
p.map(make_plot, glob.glob('models/basic/images_total_*_conv.fits'))
