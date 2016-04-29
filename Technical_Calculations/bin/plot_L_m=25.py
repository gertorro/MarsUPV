#!/usr/bin/python

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotty
from scipy.optimize import fsolve


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


def new_ax():
    fig, ax = plotty.new_ax(fig_width=inches(15), axis_width=inches(13.5),
                            x_0=inches(1.5), y_0=inches(0.75), cb_pad=0.15,
                            rel_offset=False, cb=True, cb_height=0.1)
    return fig, ax

def m_co2(m_p):
    rho_lox = 1200.
    rho_lng = 450.
    m_lox = m_p / 3. * 2.
    m_lng = m_p / 3.
    V_lox = m_lox / rho_lox
    V_lng = m_lng / rho_lng
    V_p = V_lox + V_lng
    rho_lco2 = 1050.
    R_co2 = 188.9
    rho_co2_min = 10E6 / R_co2 / 250.
    m_p_co2 = rho_co2_min * V_p
    def loop(V_co2):
        return V_co2 * rho_lco2 / (V_p + V_co2) - rho_co2_min
    return rho_lco2 * fsolve(loop, m_p / 2. / rho_lco2)[0]
    

def D(v, h):
    A_f = 2.
    C_D = 1.3
    return 0.5 * rho(h) * v ** 2 * A_f * C_D


def W(m_p, m_a):
    m_e = 20.
    m_s = 65.
    m_jp = 30.
    m_tp = 10.
    try:
        m_co2_ = np.array([m_co2(m) for m in m_p])
    except:
        m_co2_ = m_co2(m_p)
    m_d = m_a + m_e + m_s + m_jp + m_co2_
    g = 3.711
    return (m_d + m_p) * g


def t(v, h, m_a):
    Isp = 3050.
    m_p = np.linspace(5., 20.)
    t_ = np.ones(np.shape(v))
    for i in range(np.shape(v)[0]):
        for j in range(np.shape(v)[1]):
            t_[i, j] = np.trapz(Isp / np.sqrt(D(v[i, j], h[i, j]) ** 2
                                              + W(m_p, m_a) ** 2), m_p)
    return t_


def L(v, h, m_a):
    return v * t(v, h, m_a)


def T(h):
    return -31. - 0.000998 * h + 273.15


def p(h):
    return 699. * np.e ** (-0.00009 * h)


def rho(h):
    return p(h) / T(h) / 192.1


def main():
    mpl.rcParams['font.size'] = 11
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['text.usetex'] = 'True'
    pgf_preamble = (r'\usepackage{/home/luismi/doc/2016/'
        + r'spaceapps/latex_stylesheet}')
    mpl.rcParams['text.latex.preamble'] = pgf_preamble
    v = np.linspace(0, 250., 50)
    h = np.linspace(-4000., 1000., 50)
    V, H = np.meshgrid(v, h)
    fig, ax = new_ax()
    c1 = ax.contourf(V, H / 1E3, L(V, H, 90.) / 1E3,
                     np.arange(0, 9.6, 0.5), cmap=mpl.cm.viridis)
    c2 = ax.contour(V, H / 1E3, L(V, H, 90.) / 1E3,
                    np.arange(0, 9.6, 1), colors='k', linestyles='--')
    cb = plotty.colorbar(c1, pad=0.15, fraction=0.1)
    cb.set_label(r'$L$ [\si{\kilo\metre}]')
    ax.clabel(c2, fmt='%.0f \si{\kilo\metre}')
    ax.set_xlabel(r'$v$ [\si{\metre\per\second}]')
    ax.set_ylabel(r'$h$ [\si{\kilo\metre}]')
    plotty.candy(ax, ncol=2, cb=True, pad=0.15, fraction=0.1)
    ax.xaxis.set_ticks([0, 50, 100, 150, 200])
    ax.yaxis.set_ticks([-4., -3., -2., -1., 0.])
    fig.savefig('img/l_ma_90_mp_25.pdf')
    plt.close(fig)
    fig, ax = new_ax()
    c1 = ax.contourf(V, H / 1E3, L(V, H, 60.) / 1E3,
                     np.arange(0, 9.6, 0.5), cmap=mpl.cm.viridis)
    c2 = ax.contour(V, H / 1E3, L(V, H, 60.) / 1E3,
                    np.arange(0, 9.6, 1), colors='k', linestyles='--')
    cb = plotty.colorbar(c1, pad=0.15, fraction=0.1)
    cb.set_label(r'$L$ [\si{\kilo\metre}]')
    ax.clabel(c2, fmt='%.0f \si{\kilo\metre}')
    ax.set_xlabel(r'$v$ [\si{\metre\per\second}]')
    ax.set_ylabel(r'$h$ [\si{\kilo\metre}]')
    plotty.candy(ax, ncol=2, cb=True, pad=0.15, fraction=0.1)
    ax.xaxis.set_ticks([0, 50, 100, 150, 200])
    ax.yaxis.set_ticks([-4., -3., -2., -1., 0.])
    fig.savefig('img/l_ma_60_mp_25.pdf')
    plt.close(fig)


if __name__ == '__main__':
    main()
