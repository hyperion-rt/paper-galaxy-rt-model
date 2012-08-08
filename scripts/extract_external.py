import os
import glob

import numpy as np

from hyperion.model import ModelOutput

import pyfits

from hyperion.util.constants import c, kpc
from hyperion.util.integrate import integrate_subset


def rebin_filter(filtname, nu):

    # Read in filter
    trans = np.loadtxt('filters/%s.txt' % filtname)
    fwav, fval = trans[:, 0], trans[:, 1]
    fnu = c / (fwav * 1.e-4)

    fnu = np.hstack([0., fnu, np.inf])
    fval = np.hstack([0., fval, 0.])

    # Initialize new filter
    fval_new = np.zeros(nu.shape)

    nu_min = nu[0]
    nu_max = 0.5 * (nu[1] + nu[0])

    fval_new[0] = integrate_subset(fnu, fval, nu_min, nu_max)

    for j in range(1, len(nu) - 1):

        nu_min = 0.5 * (nu[j] + nu[j - 1])
        nu_max = 0.5 * (nu[j] + nu[j + 1])

        fval_new[j] = integrate_subset(fnu, fval, nu_min, nu_max)

    nu_min = 0.5 * (nu[-2] + nu[-1])
    nu_max = nu[-1]

    fval_new[-1] = integrate_subset(fnu, fval, nu_min, nu_max)

    return fval_new

n_sources = 87
n_dust = 3

n_wav = 160

n_groups = 9

filters = ['I1', 'I2', 'I3', 'I4', 'M1', 'S3', 'S4']


def extract(model):

    # Extract model name
    model_name = os.path.basename(model).replace('.rtout', '').replace('external_', '')

    m = ModelOutput(model)

    wav, flux = m.get_image(group=0, units='MJy/sr', distance=1000. * kpc)  # distance should not matter as long as it is large
    flux = flux[0, :, :, :]

    # Convolve with filters
    flux_conv = np.zeros((len(filters), flux.shape[0], flux.shape[1]))
    for i, filtname in enumerate(filters):
        transmission = rebin_filter(filtname, c / (wav * 1.e-4))
        flux_conv[i, :, :] = np.sum(transmission[np.newaxis, np.newaxis:] * flux, axis=2)

    pyfits.writeto('models/external/external_%s.fits' % model_name, flux, clobber=True)
    pyfits.writeto('models/external/external_%s_conv.fits' % model_name, flux_conv, clobber=True)

from multiprocessing import Pool
p = Pool()
p.map(extract, glob.glob('models/external/external_*.rtout'))
