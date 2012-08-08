
import pyfits
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from plot_settings import set_plot_parameters
set_plot_parameters(mpl)

from hyperion.util.interpolate import interp1d_fast

from matplotlib.ticker import FuncFormatter

arcperpix = 3. * 60.

bands = ['I1', 'I2', 'I3', 'I4']
labels = [r'IRAC 3.6$\mu$m', r'IRAC 4.5$\mu$m', r'IRAC 5.8$\mu$m', r'IRAC 8.0$\mu$m']

n_groups = 8

nx = 5
ny = 4

xmin = 0.09
xmax = 0.98
ymin = 0.05
ymax = 0.99
ddx = 0.012
ddy = 0.015

dx = (xmax - xmin - ddx * (nx - 1)) / float(nx)
dy = (ymax - ymin - ddy * (ny - 1)) / float(ny)

for model_name in ['sky_updarm_gaussian_hole_morepah']:

    # Define longitude scale
    l = np.linspace(65., -65., 130)

    # Read in flux
    flux_lon = pyfits.getdata('models/basic/images_lon_%s_conv.fits' % model_name)[:, 0, :, :]

    # Open figure
    fig = plt.figure(figsize=(7.1, 5.0))

    # Loop through the four IRAC bands
    for inu in range(4):

        # Read in data
        data_lon = np.loadtxt('catalogs/profiles/profile_%s_lon.txt' % bands[inu])
        data_lon = data_lon[::-1, :]

        # LONGITUDE
        ax = fig.add_axes([xmin, ymax - dy * (inu + 1) - ddy * inu, dx * (nx - 1) + ddx * (nx - 2), dy])

        # Initialize empty cumulative flux container
        flux_total = np.zeros(l.shape)

        # Loop through groups and plot cumulative flux
        for ig in range(5):
            flux_total += flux_lon[inu, :, ig]

        flux_total = interp1d_fast(l[::-1], flux_total[::-1], data_lon[:, 0], bounds_error=False, fill_value=0.)

        ax.axhline(1., ls='dashed', color='black')
        ax.plot(data_lon[:, 0], data_lon[:, 1] / flux_total, 'o', color='black', markersize=2, zorder=1)

        # Set view limits
        ax.set_ylim(0., 1.55)
        ax.set_xlim(65., -65.)
        ax.text(0.015, 0.93, labels[inu], ha='left', va='top', transform=ax.transAxes, size=8)

        # Turn off x tick labels
        if inu < len(bands) - 1:
            for label in ax.xaxis.get_ticklabels():
                label.set_visible(False)

    # Add labels
    xlabel1 = fig.text(xmin + (dx * (nx - 1) + ddx * (nx - 2)) / 2., 0.00, "Galactic Longitude (deg)", ha='center', size=8)
    ylabel = fig.text(0.02, 0.5, "Archive flux / Model stellar flux", rotation=90., va='center', size=8)

    # Save plot
    fig.savefig('plots/unresolved_ratio_%s.png' % model_name, bbox_inches='tight', bbox_extra_artists=[xlabel1, ylabel])
    fig.savefig('plots/unresolved_ratio_%s.eps' % model_name, bbox_inches='tight', bbox_extra_artists=[xlabel1, ylabel])

    # Open figure
    fig = plt.figure(figsize=(7.1, 5.0))

    # Loop through the four IRAC bands
    for inu in range(4):

        # Read in data
        data_lon = np.loadtxt('catalogs/profiles/profile_%s_lon.txt' % bands[inu])

        # LONGITUDE
        ax = fig.add_axes([xmin, ymax - dy * (inu + 1) - ddy * inu, dx * (nx - 1) + ddx * (nx - 2), dy])
        ax.plot(data_lon[:, 0], data_lon[:, 1], 'o', color='black', markersize=2, zorder=1)

        # Initialize empty cumulative flux container
        flux_total = np.zeros(l.shape)

        # Loop through groups and plot cumulative flux
        for ig in range(5):
            flux_total += flux_lon[inu, :, ig]

        ax.fill_between(l, flux_total, facecolor='0.80',
                        edgecolor='0.25', zorder=-ig, y2=1.e-30)

        # Set view limits
        ax.set_xlim(65., -65.)

        m = np.median(data_lon[:, 1])
        ax.set_ylim(m / 10., m * 10.)
        ax.set_yscale('log')

        ax.text(0.015, 0.93, labels[inu], ha='left', va='top', transform=ax.transAxes, size=8)

        # Turn off x tick labels
        if inu < len(bands) - 1:
            for label in ax.xaxis.get_ticklabels():
                label.set_visible(False)

        # Change ticks to non exponential format
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, y: str(int(x))))

    # Add labels
    xlabel1 = fig.text(xmin + (dx * (nx - 1) + ddx * (nx - 2)) / 2., 0.015, "Galactic Longitude (deg)", ha='center', size=8)
    ylabel = fig.text(0.02, 0.5, "Average Surface Brightness (MJy/sr)", rotation=90., va='center', size=8)

    # Save plot
    fig.savefig('plots/unresolved_%s.png' % model_name, bbox_inches='tight', bbox_extra_artists=[xlabel1, ylabel])
    fig.savefig('plots/unresolved_%s.eps' % model_name, bbox_inches='tight', bbox_extra_artists=[xlabel1, ylabel])
