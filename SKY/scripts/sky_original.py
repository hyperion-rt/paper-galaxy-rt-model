import os

import numpy as np
import atpy
import pyfits

from hyperion.util.meshgrid import meshgrid_nd

# Set global parameters
R_max = 15.0  # kpc (outer radius)
z_max = 3.0  # kpc (max scaleheight for grid)
R_0 = 8.5  # kpc (solar radius)
h = 3.5  # kpc (scale-length)
R_r = 0.45 * R_0  # (ring radius)
sigma_r = 0.064 * R_0  # (ring width)

# Set cylindrical grid parameters
n_r = 200
n_z = 50
n_p = 100

# Set up grid walls
r_w = np.linspace(0., R_max, n_r + 1)

zhalf = np.logspace(-3., np.log10(z_max), n_z / 2)
z_w = np.hstack([-zhalf[::-1], 0, zhalf])

p_w = np.linspace(0., 2. * np.pi, n_p + 1)

# Find position of center of cells
R = 0.5 * (r_w[1:] + r_w[:-1])
z = 0.5 * (z_w[1:] + z_w[:-1])
p = 0.5 * (p_w[1:] + p_w[:-1])

# Calculate volumes
dr2 = r_w[1:] ** 2 - r_w[:-1] ** 2
dz = z_w[1:] - z_w[:-1]
dp = p_w[1:] - p_w[:-1]
volumes = dr2[np.newaxis, np.newaxis, :] \
          * dz[np.newaxis, :, np.newaxis] \
          * dp[:, np.newaxis, np.newaxis] / 2.

# Create 3D grid of coordinates
R, z, p = meshgrid_nd(R, z, p)

# Load up information about spectral types
t = atpy.Table('tables/table2.tbl')

# Find number of spectral types
n_spec = len(t)

# Load up information about arms
t_arm = atpy.Table('tables/arms.tbl')

# Find number of arms
n_arm = len(t_arm)

# Pre-compute density scalings

rho_0 = 10. ** t['lrho0']

rho_d = rho_0 * t['disk']

g_a = 5
rho_a = rho_0 * t['arm'] * g_a

g_r = 25
rho_r = rho_0 * t['ring'] * g_r

g_b = 3.6
rho_b = rho_0 * t['bulge'] * g_b

g_h = 0.0008  # Changed in Cohen (1995)
rho_h = rho_0 * t['halo'] * g_h

# Convert scale-height to kpc
t.hz = t.hz / 1000.

densities = []

# Loop through spectral types
for ispec in range(n_spec):

    print "Processing %s..." % t['Type'][ispec]

    # Initialize density
    rho = np.zeros((n_p, n_z, n_r))

    # Exponential disk
    rho += rho_d[ispec] \
           * np.exp(-(R - R_0) / h) \
           * np.exp(-np.abs(z) / t['hz'][ispec])

    # Bulge
    k1 = 1.6
    R1 = 2.0  # kpc
    x = np.sqrt(R * R + k1 * k1 * z * z) / R1
    rho += rho_b[ispec] * x ** -1.8 * np.exp(-x * x * x)

    # Halo
    rho += rho_h[ispec] * np.sqrt(np.sqrt(R / R_0))

    # Spiral Arms

    for iarm in range(n_arm):

        dphi = np.mod(p - t_arm['phi_min'][iarm], 2. * np.pi)

        R_arm = np.exp(dphi / t_arm['a'][iarm]) \
                * t_arm['R_min'][iarm]

        R_arm_max = np.exp(t_arm['extent'][iarm] / t_arm['a'][iarm]) \
                    * t_arm['R_min'][iarm]

        in_arm = (R < R_arm + t_arm['width'][iarm] / 2.) \
                 & (R > R_arm - t_arm['width'][iarm] / 2.) \
                 & (R < R_arm_max) & (R > t_arm['R_min'][iarm])

        rho[in_arm] += rho_a[ispec] \
                       * np.exp(-(R[in_arm] - R_0) / h) \
                       * np.exp(-np.abs(z[in_arm]) / t['hz'][ispec])

    # Molecular Ring
    rho += rho_r[ispec] \
           * np.exp(-(R - R_r) ** 2 / (2. * sigma_r ** 2)) \
           * np.exp(-np.abs(z) / t['hz'][ispec])

    densities.append(rho)

densities = np.vstack(densities).reshape((n_spec, n_p, n_z, n_r))

# Create directory if needed
if not os.path.exists('models'):
    os.mkdir('models')

# Write out to file
hdu1 = pyfits.PrimaryHDU(densities * volumes)
hdu2 = pyfits.ImageHDU(r_w)
hdu3 = pyfits.ImageHDU(z_w)
hdu4 = pyfits.ImageHDU(p_w)
hdulist = pyfits.HDUList([hdu1, hdu2, hdu3, hdu4])
hdulist.writeto('models/sky_model_original.fits', clobber=True)
