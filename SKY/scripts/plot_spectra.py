import os

import atpy

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

# Set list of filters
filt_name = ['B', 'V', 'J', 'H', 'K', '12', '25']

# Set wavelengths in microns
filt_wav = np.array([0.44, 0.55, 1.235, 1.662, 2.159, 12., 25.])

ts = atpy.TableSet('models/sky_model_spectra.fits')

t_default = ts['DEFAULT FLUXES']

fig = plt.figure(figsize=(15, 15))

for ispec in range(len(t_default)):

    spec_type = t_default['Type'][ispec].strip().upper()

    ax = fig.add_subplot(10, 10, ispec + 1)

    default_fluxes = np.array([t_default[band][ispec] for band in filt_name])
    ax.scatter(filt_wav, default_fluxes)

    maxflux = np.max(default_fluxes)

    ax.text(0.5, 1.02, spec_type, transform=ax.transAxes,
            size='xx-small', ha='center')

    if spec_type in ts.tables:
        ax.plot(ts[spec_type].wav, ts[spec_type].fnu, color='green')

    ax.set_xscale('log')
    ax.set_yscale('log')

    for tick in ax.get_xticklabels():
        tick.set_visible(False)
    for tick in ax.get_yticklabels():
        tick.set_visible(False)

    ax.set_xlim(0.1, 50.)
    ax.set_ylim(maxflux / 1e5, maxflux * 10.)

if not os.path.exists('plots'):
    os.mkdir('plots')

fig.savefig('plots/thumbnails.png')
