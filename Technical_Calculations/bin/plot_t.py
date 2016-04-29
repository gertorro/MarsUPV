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
    return rho_lco2 * fsolve(loop, m_p / 2. / rho_lco2)
    


def main():
    mpl.rcParams['font.size'] = 11
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['text.usetex'] = 'True'
    pgf_preamble = (r'\usepackage{/home/luismi/doc/2016/'
        + r'spaceapps/latex_stylesheet}')
    mpl.rcParams['text.latex.preamble'] = pgf_preamble
    m_a = np.linspace(50, 90)
    m_p = np.linspace(25., 200.)
    M_a, M_p = np.meshgrid(m_a, m_p)
    M_a, M_co2 = np.meshgrid(m_a, m_co2(m_p))
    m_e = 20.
    m_s = 65.
    m_jp = 30.
    m_tp = 10.
    m_d_1 = M_a + m_e + m_s + m_jp + M_co2
    m_d_2 = M_a + m_e + m_s + m_jp + m_tp
    Isp = 3050.
    g = 3.711
    dt_1 = -Isp / g * np.log(m_d_1 / (m_d_1 + M_p))
    dt_2 = -Isp / g * np.log(m_d_2 / (m_d_2 + M_p))
    fig, ax = new_ax()
    c = ax.contourf(M_a, M_p, dt_1, np.arange(50, 651, 25),
                    cmap=mpl.cm.viridis)
    c2 = ax.contour(M_a, M_p, dt_1, np.arange(50, 651, 50),
                    colors='k', linestyles='--')
    ax.set_xlabel(r'$m_a$ [\si{\kilogram}]')
    ax.set_ylabel(r'$m_p$ [\si{\kilogram}]')
    cb = plotty.colorbar(c, pad=0.15, fraction=0.1)
    cb.set_label(r'$t$ [\si{\second}]')
    ax.clabel(c2, fmt='%.0f s')
    plotty.candy(ax, ncol=2, cb=True, pad=0.15, fraction=0.1)
    ax.xaxis.set_ticks([50., 60., 70., 80.])
    ax.yaxis.set_ticks([25, 50., 75., 100., 125., 150., 175.])
    fig.savefig('img/delta_t_co2.pdf')
    plt.close(fig)
    fig, ax = new_ax()
    c = ax.contourf(M_a, M_p, dt_2, np.arange(50, 651, 25),
                    cmap=mpl.cm.viridis)
    c2 = ax.contour(M_a, M_p, dt_2, np.arange(50, 651, 50),
                    colors='k', linestyles='--')
    ax.set_xlabel(r'$m_a$ [\si{\kilogram}]')
    ax.set_ylabel(r'$m_p$ [\si{\kilogram}]')
    cb = plotty.colorbar(c, pad=0.15, fraction=0.1)
    cb.set_label(r'$t$ [\si{\second}]')
    ax.clabel(c2, fmt='%.0f s')
    plotty.candy(ax, ncol=2, cb=True, pad=0.15, fraction=0.1)
    ax.xaxis.set_ticks([50., 60., 70., 80.])
    ax.yaxis.set_ticks([25, 50., 75., 100., 125., 150., 175.])
    fig.savefig('img/delta_t_tp.pdf')

if __name__ == '__main__':
    main()
