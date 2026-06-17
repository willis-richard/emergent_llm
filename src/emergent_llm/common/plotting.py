import matplotlib
import matplotlib.pyplot as plt

def setup(configuration: str) -> tuple[tuple[float, float], str, float]:
    matplotlib.use('Agg')

    if configuration == 'aamas_self_play':
        FIGSIZE, SIZE, FORMAT = (8.2, 1.5), 7, 'svg'
    elif configuration == 'aamas_diversity':
        FIGSIZE, SIZE, FORMAT = (8.2, 4), 7, 'svg'
    elif configuration == 'aamas_cooperation':
        FIGSIZE, SIZE, FORMAT = (7, 1.5), 7, 'svg'
    elif configuration == 'poster_diversity':
        FIGSIZE, SIZE, FORMAT = (13.5, 7.5), 27, 'svg'
    elif configuration == 'viewing':
        FIGSIZE, SIZE, FORMAT = (7, 4), 8, 'svg'
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

    return FIGSIZE, FORMAT, SIZE
