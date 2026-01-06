import matplotlib
import matplotlib.pyplot as plt

def setup(configuration: str) -> tuple[tuple[float, float], str]:
    matplotlib.use('Agg')

    if configuration == '3_col_paper':
        FIGSIZE, SIZE, FORMAT = (2.2, 0.8), 7, 'svg'
    elif configuration == '2_col_paper':
        FIGSIZE, SIZE, FORMAT = (2.5, 0.9), 8, 'svg'
    elif configuration == '1_col_slide':
        FIGSIZE, SIZE, FORMAT = (5, 1.2), 8, 'svg'
    else:
        assert False, f"Unknown configuration: {configuration}"

    plt.rcParams.update({
        'font.size': SIZE,
        'axes.titlesize': 'medium',
        'axes.labelsize': 'medium',
        'xtick.labelsize': 'small',
        'ytick.labelsize': 'small',
        'legend.fontsize': 'medium',
        'lines.markersize': SIZE / 4,
        'legend.handlelength': SIZE / 6,
        'axes.linewidth': 0.1
    })

    return FIGSIZE, FORMAT
