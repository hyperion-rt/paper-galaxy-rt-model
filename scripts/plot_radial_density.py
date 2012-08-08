import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from plot_settings import set_plot_parameters
set_plot_parameters(mpl)

dh = 3.5
dz = 0.1

a = 4.50
b = 1.00

t = b * b / dh + a
s = np.exp(-t / dh) / np.exp(-(t - a) ** 2 / 2. / b ** 2)

r = np.linspace(0., 15., 200)

inner = r < t
outer = r >= t

density_old = np.exp(-r / dh)

density_new = np.zeros(r.shape)
density_new[outer] = np.exp(-r[outer] / dh)
density_new[inner] = s * np.exp(-(r[inner] - a) ** 2 / 2. / b ** 2)

fig = plt.figure(figsize=(3.505, 2.5))
ax = fig.add_axes([0.15, 0.13, 0.8, 0.82])
ax.plot(r, density_old, color='gray')
ax.plot(r, density_new, color='black')
xlabel = fig.text(0.55, 0.015, "Galactocentric Radius (kpc)", ha='center', size=8)
ylabel = fig.text(0.02, 0.53, "Relative density", rotation=90., va='center', size=8)
ax.set_xlim(0., 15.)
fig.savefig('plots/radial_density_profile.eps')
fig.savefig('plots/radial_density_profile.png')
