import os

import matplotlib
matplotlib.use('Agg')

from hyperion.model import Model
from hyperion.util.constants import kpc

from models import sky_model
from sources import setup_sources
from dust import setup_dust

if not os.path.exists('models'):
    os.mkdir('models')

if not os.path.exists('models/basic'):
    os.mkdir('models/basic')

seed = -43912

for model_name in sky_model:

    m = Model('models/basic/basic_%s' % model_name)

    seed += 1
    m.set_seed(seed)

    m = setup_sources(m, model_name, sky_model[model_name][0])
    m = setup_dust(m, **sky_model[model_name][1])

    image = m.add_peeled_images(image=True, sed=False)
    image.set_image_size(1, 1)
    image.set_viewing_angles([90.], [180.])
    image.set_image_limits(65., -65., -1., 1.)
    image.set_inside_observer((8.5 * kpc, 0. * kpc, 0.015 * kpc))
    image.set_wavelength_range(160, 3.0, 140.)
    image.set_track_origin('detailed')

    image = m.add_peeled_images(image=True, sed=False)
    image.set_image_size(130, 1)
    image.set_viewing_angles([90.], [180.])
    image.set_image_limits(65., -65., -1., 1.)
    image.set_inside_observer((8.5 * kpc, 0. * kpc, 0.015 * kpc))
    image.set_wavelength_range(160, 3.0, 140.)
    image.set_track_origin('detailed')

    image = m.add_peeled_images(image=True, sed=False)
    image.set_image_size(1, 40)
    image.set_viewing_angles([90.], [180.])
    image.set_image_limits(65., -65., -1., 1.)
    image.set_inside_observer((8.5 * kpc, 0. * kpc, 0.015 * kpc))
    image.set_wavelength_range(160, 3.0, 140.)
    image.set_track_origin('detailed')

    m.set_raytracing(True)

    m.set_n_initial_iterations(5)

    m.set_sample_sources_evenly(True)

    m.set_n_photons(initial=100000000, \
                    imaging=1000000000, \
                    raytracing_sources=1000000000, \
                    raytracing_dust=1000000000)

    m.write()
