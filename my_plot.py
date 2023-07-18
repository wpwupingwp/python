#!/usr/bin/python3

import argparse
import logging
from pathlib import Path
from sys import argv
from subprocess import run

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams, ticker
# config figure
font_settings = {'legend.fontsize': 'xx-large', 'axes.labelsize': 'xx-large',
                 'xtick.labelsize': 'xx-large', 'ytick.labelsize': 'x-large'}
rcParams.update(font_settings)
params = {'axes.linewidth': 1.5, 'font.family': 'sans-serif',
          'lines.linewidth': 1.5, 'legend.handlelength': 2,
          'figure.figsize': (16, 9)}
rcParams.update(params)
# define logger
FMT = '%(asctime)s %(levelname)-8s %(message)s'
DATEFMT = '%H:%M:%S'
Formatter = logging.Formatter(fmt=FMT, datefmt=DATEFMT)
Default_level = logging.INFO
import coloredlogs
coloredlogs.install(level=Default_level, fmt=FMT, datefmt=DATEFMT)
log = logging.getLogger(__name__)

# colors
red = '#db5000' #gene
yellow = '#eeba00,#f8d90f'.split(',') #cds, intron
blue = '#2a4a8b,#0091b5'.split(',') #trna rrna
green = '#058240' #spacer
gray = '#adcacb,#d3dcc8,#a4bfd1'.split(',') #others
colors = [red, *yellow, *blue, green, *gray]
# plt.bar(colors, [1]*len(colors), color=colors)
# plt.show()
print(colors)


def parse_args():
    arg = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=main.__doc__)
    arg.add_argument('-input', help='input file',
                     default=r'E:\Onedrive\IBCAS\Paper\BarcodeFinder\Figure\draw.xlsx')
    arg.add_argument('-type', choices=('box', 'groupbox', 'pie', 'dot',
                                       'stack', 'bar'),
                     default='box', help='figure type')
    arg.add_argument('-o', '-out', dest='out', help='output prefix',
                     default='draw_out')
    arg.add_argument('-no_show', action='store_true', help='show figure')
    option = arg.add_argument_group('Options')
    option.add_argument('-sheet', default=0, type=int, help='sheet index')
    option.add_argument('-horizon', action='store_false',
                        help='figure direction')
    option.add_argument('-italic', action='store_true', help='italic labels')
    option.add_argument('-merge_small', action='store_true',
                        help='merge small values in pie')
    option.add_argument('-y_log', action='store_true', help='log y axis or not')
    option.add_argument('-x_log', action='store_true', help='log y axis or not')
    option.add_argument('-x', default='', help='x label')
    option.add_argument('-y', default='', help='y label')
    option.add_argument('-y_percent', action='store_true',
                        help='set y ticks to percent')
    option.add_argument('-notch', action='store_true', help='notch of boxplot')
    option.add_argument('-inkscape',
                        default=r'"D:\Program Files\Inkscape\bin\inkscape.exe"',
                        help='inkscape path, for convert figure to emf')
    return arg.parse_args()


def init_arg(arg):
    # check input
    arg.input = Path(arg.input).absolute()
    if not arg.input.exists():
        log.error('Input does not exist.')
        raise SystemExit(-1)
    # init out
    if arg.out is None:
        arg.out = arg.input.with_suffix('.emf')
    else:
        arg.out = arg.input.parent / (arg.out+'.emf')
    if arg.out.exists():
        log.warning(f'Output file {arg.out} exists.')
    # add file log
    log_filename = arg.input.with_suffix('.log')
    log_file = logging.FileHandler(log_filename)
    log_file.setFormatter(Formatter)
    log_file.setLevel(Default_level)
    log.addHandler(log_file)
    return arg


def plot_set(plt, arg):
    plt.xlabel(arg.x)
    plt.ylabel(arg.y)
    yscale = 'log' if arg.y_log else 'linear'
    xscale = 'log' if arg.x_log else 'linear'
    plt.xscale(xscale)
    plt.yscale(yscale)
    if arg.y_percent:
        #plt.yticks(np.arange(0, 1.1, 0.1))
        ax = plt.gca()
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=2))
    pass


def svg2emf(plt, arg):
    svg = arg.out.with_suffix('.svg')
    pdf = arg.out.with_suffix('.pdf')
    plt.savefig(svg)
    plt.savefig(pdf)
    cmd = f'{arg.inkscape} -o "{arg.out}" "{svg}"'
    log.info('Convert svg to emf:')
    log.info(cmd)
    _ = run(cmd, shell=True)
    if arg.no_show:
        pass
    else:
        plt.show()
    if _.returncode:
        log.error('Conversion failed.')
        return arg.out
    return arg.out


def boxplot(arg):
    """
    table format:
    field1,field2,field3
    1,2,3
    4,5,6
    """
    flierprops = dict(marker='o', markeredgewidth=0.5,
                      markersize=5, alpha=0.5)
    boxprops = dict(linewidth=0.5, alpha=0.9)
    # grey
    medianprops = dict(linestyle='-', linewidth=0.9, alpha=0.8, color='#ddddee')
    textprops = dict(fontsize=8)
    raw_data = pd.read_excel(arg.input, sheet_name=arg.sheet)
    labels = raw_data.columns
    print(labels)
    filtered_data = [raw_data[i].dropna() for i in raw_data]
    bp = plt.boxplot(filtered_data, notch=arg.notch, labels=labels,
                     # labeldistance=5,
                     vert=arg.horizon, patch_artist=True, flierprops=flierprops,
                     boxprops=boxprops, medianprops=medianprops)
                    # textprops=textprops)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    plot_set(plt, arg)
    plt.xticks(np.arange(1, len(labels)+1), labels=labels)
    # plt.yticks([0, 50000, 100000, 150000, 200000],['0', '50,000', '100,000', '150,000', '200,000'])
    svg2emf(plt, arg)
    return arg.out


