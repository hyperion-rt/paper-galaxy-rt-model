from matplotlib.colors import ColorConverter


def group(spectral_type):

    if 'AGB' in spectral_type:
        return 2
    elif 'III' in spectral_type:
        return 3
    elif 'V' in spectral_type:
        return 4
    elif 'YOUNG OB' in spectral_type:
        return 4
    elif 'TAURI' in spectral_type:
        return 0
    elif 'H_II' in spectral_type:
        return 0
    elif 'PN' in spectral_type:
        return 0
    elif 'X' in spectral_type:
        return 0
    elif 'I' in spectral_type:
        return 1
    elif 'dust' in spectral_type:
        return 5
    else:
        return 0

groups = ['Other', 'Supergiants', 'AGB', 'Giants', 'Main Sequence', 'PAHs', 'VSGs', 'Big grains', 'Scattered Light']
groups_short = ['Other', 'Supergiants', 'AGBs', 'Giants', 'Main Seq.', 'PAHs', 'VSGs', 'Big grains', 'Scat.']
group_colors = ['gray', 'purple', 'blue', (0., 0.5,  0.5), 'green', 'red', 'orange', 'yellow', 'black']
light_group_colors = []

converter = ColorConverter()
for color in group_colors:
    r, g, b = converter.to_rgb(color)
    r = 0.5 + r / 2.
    g = 0.5 + g / 2.
    b = 0.5 + b / 2.
    light_group_colors.append((r, g, b))


def color(spectral_type):
    return group_colors[group(spectral_type)]
