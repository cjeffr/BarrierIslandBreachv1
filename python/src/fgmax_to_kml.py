from clawpack.geoclaw import fgmax_tools, geoplot
from simplekml import (Kml, OverlayXY, ScreenXY, Units, RotationXY,
                       AltitudeMode, Camera)
import numpy as np
import matplotlib.pyplot as plt
import os

def make_kml(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat,
             figs, colorbar=None, **kw):
    """
    TODO: LatLon bbox, list of figs, optional colorbar figure,
    and several simplekml kw...
    """

    kml = Kml()
    altitude = kw.pop('altitude', 1.05e4)
    roll = kw.pop('roll', 0)
    tilt = kw.pop('tilt', 0)
    altitudemode = kw.pop('altitudemode', AltitudeMode.relativetoground)
    camera = Camera(latitude=np.mean([urcrnrlat, llcrnrlat]),
                    longitude=np.mean([urcrnrlon, llcrnrlon]),
                    altitude=altitude, roll=roll, tilt=tilt,
                    altitudemode=altitudemode)

    kml.document.camera = camera
    draworder = 0
    for fig in figs:  # NOTE: Overlays are limited to the same bbox.
        draworder += 1
        ground = kml.newgroundoverlay(name='GroundOverlay')
        ground.draworder = draworder
        ground.visibility = kw.pop('visibility', 1)
        ground.name = kw.pop('name', 'overlay')
        ground.color = kw.pop('color', '9effffff')
        ground.atomauthor = kw.pop('author', 'ocefpaf')
        ground.latlonbox.rotation = kw.pop('rotation', 0)
        ground.description = kw.pop('description', 'Matplotlib figure')
        ground.gxaltitudemode = kw.pop('gxaltitudemode',
                                       'clampToSeaFloor')
        ground.icon.href = fig
        ground.latlonbox.east = llcrnrlon
        ground.latlonbox.south = llcrnrlat
        ground.latlonbox.north = urcrnrlat
        ground.latlonbox.west = urcrnrlon

    if colorbar:  # Options for colorbar are hard-coded (to avoid a big mess).
        screen = kml.newscreenoverlay(name='ScreenOverlay')
        screen.icon.href = colorbar
        screen.overlayxy = OverlayXY(x=0, y=0,
                                     xunits=Units.fraction,
                                     yunits=Units.fraction)
        screen.screenxy = ScreenXY(x=0.65, y=0.175,
                                   xunits=Units.fraction,
                                   yunits=Units.fraction)
        screen.rotationXY = RotationXY(x=0.5, y=0.5,
                                       xunits=Units.fraction,
                                       yunits=Units.fraction)
        screen.size.x = 0
        screen.size.y = 0
        screen.size.xunits = Units.fraction
        screen.size.yunits = Units.fraction
        screen.visibility = 1

    kmzfile = kw.pop('kmzfile', 'overlay.kmz')
    kml.savekmz(kmzfile)




def gearth_fig(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, pixels=1024):
    """Return a Matplotlib `fig` and `ax` handles for a Google-Earth Image."""
    aspect = np.cos(np.mean([llcrnrlat, urcrnrlat]) * np.pi / 180.0)
    xsize = np.ptp([urcrnrlon, llcrnrlon]) * aspect
    ysize = np.ptp([urcrnrlat, llcrnrlat])
    aspect = ysize / xsize

    if aspect > 1.0:
        figsize = (10.0 / aspect, 10.0)
    else:
        figsize = (10.0, 10.0 * aspect)

    if False:
        plt.ioff()  # Make `True` to prevent the KML components from poping-up.
    fig = plt.figure(figsize=figsize,
                     frameon=False,
                     dpi=pixels // 10)
    # KML friendly image.  If using basemap try: `fix_aspect=False`.
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(llcrnrlon, urcrnrlon)
    ax.set_ylim(llcrnrlat, urcrnrlat)
    return fig, ax




def plot_fgmax_grid(fname, fgno, xl, xu, yl, yu):
    """Plots the fg_max data using clawpack and creates a figure in the _plots directory"""
    xlower = xl
    xupper = xu
    ylower = yl
    yupper = yu

    fg = fgmax_tools.FGmaxGrid()
    fg.read_fgmax_grids_data(3)
    fg.read_output(fgno=fgno)

    clines_zeta = [0.01] + list(np.linspace(0.25, 6, 24))
    colors = geoplot.discrete_cmap_1(clines_zeta)
    zeta = np.where(fg.B > 0, fg.h, fg.h + fg.B)  # surface elevation in ocean

    fig, ax = gearth_fig(llcrnrlon=xlower, llcrnrlat=ylower, urcrnrlon=xupper, urcrnrlat=yupper, pixels=1024)

    ax.contourf(fg.X, fg.Y, zeta, clines_zeta, colors=colors, alpha=.90)
    ax.contour(fg.X, fg.Y, fg.B, [0.], colors='k')  # coastline
    # fix axes:
    ax.ticklabel_format(style='plain', useOffset=False)
    plt.xticks(rotation=20)
    plt.gca().set_aspect(1. / np.cos(fg.Y.mean() * np.pi / 180.))
    plt.title("Maximum amplitude")
    cs = ax.contourf(fg.X, fg.Y, zeta, clines_zeta, colors=colors)
    return (cs)

# CHANGE STUFF HERE!!!!!!!

xl = -72.615
xu = -72.375
yl = 40.80
yu = 40.87
name = '/mnt/c/storm/moriches/mor/_output/fgmax0003.txt'
output_name = 'moriches_max_a.png'
scale_bar_name = 'scale.png'
kmz_name = 'moriches.kmz'
kmz_title = 'Moriches no breach'
# STOP CHANGING STUFF HERE


os.chdir('/mnt/c/storm/moriches/mor/')
cs = plot_fgmax_grid(name,3, xl, xu, yl, yu)
plotdir = '/mnt/c/storm/moriches/mor/_plots'
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)
oname = os.path.join(plotdir, output_name)
plt.savefig(oname, transparent=True)
print ("Created ",oname)

fig1 = plt.figure(figsize=(2.0, 11.), facecolor=None, frameon=False)
ax1 = fig1.add_axes([0.0, 0.0, .2, .9])
cb = fig1.colorbar(cs, cax=ax1)
cb.set_label('Maximum Wave Amplitude [m]', rotation=-90, color = 'k', labelpad=50, size=20)
ax1.tick_params(labelsize=20)
fig1.savefig(scale_bar_name, transparent=False, format='png', bbox_inches='tight')


make_kml(llcrnrlon=xl, llcrnrlat=yl,
         urcrnrlon=xu, urcrnrlat=yu,
         figs=[oname], colorbar=scale_bar_name,
         kmzfile=kmz_name, name=kmz_title)