def boxplot2(arg):
    """
    boxplot for two groups of data
    table:
    group1-a,group2-a,group1-b,group2-b
    """
    flierprops = dict(marker='o', markeredgewidth=0.5,
                      markersize=5, alpha=0.5)
    boxprops = dict(linestyle='-', linewidth=0.5, alpha=0.9)
    # grey
    medianprops = dict(linestyle='-', linewidth=0.9, alpha=0.8, color='#ddddee')
    textprops = dict(fontsize=8)
    raw_data = pd.read_excel(arg.input, sheet_name=arg.sheet)
    labels = [raw_data.columns[i] for i in range(0, len(raw_data.columns), 2)]
    filtered_data = [raw_data[i].dropna() for i in raw_data]
    group_1 = [filtered_data[i] for i in range(0, len(filtered_data), 2)]
    group_2 = [filtered_data[i] for i in range(1, len(filtered_data), 2)]
    def draw(data, offset, fill=True):
        pos = np.arange(len(data)) + offset
        bp = plt.boxplot(data, positions=pos, notch=arg.notch, widths=0.35,
                         # labeldistance=5,
                         vert=arg.horizon, patch_artist=True,
                         flierprops=flierprops,
                         boxprops=boxprops, medianprops=medianprops)
        # textprops=textprops)
        if not fill:
            for patch, color in zip(bp['boxes'], colors):
                patch.set_color('black')
                patch.set_facecolor(color)
        else:
            for patch, color in zip(bp['boxes'], colors):
                patch.set_color(color)
                patch.set_facecolor('none')
    draw(group_1, -0.2, True)
    draw(group_2, 0.2, False)
    plot_set(plt, arg)
    plt.xticks(np.arange(0, 5), labels=labels)
    svg2emf(plt, arg)
    return arg.out



def barplot(arg):
    """
    table format:
    field,number
    A,2
    B,3
    """
    data = pd.read_excel(arg.input, sheet_name=arg.sheet)
    labels = data.iloc[:,0]
    count = data.iloc[:,1]
    if arg.italic:
        labels = [f'${{{i}}}$' for i in labels]
    pie = plt.bar(labels, count, color=colors)
    plot_set(plt, arg)
    svg2emf(plt, arg)
    return arg.out


def pieplot(arg):
    """
    table format:
    field,number
    A,2
    B,3
    """
    def func(pct, values):
        absolute = int(round(pct/100*sum(values)))
        return f'{pct/100:.1%}, {absolute}'

    data = pd.read_excel(arg.input, sheet_name=arg.sheet)
    labels = data.iloc[:,0]
    count = data.iloc[:,1]
    print(labels, count)
    if arg.italic:
        labels = [f'${{{i}}}$' for i in labels]
    pie = plt.pie(count, labels=labels, autopct=lambda pct: func(pct, count),
                  colors=colors)
    svg2emf(plt, arg)
    return arg.out


def scatter(arg):
    """
    table format:
    Type,x,y
    """
    raw_data = pd.read_excel(arg.input, sheet_name=arg.sheet)
    # skip type
    type_ = raw_data.columns[0]
    labels = raw_data.columns[1:]
    groups = raw_data.groupby(type_)
    for name, data in groups:
        filtered_data = [data[i].dropna() for i in data]
        x = filtered_data[1]
        y = filtered_data[2]
        plt.scatter(x, y, label=name, alpha=0.8, edgecolor='none')
    plt.legend()
    plt.plot([2000, 2000], [0, 1], 'k--', alpha=0.5)
    plot_set(plt, arg)
    svg2emf(plt, arg)
    return arg.out


def stackplot(arg):
    """
    table format:
    field1,field2,field3
    1,2,3
    4,5,6
    """
    # grey
    textprops = dict(fontsize=8)
    raw_data = pd.read_excel(arg.input, sheet_name=arg.sheet)
    labels = raw_data.columns
    filtered_data = [raw_data[i].dropna() for i in raw_data]
    sp = plt.stackplot(range(len(filtered_data[0])), filtered_data,
                       labels=labels, colors=colors)
    #for patch, color in zip(sp['stacks'], colors):
    #    patch.set_facecolor(color)
    plot_set(plt, arg)
    plt.legend(loc='upper left')
    # plt.xticks(np.arange(1, len(labels)+1), labels=labels)
    #plt.xticks([])
    plt.yticks([0, 50000, 100000, 150000, 200000],
               ['0', '50,000', '100,000', '150,000', '200,000'])
    svg2emf(plt, arg)
    return arg.out


def main():
    """
    draw boxplot with matplotlib
    Usage:
    python3 my_plot.py data.csv [output_file]
    """
    arg = parse_args()
    arg = init_arg(arg)
    log.info('python3 '+' '.join(argv))
    # start here
    type_func = {'box': boxplot, 'pie': pieplot, 'groupbox': boxplot2,
                 'dot': scatter, 'stack': stackplot, 'bar': barplot}
    func = type_func.get(arg.type, 'None')
    if func is None:
        raise ValueError('Figure type is invalid.')
    else:
        func(arg)
    # end
    log.info('Bye')


if __name__ == '__main__':
    main()
