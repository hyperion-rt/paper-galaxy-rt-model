import os

from hyperion.model import Model

from models import sky_model
from sources import setup_sources, spectral_types
from dust import setup_dust

if not os.path.exists('models'):
    os.mkdir('models')

if not os.path.exists('models/indiv'):
    os.mkdir('models/indiv')

seed = -69102

for model_name in ['sky_updarm_gaussian_hole_morepah']:

    for spectral_type in spectral_types:

        print "Processing %s..." % spectral_type

        m = Model('models/indiv/energy_%s_%s' % (model_name, spectral_type.replace(' ', '_')))

        seed += 1
        m.set_seed(seed)

        m = setup_sources(m, model_name, sky_model[model_name][0], spectral_type=spectral_type)
        m = setup_dust(m, **sky_model[model_name][1])

        m.set_n_initial_iterations(3)
        m.set_n_photons(initial=100000000, imaging=0)

        m.set_enforce_energy_range(False)

        m.write()
