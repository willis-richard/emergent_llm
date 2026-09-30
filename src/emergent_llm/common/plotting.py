import matplotlib
import matplotlib.pyplot as plt

def setup(configuration: str) -> tuple[tuple[float, float], str, float]:
    matplotlib.use('Agg')
    royal_width = 384.1122 / 72.27
    royal_format = 'png'
    royal_font = 9.

    if configuration == 'aamas_self_play_single':
        FIGSIZE, SIZE, FORMAT = (2.7, 1.5), 7., 'svg'
    elif configuration == 'aamas_self_play':
        FIGSIZE, SIZE, FORMAT = (8.2, 1.5), 7., 'svg'
    elif configuration == 'royal_self_play':
        FIGSIZE, SIZE, FORMAT = (royal_width, 1.5), royal_font, royal_format
    elif configuration == 'aamas_pca':
        FIGSIZE, SIZE, FORMAT = (8.2, 4), 7., 'svg'
    elif configuration == 'royal_pca':
        FIGSIZE, SIZE, FORMAT = (royal_width, 4), royal_font, royal_format
    elif configuration == 'poster_pca':
        FIGSIZE, SIZE, FORMAT = (13.5, 7.5), 27., 'svg'
    elif configuration == 'aamas_cooperation':
        FIGSIZE, SIZE, FORMAT = (7, 1.5), 7., 'svg'
    elif configuration == 'royal_cooperation':
        FIGSIZE, SIZE, FORMAT = (royal_width, 1.5), royal_font, royal_format
    elif configuration == 'viewing':
        FIGSIZE, SIZE, FORMAT = (7, 4), 8., 'svg'
    else:
        assert False, f"Unknown configuration: {configuration}"

    plt.rcParams.update({
        'font.size': SIZE,
        'axes.titlesize': 'medium',
        'axes.labelsize': 'medium',
        'figure.titlesize': 'medium',
        'figure.labelsize': 'medium',
        'xtick.labelsize': 'small',
        'ytick.labelsize': 'small',
        'legend.fontsize': 'medium',
        'legend.columnspacing': 0.3,
        'legend.handletextpad' : 0.1,
        'lines.markersize': SIZE / 4,
        'axes.linewidth': 0.5,
        'savefig.bbox': 'tight',
        'figure.constrained_layout.use': True,
        'savefig.pad_inches': 0.02,
    })

    if 'royal' in configuration:
        plt.rcParams.update({
            'ps.fonttype': 42,          # no Type 3 fonts
            'pdf.fonttype': 42,
            'font.family': 'serif',
            'font.serif': ['Times New Roman', 'Times', 'STIXGeneral'],
            'mathtext.fontset': 'stix', # Times-like maths
            "savefig.dpi": 600,
        })

    return FIGSIZE, FORMAT, SIZE
