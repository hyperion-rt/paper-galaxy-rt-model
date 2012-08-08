import os
import glob

import pyfits
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter

from groups import group_colors, light_group_colors

from plot_settings import set_plot_parameters
set_plot_parameters(mpl)

if not os.path.exists('plots'):
    os.mkdir('plots')

arcperpix = 3. * 60.

bands = ['I1', 'I2', 'I3', 'I4', 'M1', 'S3', 'S4']
labels = [r'IRAC 3.6$\mu$m', r'IRAC 4.5$\mu$m', r'IRAC 5.8$\mu$m', r'IRAC 8.0$\mu$m', r'MIPS 24$\mu$m', r'IRAS 60$\mu$m', r'IRAS 100$\mu$m']

n_groups = 8

nx = 5
ny = 7

xmin = 0.09
xmax = 0.98
ymin = 0.05
ymax = 0.99
ddx = 0.012
ddy = 0.008

dx = (xmax - xmin - ddx * (nx - 1)) / float(nx)
dy = (ymax - ymin - ddy * (ny - 1)) / float(ny)


def make_plot(model):

    for style in ['fill', 'solid']:

        # Extract model name
        model_name = os.path.basename(model).replace('_conv.fits', '').replace('images_total_', '')

        # Define longitude scale
        l = np.linspace(65., -65., 130)
        b = np.linspace(-1., 1., 40)

        # Read in flux
        flux_lon = pyfits.getdata('models/basic/images_lon_%s_conv.fits' % model_name)[:, 0, :, :]
        flux_lat = pyfits.getdata('models/basic/images_lat_%s_conv.fits' % model_name)[:, :, 0, :]

        # Open figure
        fig = plt.figure(figsize=(7.1, 9.2))

        # Loop through the four IRAC bands
        for inu in range(len(bands)):

            # Read in data
            data_lon = np.loadtxt('images/profiles/profile_%s_lon.txt' % bands[inu])
            data_lat = np.loadtxt('images/profiles/profile_%s_lat.txt' % bands[inu])

            # LONGITUDE
            ax = fig.add_axes([xmin, ymax - dy * (inu + 1) - ddy * inu, dx * (nx - 1) + ddx * (nx - 2), dy])
            ax.plot(data_lon[:, 0], data_lon[:, 1], color='black',
                    markersize=0, zorder=1)

            # Spiral arm tangencies
            if inu == 0:
                ax.plot([-58., -58, -47, -47.], [9., 10., 10., 9.], lw=1, color='black')
                ax.text(-52.5, 12, 'Centaurus', ha='center', size='xx-small')
                ax.plot([-35., -35, -28, -28.], [16.2, 18., 18., 16.2], lw=1, color='black')
                ax.text(-31.5, 21.6, 'Norma', ha='center', size='xx-small')
                ax.plot([24., 24., 32., 32.], [18., 20., 20., 18.], lw=1, color='black')
                ax.text(28., 24, 'Scutum', ha='center', size='xx-small')
                ax.plot([46., 46., 50.5, 50.5], [8.1, 9., 9., 8.1], lw=1, color='black')
                ax.text(48.25, 10.8, 'Sagittarius', ha='center', size='xx-small')

            # Initialize empty cumulative flux container
            flux_total = np.zeros(l.shape)

            # Loop through groups and plot cumulative flux
            for ig in range(n_groups):
                flux_total += flux_lon[inu, :, ig]
                if style == 'fill':
                    ax.fill_between(l, flux_total, facecolor=light_group_colors[ig],
                                    edgecolor=group_colors[ig], zorder=-ig, y2=1.e-30)
                elif style == 'solid':
                    ax.plot(l, flux_lon[inu, :, ig], color=group_colors[ig], zorder=-ig, markersize=0)

            if style == 'solid':
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

            # LATITUDE
            ax = fig.add_axes([xmin + dx * (nx - 1) + ddx * (nx - 1), ymax - dy * (inu + 1) - ddy * inu, dx, dy])
            ax.plot(data_lat[:, 0], data_lat[:, 1], color='black',
                    markersize=0, zorder=1)

            # Initialize empty cumulative flux container
            flux_total = np.zeros(b.shape)

            # Loop through groups and plot cumulative flux
            for ig in range(n_groups):
                flux_total += flux_lat[inu, :, ig]
                if style == 'fill':
                    ax.fill_between(b, flux_total, facecolor=light_group_colors[ig],
                                    edgecolor=group_colors[ig], zorder=-ig, y2=1.e-30)
                elif style == 'solid':
                    ax.plot(b, flux_lat[inu, :, ig], color=group_colors[ig], zorder=-ig, markersize=0)

            if style == 'solid':
                ax.fill_between(b, flux_total, facecolor='0.80',
                                edgecolor='0.25', zorder=-ig, y2=1.e-30)

            # Set view limits
            ax.set_xlim(-1., 1.)

            ax.set_ylim(m / 10., m * 10.)
            ax.set_yscale('log')

            # Turn off x tick labels
            if inu < len(bands) - 1:
                for label in ax.xaxis.get_ticklabels():
                    label.set_visible(False)

            # Turn off y tick labels
            for label in ax.yaxis.get_ticklabels():
                label.set_visible(False)

        # Add labels
        xlabel1 = fig.text(xmin + (dx * (nx - 1) + ddx * (nx - 2)) / 2., 0.015, "Galactic Longitude (deg)", ha='center', size=8)
        xlabel2 = fig.text(xmin + (dx * (nx - 1) + ddx * (nx - 1)) + dx / 2., 0.015, "Galactic Latitude (deg)", ha='center', size=8)
        ylabel = fig.text(0.02, 0.5, "Average Surface Brightness (MJy/sr)", rotation=90., va='center', size=8)

        # Save plot
        fig.savefig('plots/profiles_%s_%s.png' % (model_name, style), bbox_inches='tight', bbox_extra_artists=[xlabel1, xlabel2, ylabel])
        fig.savefig('plots/profiles_%s_%s.eps' % (model_name, style), bbox_inches='tight', bbox_extra_artists=[xlabel1, xlabel2, ylabel])

from multiprocessing import Pool
p = Pool()
p.map(make_plot, glob.glob('models/basic/images_total_*_conv.fits'))
