#!/usr/bin/python

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotty


markers = {1000: 'o',
           1250: 's',
           1500: '^',
           1750: 'v',
           2000: 'h',
           2250: '*',
           2500: '<',
           3000: '>',
           3500: 'D',
           4000: 'd',
           4750: (5, 0, 0)}


def inches(x):
    return plotty.cm_to_inches(x)


def legend_labels(ax):
    ax.plot([], [], '-', color='k', label='Experiment', linewidth=2)
    ax.plot([], [], '-', color=plotty.colors[0], label='Vanilla', linewidth=2)
    ax.plot([], [], '-', color=plotty.colors[1], label='CMT-TCM', linewidth=2)


def new_ax():
    fig, ax = plotty.new_ax(fig_width=inches(15), axis_width=inches(13.5),
                            x_0=inches(1.5), y_0=inches(0.77), cb_pad=0.15,
                            rel_offset=False, cb=True, cb_height=0.1)
    return fig, ax


def T(h):
    return -31. - 0.000998 * h + 273.15


def p(h):
    return 699. * np.e ** (-0.00009 * h)


def rho(h):
    return p(h) / T(h) / 192.1


def h(p):
    return np.log(699. / p) / 0.00009


def main():
    mpl.rcParams['font.size'] = 11
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['text.usetex'] = 'True'
    pgf_preamble = (r'\usepackage{/home/luismi/doc/2016/'
        + r'spaceapps/latex_stylesheet}')
    mpl.rcParams['text.latex.preamble'] = pgf_preamble
    data = []
    for i in range(1, 6):
        data.append(pd.read_fwf('data/rocket/{}0000.csv'.format(i)))
    height = []
    p_c = []
    isp = []
    for d in data:
        height += (h(d.p.values[2:] * 1E5) / 1E3).tolist()
        isp += d.isp.values[2:].tolist()
    for i in range(1, 6):
        p_c += len(data[0].values[2:]) * [i * 10]
    triang = mpl.tri.Triangulation(p_c, height)
    fig, ax = new_ax()
    c1 = ax.tricontourf(triang, isp, np.arange(2900, 3151, 25), 
        cmap=mpl.cm.viridis)
    c2 = ax.tricontour(triang, isp, np.arange(2900, 3151, 50), 
        colors='k', linestyles='--')
    cb = plotty.colorbar(c1, pad=0.15, fraction=0.1)
    cb.set_label(r'$Isp$ [\si{\metre\per\second}]')
    ax.clabel(c2, fmt=r'%.0f \si{\metre\per\second}')
    ax.set_xlabel(r'$p_c$ [\si{\mega\pascal}]')
    ax.set_ylabel(r'$h$ [\si{\kilo\metre}]')
    plotty.candy(ax, ncol=2, cb=True, pad=0.15, fraction=0.1)
    ax.xaxis.set_ticks([10, 20, 30, 40])
    ax.yaxis.set_ticks([-4., -3., -2., -1., 0.])
    fig.savefig('img/isp.pdf')


if __name__ == '__main__':
    main()
