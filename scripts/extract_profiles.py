import os
import glob

import numpy as np
import atpy
import pyfits

from hyperion.model import ModelOutput
from hyperion.util.constants import c
from hyperion.util.integrate import integrate_subset

from groups import group


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

# Read in spectral information
ts = atpy.TableSet('SKY/models/sky_model_spectra.fits')

# Extract default table
t_default = ts['DEFAULT FLUXES']


def extract(model):

    # Check that file is valid
    if not os.path.basename(model).startswith('basic_') or not os.path.basename(model).endswith('.rtout'):
        raise Exception("Only basic_*.rtout files should be specified")

    # Extract model name
    model_name = os.path.basename(model).replace('.rtout', '').replace('basic_', '')

    m = ModelOutput('models/basic/basic_%s.rtout' % model_name)

    for image_set in range(3):

        if image_set == 0:

            n_x = 1
            n_y = 1
            image_set_name = 'total'

        elif image_set == 1:

            n_x = 130
            n_y = 1
            image_set_name = 'lon'

        elif image_set == 2:

            n_x = 1
            n_y = 40
            image_set_name = 'lat'

        flux = np.zeros((n_y, n_x, n_groups, n_wav))

        print "Direct source emission"

        try:
            wav, nufnu_all = m.get_image(group=image_set, component='source_emit', units='MJy/sr', source_id='all')
        except IOError:
            return

        for source_id in range(n_sources):

            nufnu = nufnu_all[source_id, 0, :, :, :]
            spec_type = t_default['Type'][source_id].strip().upper()
            group_id = group(spec_type)
            flux[:, :, group_id, :] += nufnu

        print "Direct dust emission"

        wav, nufnu_all = m.get_image(group=image_set, component='dust_emit', units='MJy/sr', dust_id='all')

        for dust_id in range(n_dust):

            nufnu = nufnu_all[dust_id, 0, :, :, :]
            flux[:, :, 5 + dust_id, :] += nufnu

        print "Scattered source emission"

        wav, nufnu = m.get_image(group=image_set, component='source_scat', units='MJy/sr')
        nufnu = nufnu[0, :, :, :]
        flux[:, :, 8, :] += nufnu

        print "Scattered dust emission"

        wav, nufnu = m.get_image(group=image_set, component='dust_scat', units='MJy/sr')
        nufnu = nufnu[0, :, :, :]
        flux[:, :, 8, :] += nufnu

        # Convolve with filters
        flux_conv = np.zeros((len(filters), n_y, n_x, n_groups))
        for i, filtname in enumerate(filters):
            transmission = rebin_filter(filtname, c / (wav * 1.e-4))
            flux_conv[i, :, :, :] = np.sum(transmission[np.newaxis, np.newaxis, np.newaxis, :] * flux, axis=3)

        pyfits.writeto('models/basic/images_%s_%s.fits' % (image_set_name, model_name), flux, clobber=True)
        pyfits.writeto('models/basic/images_%s_%s_conv.fits' % (image_set_name, model_name), flux_conv, clobber=True)

from multiprocessing import Pool
p = Pool()
p.map(extract, glob.glob('models/basic/basic_*.rtout'))
