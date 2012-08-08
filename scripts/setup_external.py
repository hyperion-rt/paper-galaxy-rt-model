import os

from hyperion.model import Model
from hyperion.util.constants import kpc

from models import sky_model
from sources import setup_sources
from dust import setup_dust

if not os.path.exists('models'):
    os.mkdir('models')

if not os.path.exists('models/external'):
    os.mkdir('models/external')

seed = -94452

for model_name in sky_model:

    m = Model('models/external/external_%s' % model_name)

    seed += 1
    m.set_seed(seed)

    m = setup_sources(m, model_name, sky_model[model_name][0])
    m = setup_dust(m, **sky_model[model_name][1])

    image = m.add_peeled_images(image=True, sed=False)
    image.set_viewing_angles([0.], [0.])
    image.set_image_size(512, 512)
    image.set_image_limits(-15 * kpc, 15 * kpc, -15 * kpc, 15 * kpc)
    image.set_wavelength_range(160, 3.0, 140.)

    m.set_raytracing(True)

    m.set_n_initial_iterations(3)

    m.set_n_photons(initial=100000000,
                    imaging=1000000000,
                    raytracing_sources=1000000000,
                    raytracing_dust=1000000000)

    m.write()
