import numpy as np
np.seterr(all='ignore')
import pyfits
import atpy

from hyperion.util.constants import c, kpc
from hyperion.util.integrate import integrate_loglog

# Set list of filters
filt_name = ['B', 'V', 'J', 'H', 'K', '12', '25']

# Set wavelengths in microns
filt_wav = np.array([0.44, 0.55, 1.235, 1.662, 2.159, 12., 25.])

# Read in spectral information
ts = atpy.TableSet('SKY/models/sky_model_spectra.fits', verbose=False)

# Extract default table
t_default = ts['DEFAULT FLUXES']

# Find number of spectral types
n_spec = len(t_default)

# Compile list of spectral types
spectral_types = [t_default['Type'][ispec].strip().upper() for ispec in range(n_spec)]

sky_loaded = {}


def setup_sources(model, model_name, sky_model, spectral_type=None):

    global sky_loaded

    # Read in SKY model maps
    if sky_model in sky_loaded:
        print "[%s] Reading %s (cached)" % (model_name, sky_model)
        hdulist = sky_loaded[sky_model]
    else:
        print "[%s] Reading %s" % (model_name, sky_model)
        hdulist = pyfits.open(sky_model)
        sky_loaded[sky_model] = hdulist

    # Set cylindrical grid parameters
    r_wall = hdulist[1].data * kpc
    z_wall = hdulist[2].data * kpc
    p_wall = hdulist[3].data
    model.set_cylindrical_polar_grid(r_wall, z_wall, p_wall)

    # Loop through spectral types
    for ispec in range(n_spec):

        if spectral_type is not None and t_default['Type'][ispec].strip().upper() != spectral_type:
            continue
        else:
            spec_type = t_default['Type'][ispec].strip().upper()

        # Check if full spectrum exists
        if spec_type in ts.tables:
            nu = ts[spec_type]['nu']
            fnu = ts[spec_type]['fnu']
        else:
            nu = c / (filt_wav * 1.e-4)
            fnu = np.array([t_default[band][ispec] for band in filt_name])

        # Sort spectrum
        order = np.argsort(nu)
        nu, fnu = nu[order], fnu[order]

        # Find total luminosity of single object
        l_single = integrate_loglog(nu, fnu)

        # Find number of sources in each cell
        number = hdulist[0].data[ispec, :, :, :]

        # Set up source
        source = model.add_map_source()
        source.luminosity = np.sum(number) * l_single
        source.spectrum = (nu.astype(np.float64), fnu.astype(np.float64))
        source.map = number

    return model
