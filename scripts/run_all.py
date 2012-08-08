import os
import glob

for filename in glob.glob('models/*/*.rtin'):

    filename_out = filename.replace('.rtin', '.rtout')

    if os.path.exists(filename_out):
        continue

    os.system('hyperion -m 12 %s %s' % (filename, filename.replace('.rtin', '.rtout')))
