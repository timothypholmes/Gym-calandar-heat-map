#! /usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


days = ['Sun.', 'Mon.', 'Tues.', 'Wed.', 'Thurs.', 'Fri.', 'Sat.']
months = ['J.', 'F.', 'M.', 'A.', 'M.', 'J.', 'J.', 'A.', 'S.', 'O.', 'N.', 'D.']


def calendar_heatmap(series, start=None, end=None, mean=False, ax=None, **kwargs):
    '''Plot a calendar heatmap given a datetime series.

    Arguments:
        series (pd.Series):
            A series of numeric values with a datetime index. Values occurring
            on the same day are combined by sum.
        start (Any):
            The first day to be considered in the plot. The value can be
            anything accepted by :func:`pandas.to_datetime`. The default is the
            earliest date in the data.
        end (Any):
            The last day to be considered in the plot. The value can be
            anything accepted by :func:`pandas.to_datetime`. The default is the
            latest date in the data.
        mean (bool):
            Combine values occurring on the same day by mean instead of sum.
        ax (matplotlib.Axes or None):
            The axes on which to draw the heatmap. The default is the current
            axes in the :module:`~matplotlib.pyplot` API.
        **kwargs:
            Forwarded to :meth:`~matplotlib.Axes.pcolormesh` for drawing the
            heatmap.

    Returns:
        matplotlib.collections.Axes:
            The axes on which the heatmap was drawn. This is set as the current
            axes in the `~matplotlib.pyplot` API.
    '''
    dates = series.index.floor('D')
    group = series.groupby(dates)
    series = group.mean() if mean else group.sum()

    start = pd.to_datetime(start or series.index.min())
    end = pd.to_datetime(end or series.index.max())

    end += np.timedelta64(1, 'D')

    start_sun = start - np.timedelta64((start.dayofweek + 1) % 7, 'D')
    end_sun = end + np.timedelta64(7 - end.dayofweek - 1, 'D')

    num_weeks = (end_sun - start_sun).days // 7
    heatmap = np.zeros((7, num_weeks))
    ticks = {} 
    for week in range(num_weeks):
        for day in range(7):
            date = start_sun + np.timedelta64(7 * week + day, 'D')
            if date.day == 1:
                ticks[week] = months[date.month - 1]
            if date.dayofyear == 1:
                ticks[week] += f'\n{date.year}'
            if start <= date < end:
                heatmap[day, week] = series.get(date, 0)

    y = np.arange(8) - 0.5
    x = np.arange(num_weeks + 1) - 0.5

    ax = ax or plt.gca()
    mesh = ax.pcolormesh(x, y, heatmap, **kwargs)
    ax.invert_yaxis()

    ax.set_xticks(list(ticks.keys()))
    ax.set_xticklabels(list(ticks.values()))
    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(days)

    plt.sca(ax)
    plt.sci(mesh)

    return ax

def gym_heatmap():
    dates = pd.date_range(start='2015-01-01', end='2018-12-31')
    data = pd.read_csv('~/Desktop/Gym-calandar-heat-map/all_data.csv')
    data = dict(zip(data['Date'], data['Time_Numerical']))
    print(data)
    data = pd.Series(data)
    data.index = pd.DatetimeIndex(data.index)
    data = data.reindex(dates, fill_value=-100)

    figsize = plt.figaspect(7 / 56*3)
    fig = plt.figure(figsize=figsize)

    ax = calendar_heatmap(data, edgecolor='black')
    plt.colorbar(ticks=range(100), pad=0.02)

    cmap = mpl.cm.get_cmap('cividis', 100)
    plt.set_cmap(cmap)
    plt.clim(0.1, .99)

    fig.savefig('heatmap.png', bbox_inches='tight')
    plt.show(fig)


if __name__ == "__main__":

    gym_heatmap()