#!/bin/bash

# First set up the SKY models
cd SKY
./do.sh
cd ..

# Now set up the RT models

if [ -d "models" ]; then
    rm -r models/*
else
    mkdir models
fi

python scripts/setup_basic.py
python scripts/setup_indiv.py
python scripts/setup_external.py

# Run all the moodels

python scripts/run_all.py

# Now make all plots

if [ -d "plots" ]; then
    rm -r plots/*
else
    mkdir plots
fi

python scripts/extract_external.py
python scripts/extract_profiles.py

python scripts/plot_energy.py
python scripts/plot_fractions.py
python scripts/plot_profiles.py
python scripts/plot_spectrum.py
python scripts/plot_external.py
python scripts/plot_radial_density.py
python scripts/plot_unresolved.py
