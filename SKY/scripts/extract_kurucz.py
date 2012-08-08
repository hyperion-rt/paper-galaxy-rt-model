from StringIO import StringIO

import numpy as np
import atpy


def chunk(string, n):
    return [string[i * n:i * n + n] for i in range(len(string) / n)]


def extract_kurucz(req_teff, req_logg):

    # Open file
    f = open('kurucz/fp00k2odfnew.pck', 'rb')

    # Replace strange line endings
    f = StringIO(f.read().replace('\r', '\n'))

    # Skip header
    while f.readline().strip() != "END":
        pass

    # Read in wavelengths
    n_wav = 1221
    wav = []
    while len(wav) < n_wav:
        wav += f.readline().strip().split()
    wav = np.array(wav, dtype=float)

    for i in range(476):

        # Read in header line
        header = f.readline()

        # Extract information from header
        _, teff, _, logg, _ = header.split(None, 4)
        teff, logg = float(teff), float(logg)

        # Read model flux
        fnu = []
        while len(fnu) < n_wav:
            fnu += chunk(f.readline().strip(), 10)
        fnu = np.array(fnu, dtype=float)

        # Read continuum flux
        fnu_cont = []
        while len(fnu_cont) < n_wav:
            fnu_cont += chunk(f.readline().strip(), 10)
        fnu_cont = np.array(fnu_cont, dtype=float)

        if teff == req_teff and logg == req_logg:

            # Create table to contain spectrum
            t = atpy.Table()

            # Write parameters to header
            t.keywords['teff'] = teff
            t.keywords['logg'] = logg

            # Add wavelength/frequency info
            t.add_column('wav', wav / 1000.)
            t.add_column('nu', 29979245800. / (wav * 1.e-7))

            # Add flux columns
            t.add_column('fnu', fnu)
            t.add_column('fnu_cont', fnu_cont)

            return t

    print "WARNING: Spectrum not found", req_teff, req_logg
    return None
