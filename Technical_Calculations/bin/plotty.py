import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.patheffects as PathEffects


golden_ratio = (1 + np.sqrt(5)) / 2.


colors = [(0.1, 0.1, 0.4), (0.8, 0.3, 0.3), (0.3, 0.8, 0.3),
          (0.1, 0.3, 0.9), (0.7, 0.5, 0.5), (0.7, 0.8, 0.5),
          (0.7, 0.8, 0.8)]


def forbidden(ax, limit, n=6):
    clip_path = Polygon(limit, color='white', alpha=0.)
    ax.add_patch(clip_path)
    x = np.linspace(-1, 1, 2 * n, endpoint=False)
    for i in range(n):
        v = np.array([[x[2*i], 0.], [x[2*i+1], 0.],
            [x[2*i+1] + 1., 1.], [x[2*i] + 1., 1.]])
        p = ax.add_patch(Polygon(v, color='red', alpha=0.3,
                         transform=ax.transAxes))
        p.set_clip_path(clip_path)


def candy(ax, draw_legend=True, ratio=golden_ratio, draw_grid=False,
          draw_minor_grid=True, lines=None, set_aspect=True, **kwargs):
    fancybox = kwargs.pop('fancybox', True)
    handlelength = kwargs.pop('handlelength', 1.)
    handletextpad = kwargs.pop('handletextpad', 0.3)
    labelspacing = kwargs.pop('labelspacing', 0.25)
    linewidth = kwargs.pop('linewidth', 0.5)
    loc = kwargs.pop('loc', 'best')
    numpoints = kwargs.pop('numpoints', 1)
    prune = kwargs.pop('prune', 'upper')
    scatterpoints = kwargs.pop('scatterpoints', 1)
    shadow = kwargs.pop('shadow', False)
    labelpad = kwargs.pop('labelpad', 2)
    kwargs.pop('color', None)
    kwargs.pop('linestyle', None)
    kwargs.pop('which', None)
    legend_alpha = kwargs.pop('legend_alpha', None)

    ax.minorticks_on()
    delta_x = (ax.xaxis.get_view_interval()[1]
               - ax.xaxis.get_view_interval()[0])
    delta_y = (ax.yaxis.get_view_interval()[1]
               - ax.yaxis.get_view_interval()[0])
    if (set_aspect == True):
        ax.set_aspect(delta_x / delta_y / ratio, adjustable='box-forced')
    fp = mpl.font_manager.FontProperties

    if draw_legend is True:
        try:
            if lines is None:
                leg = ax.legend(loc=loc, prop=fp(size='medium'),
                                numpoints=numpoints,
                                scatterpoints=scatterpoints,
                                handletextpad=handletextpad,
                                shadow=shadow,
                                fancybox=fancybox,
                                labelspacing=labelspacing,
                                handlelength=handlelength,
                                **kwargs)
            else:
                leg = ax.legend(lines, [l.get_label() for l in lines],
                                loc=loc, prop=fp(size='medium'),
                                numpoints=numpoints,
                                scatterpoints=scatterpoints,
                                handletextpad=handletextpad,
                                shadow=shadow,
                                fancybox=fancybox,
                                labelspacing=labelspacing,
                                handlelength=handlelength,
                                **kwargs)
            frame = leg.get_frame()
            frame.set_facecolor('0.95')
            leg.set_zorder(10)
            if legend_alpha is not None:
                frame.set_alpha(legend_alpha)
                leg.set_alpha(legend_alpha)
        except:
            pass
    if (draw_grid is True):
        ax.grid('on', which='major', linestyle='solid', linewidth=linewidth,
                #color='white')
                color=[0.55, 0.55, 0.55])
        if (draw_minor_grid is True):
            ax.grid('on', which='minor', linestyle='dotted',
                    #linewidth=linewidth, color='white')
                    linewidth=linewidth, color=[0.6, 0.6, 0.6])
    ymajorlocator = mpl.ticker.MaxNLocator(nbins=4, prune=prune)
    yminorlocator = mpl.ticker.AutoMinorLocator(5)
    ax.yaxis.set_major_locator(ymajorlocator)
    ax.yaxis.set_minor_locator(yminorlocator)
    xmajorlocator = mpl.ticker.MaxNLocator(nbins=4, prune=prune)
    xminorlocator = mpl.ticker.AutoMinorLocator(5)
    ax.xaxis.set_major_locator(xmajorlocator)
    ax.xaxis.set_minor_locator(xminorlocator)
    ax.set_axisbelow(True)
    ax.set_axis_bgcolor('white')
    for spine in ax.spines.values():
        spine.set_color('0.65')
    for x in [ax.xaxis, ax.yaxis]:
        for y in [x.get_minorticklines(), x.get_ticklines()]:
            for z in y:
                z.set_color('0.55')
    ax.xaxis.labelpad = labelpad
    ax.yaxis.labelpad = labelpad


