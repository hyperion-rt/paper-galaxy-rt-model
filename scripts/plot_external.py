import os
import glob

import aplpy
import Image

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from plot_settings import set_plot_parameters
set_plot_parameters(mpl)

if not os.path.exists('plots'):
    os.mkdir('plots')


def make_plot(model):

    # Extract model name
    model_name = os.path.basename(model).replace('_conv.fits', '').replace('external_', '')

    aplpy.make_rgb_image('models/external/external_%s_conv.fits' % model_name,
                         'models/external/external_%s.png' % model_name,
                         indices=[3, 1, 0],
                         vmax_r=4., stretch_r='sqrt',
                         vmax_g=3., stretch_g='sqrt',
                         vmax_b=3., stretch_b='sqrt')

    fig = plt.figure(figsize=(3.5, 3.5))
    ax = fig.add_axes([0.1, 0.1, 0.85, 0.85])
    ax.imshow(Image.open('models/external/external_%s.png' % model_name),
              extent=[-15, 15, -15, 15], origin='lower')

    for tick in ax.xaxis.get_ticklines():
        tick.set_color('white')

    for tick in ax.yaxis.get_ticklines():
        tick.set_color('white')

    for spine in ax.spines:
        ax.spines[spine].set_color('white')

    ax.set_xlabel('x [kpc]')
    ax.set_ylabel('y [kpc]')
    fig.savefig('plots/external_%s.png' % model_name, bbox_inches='tight')
    fig.savefig('plots/external_%s.eps' % model_name, bbox_inches='tight')

map(make_plot, glob.glob('models/external/external_*_conv.fits'))
