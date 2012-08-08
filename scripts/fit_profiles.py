import os
import glob

import pyfits
import numpy as np

arcperpix = 3. * 60.

bands = ['I1', 'I2', 'I3', 'I4', 'M1', 'S3', 'S4']

n_groups = 8

nx = 5
ny = 7


def rms(values):
    return np.mean(values ** 2)

variance = {}

for model in glob.glob('models/basic/images_total_*_conv.fits'):

    variance[model] = {}
    variance[model]['lon'] = {}
    variance[model]['lat'] = {}

    # Extract model name
    model_name = os.path.basename(model).replace('_conv.fits', '').replace('images_total_', '')

    # Define longitude scale
    l = np.linspace(65., -65., 130)
    b = np.linspace(-1., 1., 40)

    # Read in flux
    flux_lon = pyfits.getdata('models/basic/images_lon_%s_conv.fits' % model_name)[:, 0, :, :]
    flux_lat = pyfits.getdata('models/basic/images_lat_%s_conv.fits' % model_name)[:, :, 0, :]

    vl = []
    vb = []

    # Loop through the four IRAC bands
    for inu in range(len(bands)):

        # Read in data
        data_lon = np.loadtxt('images/profiles/profile_%s_lon.txt' % bands[inu])
        data_lat = np.loadtxt('images/profiles/profile_%s_lat.txt' % bands[inu])

        dl, dlf = data_lon[:, 0], data_lon[:, 1]
        db, dbf = data_lat[:, 0], data_lat[:, 1]

        flux_total = flux_lon.sum(axis=2)[inu, :]
        mlf = np.interp(dl, l[::-1], flux_total[::-1])

        flux_total = flux_lat.sum(axis=2)[inu, :]
        mbf = np.interp(db, b, flux_total)

        kl = (mlf > 0.) & (dlf > 0.)
        kb = (mbf > 0.) & (dbf > 0.)

        variance[model]['lon'][inu] = rms(np.log10(dlf[kl]) - np.log10(mlf[kl]))
        variance[model]['lat'][inu] = rms(np.log10(dbf[kb]) - np.log10(mbf[kb]))

means = {}
for model in ['original', 'updarm_gaussian', 'updarm_gaussian_hole', 'updarm_gaussian_hole_morepah']:
    full_model = 'models/basic/images_total_sky_' + model + '_conv.fits'
    means[full_model] = {}
    for direction in ['lon', 'lat']:
        means[full_model][direction] = []

for inu in range(len(bands)):
    line = []
    for model in ['original', 'updarm_gaussian', 'updarm_gaussian_hole', 'updarm_gaussian_hole_morepah']:
        full_model = 'models/basic/images_total_sky_' + model + '_conv.fits'
        for direction in ['lon', 'lat']:
            line.append("%6.4f" % variance[full_model][direction][inu])
            means[full_model][direction].append(variance[full_model][direction][inu])
    line = ' & '.join(line)
    print line

line = []
for model in ['original', 'updarm_gaussian', 'updarm_gaussian_hole', 'updarm_gaussian_hole_morepah']:
    full_model = 'models/basic/images_total_sky_' + model + '_conv.fits'
    for direction in ['lon', 'lat']:
        line.append("%6.4f" % np.mean(means[full_model][direction]))
line = ' & '.join(line)
print line
