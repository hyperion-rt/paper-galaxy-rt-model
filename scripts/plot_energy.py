import os
import glob

import h5py
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from plot_settings import set_plot_parameters
set_plot_parameters(mpl)

from groups import group, group_colors, light_group_colors
from stacked_bar import make_percent_bar

if not os.path.exists('plots'):
    os.mkdir('plots')

normalization = [1226.5418655729284, 328.27406203159899, 229.92279880210157]
labels = ["PAHs", "VSGs", "Big grains"]

w, h = 7.1, 1.8

ns = len(labels)
xmin = 0.15 / w
xmax = 1. - 0.15 / w
ymin = 0.25 / h
ymax = 1. - 0.25 / h
ddy = 0.25 / h
dy = 0.3 / h

fig = plt.figure(figsize=(w, h))
ax = fig.add_axes([0., 0., 1., 1.])
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
for spine in ax.spines:
    ax.spines[spine].set_visible(False)

for model_name in ['sky_updarm_gaussian_hole_morepah']:

    for isize in range(ns):

        # Initialize model names and total energies deposited
        names = []
        energies = []

        energy_all = None

        # Loop through models and find total energy deposited in PAH grains for each
        for model in glob.glob(os.path.join('models/indiv/', 'energy_%s_*.rtout' % model_name)):

            print model

            # Open output file and extract specific energy absorbed
            try:
                f = h5py.File(model, 'r')
                energy = f['iteration_%05i' % (len(f) - 1)]['specific_energy']
            except IOError:
                break

            # Extract PAH energy
            energy = energy[isize, :, :, :]

            # Append to lists
            energies.append(np.mean(energy) / normalization[isize])
            names.append(os.path.basename(model).replace('.rtout', '').replace('energy_%s_' % model_name, '').replace('_', ' ').strip())

        # Create list of group numbers
        groups = [group(name) for name in names]

        # Convert to Numpy arrays and sort
        energies, names, groups = np.array(energies), np.array(names), np.array(groups)
        key = np.array(zip(groups, energies), dtype=[('groups', int), ('energies', float)])
        order = np.argsort(key, order=['groups', 'energies'])
        energies, names, groups = energies[order], names[order], groups[order]

        # Create pie chart figure
        print len(energies)

        ax.text(xmin, ymax - isize * dy - isize * ddy + 0.02 / h, labels[isize],
            va='bottom', ha='left', size=8, color='black')

        make_percent_bar(ax, energies, names,
                     [xmin, xmax,
                      ymax - (isize + 1) * dy - isize * ddy,
                      ymax - isize * dy - isize * ddy],
                      [light_group_colors[g] for g in groups], [group_colors[g] for g in groups])

    fig.savefig('plots/energy_fractions_%s.eps' % model_name)
    fig.savefig('plots/energy_fractions_%s.png' % model_name)
