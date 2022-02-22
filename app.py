from typing import Tuple
import numpy as np
import svgwrite
import panel as pn
from panel import widgets
from panel.template import DarkTheme

pn.extension()

default_file_name = './vortex.svg'


def w(i: int, min_w: float = 0.05, scale: float = 10.0):
    return min_w + (scale / i)


def map_ds_idx(n,N):
    return (N/2-np.abs(n-N/2)).astype(int)


def create_arrow_marker_sumner(dwg, s=1):
    arrow = dwg.marker(id='arrow', insert=(20/s, 5/s), size=(20/s, 10/s), orient='auto', markerUnits='strokeWidth')
    arrow.add(dwg.path(d=f'M0,{10/s} l{3.128/s},{-5/s} l{-3.128/s},-{5/s} l{20/s},{5/s} Z', fill='#f00'))
    dwg.defs.add(arrow)
    return arrow


def rainbow_scale(v: float, min_v=0., max_v=1.):
    x = (v - min_v) / (max_v - min_v)
    if x < 1 / 3:
        r = 1 - 3 * x
        g = 3 * x
        b = 0
    elif x < 2 / 3:
        r = 0
        g = 1 - 3 * (x - 1 / 3)
        b = 3 * (x - 1 / 3)
    else:
        r = 3 * (x - 2 / 3)
        g = 0
        b = 1 - 3 * (x - 2 / 3)
    return int(255 * r), int(255 * g), int(255 * b)


def create_svg(num_p: int,
               mult: int,
               color_mode: str,
               c: Tuple[int, int, int] = (255, 0, 0),
               size: Tuple[int, int] = (630, 630),
               file_name: str = default_file_name):
    width, h = size

    r = int(np.min(size) / 2.1)
    i = np.arange(num_p)
    ps = np.array([width / 2 + r * np.cos(2 * np.pi * i / num_p - np.pi / 2),
                   h / 2 + r * np.sin(2 * np.pi * i / num_p - np.pi / 2)]).transpose()
    if num_p % 2 == 0:
        ds = 2 * np.sin(np.pi*np.arange(num_p/2+1)/num_p)
    else:
        ds = 2 * np.sin(np.pi * np.arange(num_p / 2) / num_p)
    dwg = svgwrite.Drawing(filename=file_name, size=(width, h))
    arrow = create_arrow_marker_sumner(dwg=dwg, s=5*np.log10(num_p)-2)
    dwg.add(dwg.circle(center=(width/2, h/2), r=r,
                       stroke=svgwrite.rgb(100, 100, 100, '%'),
                       stroke_width=2, fill='none'))
    DRAWN = [0] * num_p
    # count loops
    n = 0
    dwg.add(dwg.circle(center=ps[0], r=r/(50 * np.log10(num_p)), fill='red'))
    for i in range(0, num_p):
        dwg.add(dwg.circle(center=ps[i], r=r/(50 * np.log10(num_p)), fill='red'))
        if DRAWN[i] == 1:
            continue
        # print(f"START FROM {i}")
        p0 = i
        p1 = (p0 * mult) % num_p
        n += 1
        while True:
            if DRAWN[p0] == 1:
                break
            # print(f"{p0} -> {p1}")
            if color_mode == 'Single':
                c = (255, 0, 0)
            elif color_mode == 'Length':
                l = ds[map_ds_idx(np.abs(p0-p1), num_p)]
                c = rainbow_scale(l, min_v=0, max_v=2)
            elif color_mode == 'Loop':
                c = loop_colors[n % len(loop_colors)]
            line = dwg.line(ps[p0], ps[p1], stroke=svgwrite.rgb(*c, '%'),
                            stroke_width=5 * w(num_p),
                            marker_end=arrow.get_funciri())
            dwg.add(line)
            DRAWN[p0] = 1
            p0 = p1
            p1 = (p0 * mult) % num_p
        # print(f"CIRCLE CLOSED")
        # UNCOMMENT THE FOLLOWING LINE TO CREATE A "vortex.svg" FILE
        #dwg.save()
    return dwg


def count_loops(num_p: int,
                mult: int):
    i = np.arange(num_p)
    ps = np.array([np.cos(2 * np.pi * i / num_p - np.pi / 2),
                   np.sin(2 * np.pi * i / num_p - np.pi / 2)]).transpose()

    DRAWN = [0] * num_p
    # count loops
    n = 0
    for i in range(0, num_p):
        if DRAWN[i] == 1:
            continue
        # print(f"START FROM {i}")
        p0 = i
        p1 = (p0 * mult) % num_p
        n += 1
        while True:
            if DRAWN[p0] == 1:
                break
            DRAWN[p0] = 1
            p0 = p1
            p1 = (p0 * mult) % num_p
        # print(f"CIRCLE CLOSED")
    return f'Total Number of Loops : {n}'


num_p = widgets.IntInput(name='Nodes', step=1, value=9)
mult = widgets.IntInput(name='Multiplier', step=1, value=2)
color = widgets.Select(name='ColorMode', options=['Length', 'Loop', 'Single'])
# file_download = pn.widgets.FileDownload(file=default_file_name,
#                                         button_type='success',
#                                         auto=False,
#                                         embed=False,
#                                         name="Download image as SVG")

size = (630, 630)

loop_colors = [(166, 206, 227), (31, 120, 180), (178, 223, 138), (51, 160, 44),
               (251, 154, 153), (227, 26, 28), (253, 191, 111), (255, 127, 0),
               (202, 178, 214), (106, 61, 154), (255, 255, 153), (177, 89, 40)]


@pn.depends(num_p.param.value, mult.param.value, color.param.value)
def get_svg(num_p, mult, color):
    return create_svg(num_p=num_p, mult=mult, color_mode=color, size=(630, 630))


@pn.depends(num_p.param.value, mult.param.value)
def get_loops(num_p, mult):
    return count_loops(num_p=num_p, mult=mult)


pn.template.FastListTemplate(
    site="Panel",
    title="Tesla Vortex",
    sidebar=[num_p, mult, color],
    main=[
        get_loops,
        get_svg
    ],
    theme="dark"
).servable()
