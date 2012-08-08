import os
import glob

import numpy as np
import pyfits

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter

from groups import group_colors, light_group_colors
from plot_settings import set_plot_parameters
set_plot_parameters(mpl)

if not os.path.exists('plots'):
    os.mkdir('plots')

bands = ['I1', 'I2', 'I3', 'I4', 'M1', 'S3', 'S4']
filtwav = np.array([3.6, 4.5, 5.8, 8.0, 24., 60., 100.])

# Loop through the bands to find the average surface brightness
data = []
for inu in range(len(bands)):
    data.append(np.mean(np.loadtxt('images/profiles/profile_%s_lon.txt' % bands[inu], usecols=[1])))
data = np.array(data)


def make_plot(model):

    for style in ['fill', 'solid']:

        # Extract model name
        model_name = os.path.basename(model).replace('_conv.fits', '').replace('images_total_', '')

        fig = plt.figure(figsize=(3.505, 2.5))
        ax = fig.add_axes([0.15, 0.13, 0.8, 0.82])

        # ORIGINAL

        # Define wavelength scale
        wav = np.linspace(np.log10(3.0), np.log10(140.), 161)[::-1]
        wav = 10. ** ((wav[1:] + wav[:-1]) / 2.)

        # Read in flux
        flux = pyfits.getdata('models/basic/images_total_%s.fits' % model_name)[0, 0, :, :]

        flux_total = np.zeros(flux.shape[-1])

        for ig in range(9):
            flux_total += flux[ig, :]
            if style == 'fill':
                ax.fill_between(wav, flux_total, facecolor=light_group_colors[ig],
                                    edgecolor=group_colors[ig], zorder=-ig, y2=1.e-30)
            elif style == 'solid':
                if ig in [0, 2]:
                    ax.plot(wav[72:], flux[ig, 72:], color=group_colors[ig], zorder=-ig, markersize=0)
                else:
                    ax.plot(wav, flux[ig, :], color=group_colors[ig], zorder=-ig, markersize=0)

        if style == 'solid':
            ax.fill_between(wav, flux_total, facecolor='0.80',
                                edgecolor='0.25', zorder=-ig, y2=1.e-30)

        # CONVOLVED

        # Read in flux
        flux = pyfits.getdata('models/basic/images_total_%s_conv.fits' % model_name)[:, 0, 0, :]

        flux_total = np.zeros(flux.shape[0])

        for ig in range(9):
            flux_total += flux[:, ig]

        ax.scatter(filtwav, flux_total, s=15, facecolor='none',
                            edgecolor='black', zorder=100)

        ax.scatter(filtwav, data, s=6, facecolor='black',
                            edgecolor='black', zorder=101)

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlim(3.0, 140.)
        ax.set_ylim(0.05, 8000.)

        def format(x, i):
            if x >= 1.:
                return str(int(x))
            else:
                return str(x)

        ax.xaxis.set_major_formatter(FuncFormatter(format))
        ax.yaxis.set_major_formatter(FuncFormatter(format))

        fig.text(0.55, 0.015, r"Wavelength ($\mu$m)", ha='center', size=8)
        fig.text(0.02, 0.53, "Average Surface Brightness (MJy/sr)", rotation=90., va='center', size=8)

        fig.savefig('plots/spectrum_%s_%s.png' % (model_name, style))
        fig.savefig('plots/spectrum_%s_%s.eps' % (model_name, style))

        if model_name == 'sky_original' and style == 'solid':

            from matplotlib.lines import Line2D
            ax.text(9.0, 2.3, "Giants", size=7, color='k', ha='center', va='center')
            ax.text(62., 40., "VSGs", size=7, color='k', ha='left', va='center')
            ax.text(75., 1.5, "PAHs", size=7, color='k', ha='right', va='center')
            ax.text(42., 0.3, "Big Grains", size=7, color='k', ha='left', va='center')
            ax.text(30., 400., "Total", size=7, color='k', ha='right', va='center')
            ax.add_line(Line2D([8.5, 9.], [0.7, 1.6], color=(0., 0.5,  0.5), lw=0.5))
            ax.add_line(Line2D([29., 40.], [0.8, 0.38], color='yellow', lw=0.5))
            ax.add_line(Line2D([95., 76.], [3.8, 2.0], color='red', lw=0.5))
            ax.add_line(Line2D([50., 60.], [70., 50.], color='orange', lw=0.5))
            ax.add_line(Line2D([31., 42.], [340., 200.], color='k', lw=0.5))

            fig.savefig('plots/spectrum_%s_%s_annotated.png' % (model_name, style))
            fig.savefig('plots/spectrum_%s_%s_annotated.eps' % (model_name, style))

from multiprocessing import Pool
p = Pool()
p.map(make_plot, glob.glob('models/basic/images_total_*_conv.fits'))
