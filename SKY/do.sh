#!/bin/bash

if [ -d "models" ]; then
    rm -r models/*
else
    mkdir models
fi

# Produce table of spectra
python scripts/sky_spectra.py

# Run SKY models
python scripts/sky_original.py
python scripts/sky_updarm.py
python scripts/sky_updarm_gaussian.py

