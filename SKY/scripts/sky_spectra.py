import os

import atpy
import numpy as np

from hyperion.util.constants import G, msun, rsun, pi, pc
from hyperion.util.interpolate import interp1d_fast_loglog

from extract_kurucz import extract_kurucz

# Set list of filters
filt_name = ['B', 'V', 'J', 'H', 'K', '12', '25']

# Set wavelengths in microns
filt_wav = np.array([0.44, 0.55, 1.235, 1.662, 2.159, 12., 25.])

# Set zero-magnitude fluxes in Jy
# The IRAS values are from M. Cohen - IR Calibration Paper I
filt_zero = np.array([4130., 3781., 1594., 1024., 666.7, 26.966, 6.288])

# Read in SKY model parameters
t = atpy.Table('tables/table2.tbl')

# Create output table set
t_out = atpy.TableSet()

# Create table of default fluxes to use if spectra are not available
t_default = atpy.Table(name='Default Fluxes')

t_default.add_column('Type', t['Type'])

for iwav in range(len(filt_name)):

    # Convert magnitudes to fluxes in Jy
    fluxes = filt_zero[iwav] * 10. ** (-0.4 * t['M_' + filt_name[iwav]])

    # Convert fluxes in Jy to fluxes in ergs/s/Hz
    fluxes *= 1.e-23 * (4. * pi * (10. * pc) ** 2)

    # Add to table
    t_default.add_column(filt_name[iwav], fluxes, unit='ergs/s/Hz')

# Append to output table set
t_out.append(t_default)

# Read in stellar parameters for various SKY spectral types
ts = atpy.Table('tables/stellar.tbl')

# Compute surface gravity
logg = np.log10(G * ts['Mass'] * msun / (ts['Radius'] * rsun) ** 2)

# Set Kurucz values
kurucz_teff = np.hstack([np.linspace(3500, 13000, 39),
                         np.linspace(14000, 50000, 37)])
kurucz_logg = np.linspace(0., 5., 11)

# Loop over spectral types
for ispec in range(len(ts)):

    # Find closest values in Kurucz grid
    ig = np.argmin(np.abs(logg[ispec] - kurucz_logg))
    it = np.argmin(np.abs(ts['Temperature'][ispec] - kurucz_teff))

    # Extract the photosphere model
    t_spec = extract_kurucz(kurucz_teff[it], kurucz_logg[ig])

    if t_spec is not None:

        # Set table name
        t_spec.table_name = ts['Type'][ispec]

        # Find scaling of spectrum to be consistent with default fluxes
        model_fluxes = interp1d_fast_loglog(t_spec['wav'], t_spec['fnu'], filt_wav)
        default_fluxes = np.array([t_default[band][ispec] for band in filt_name])
        scale = np.median(default_fluxes / model_fluxes)

        # Scale the spectra
        t_spec['fnu'] *= scale

        t_out.append(t_spec)

# Create directory if needed
if not os.path.exists('models'):
    os.mkdir('models')

# Write out to file
t_out.write('models/sky_model_spectra.fits', overwrite=True)