def new_ax(axis_width=2.67, fig_width=3.07087, fig_height='auto',
           x_0='auto', y_0='auto', rel_offset=True,
           cb=True, cb_height=0.15, cb_pad=0.3,
           shrink=0.8, ratio=golden_ratio,
           fig=None, sharex=None):
    if cb is True:
        A = 1 + cb_height + cb_pad
    else:
        A = 1.
    dx = axis_width / fig_width
    axis_height = axis_width / ratio * A
    if ((rel_offset is False)
        and (y_0 is not 'auto')
        and (fig_height is 'auto')):
        fig_height = (y_0 + axis_height)
    if fig is None:
        fig = plt.figure(figsize=(fig_width, fig_height))
    dy = axis_height / fig_height
    if x_0 is 'auto':
        x_0 = (fig_width - axis_width) / 2. / fig_width
    if y_0 is 'auto':
        y_0 = (fig_height - axis_height) / 2. / fig_height
    if rel_offset is False:
        x_0 = x_0 / fig_width
        y_0 = y_0 / fig_height
    if sharex is None:
        ax = plt.axes([x_0, y_0, dx, dy])
    else:
        sharex.yaxis.tick_left()
        ax = plt.axes([x_0, y_0, dx, dy], sharex=sharex, frameon=False)
        ax.yaxis.tick_right()
        ax.xaxis.set_visible(False)
        ax.yaxis.set_label_position('right')
    #ax.set_color_cycle(plt.cm.Paired(np.linspace(0, 1, 12)))
    fig.patch.set_alpha(0.)
    return fig, ax


def colorbar(c, ax=None, orientation='horizontal', shrink=0.8, pad=0.2,
             fraction=0.15):
    B = pad / (1. + fraction + pad)
    C = (fraction / (1. + fraction + pad))
    try:
        cb = plt.colorbar(c, ax=ax, orientation=orientation,
                          shrink=shrink, pad=B, fraction=C)
    except:
        cb = plt.colorbar(c, ax=plt.gca(), orientation=orientation,
                          shrink=shrink, pad=B, fraction=C)
    return cb


def get_convex_hull(x, y):
    hull = ConvexHull(np.array((x, y)).T)
    idx = hull.vertices
    idx = np.append(idx, idx[0])
    return x[idx], y[idx]


def smooth(x, window_len=11, window='hanning'):
    if window_len < 3:
        return x
    s = np.r_[2*x[0]-x[window_len-1::-1], x, 2*x[-1]-x[-1:-window_len:-1]]
    if window is 'flat': #moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval(window + '(window_len)')
    y = np.convolve(w / w.sum(), s, mode='same')
    return y[window_len:-window_len+1]


def cm_to_inches(x):
    return x / 2.54


def stroke_labels(ax, stroke_color, text_color, linewidth=1.5):
    for t in (ax.xaxis.get_ticklabels() + ax.yaxis.get_ticklabels()
              + [ax.xaxis.get_label(), ax.yaxis.get_label(),
                 ax.xaxis.get_offset_text(), ax.yaxis.get_offset_text()]):
        stroke_text(t, stroke_color, text_color, linewidth)


def stroke_text(text, stroke_color, text_color, linewidth=1.5):
    text.set_color(text_color)
    text.set_path_effects([PathEffects.withStroke(linewidth=linewidth,
                                                  foreground=stroke_color)])
