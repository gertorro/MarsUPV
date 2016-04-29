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
    fig, ax = plotty.new_ax(fig_width=inches(8.), axis_width=inches(6.8),
                            x_0=inches(1.2), y_0=inches(1.),
                            rel_offset=False, cb=False)
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
    m_p = np.linspace(25, 200, 100)
    fig, ax = new_ax()
    ax.plot(m_p, m_co2(m_p), color=plotty.colors[0], linewidth=2)
    ax.set_xlabel(r'$m_p$ [\si{\kilogram}]')
    ax.set_ylabel(r'$m_{\textnormal{CO}_2}$ [\si{\kilogram}]')
    ax.axis(xmin=25, ymax=75)
    plotty.candy(ax)
    ax.xaxis.set_ticks([25, 75., 125., 175.])
    ax.yaxis.set_ticks([0, 20, 40, 60])
    fig.savefig('img/co2.pdf')

if __name__ == '__main__':
    main()
