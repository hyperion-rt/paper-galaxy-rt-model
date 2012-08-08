import numpy as np
np.seterr(all='ignore')

from hyperion.util.constants import kpc


def setup_dust(model, hole=None, pah_factor=None):

    rho_0 = 1.e-25  # g/cm^3
    dh = 3.5 * kpc
    dz = 0.1 * kpc

    if hole is not None:

        print "Carving out hole"

        # Extract hole parameters
        a, b = hole[0] * kpc, hole[1] * kpc

        # Find transition radius and scale for gaussian
        t = b * b / dh + a
        s = np.exp(-t / dh) / np.exp(-(t - a) ** 2 / 2. / b ** 2)

        inner = model.grid.gw < t
        outer = ~inner

        density = np.zeros(model.grid.shape)
        density[outer] = rho_0 * np.exp(-model.grid.gw[outer] / dh) \
                       * np.exp(- np.abs(model.grid.gz[outer]) / dz)
        density[inner] = rho_0 * s \
                       * np.exp(-(model.grid.gw[inner] - a) ** 2 / 2. / b ** 2) \
                       * np.exp(- np.abs(model.grid.gz[inner]) / dz)

    else:

        density = rho_0 * np.exp(- model.grid.gw / dh) \
                * np.exp(- np.abs(model.grid.gz) / dz)

    frac = {'usg': 0.0586, 'vsg': 0.1351, 'big': 0.8063}
    if pah_factor is not None:
        frac['usg'] *= pah_factor
    for size in ['usg', 'vsg', 'big']:
        model.add_density_grid(density * frac[size], 'dust/%s.hdf5' % size)

    return model
