import matplotlib
import matplotlib.pyplot as plt

def setup(configuration: str) -> tuple[tuple[float, float], str]:
    matplotlib.use('Agg')

    if configuration == '3_col_paper':
        FIGSIZE, SIZE, FORMAT = (2.2, 0.9), 7, 'svg'
    elif configuration == '2_col_paper':
        FIGSIZE, SIZE, FORMAT = (2.5, 0.9), 8, 'svg'
    elif configuration == '1_col_slide':
        FIGSIZE, SIZE, FORMAT = (5, 1.2), 8, 'svg'
    elif configuration == '1_col_poster':
        FIGSIZE, SIZE, FORMAT = (5, 3.5), 27, 'svg'
    elif configuration == 'diversity':
        FIGSIZE, SIZE, FORMAT = (7, 4), 8, 'svg'
    elif configuration == 'diversity_poster':
        FIGSIZE, SIZE, FORMAT = (13.5, 7.5), 27, 'svg'
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
        'axes.linewidth': 0.1
    })

    return FIGSIZE, FORMAT, SIZE
