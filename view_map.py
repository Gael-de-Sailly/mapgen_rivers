#!/usr/bin/env python3

import numpy as np
import zlib
import matplotlib.colors as mcl
import matplotlib.pyplot as plt

has_matplotlib = True
try:
    import matplotlib.colors as mcl
    import matplotlib.pyplot as plt
    try:
        import colorcet as cc
        cmap1 = cc.cm.CET_L11
        cmap2 = cc.cm.CET_L12
    except ImportError: # No module colorcet
        import matplotlib.cm as cm
        cmap1 = cm.summer
        cmap2 = cm.Blues
except ImportError: # No module matplotlib
    has_matplotlib = False


def view_map(dem, lakes, scale):
    if not has_matplotlib:
        return
    lakes_sea = np.maximum(lakes, 0)
    water = np.maximum(lakes_sea - dem, 0)
    max_elev = lakes_sea.max()
    max_depth = water.max()

    ls = mcl.LightSource(azdeg=315, altdeg=45)
    rgb = ls.shade(lakes_sea, cmap=cmap1, vert_exag=1/scale, blend_mode='soft', vmin=0, vmax=max_elev)

    (X, Y) = dem.shape
    extent = (0, Y*scale, 0, X*scale)
    plt.imshow(np.flipud(rgb), extent=extent, interpolation='antialiased')
    alpha = (water > 0).astype('u1')
    plt.imshow(np.flipud(water), alpha=np.flipud(alpha), cmap=cmap2, extent=extent, vmin=0, vmax=max_depth, interpolation='antialiased')

    sm1 = plt.cm.ScalarMappable(cmap=cmap1, norm=plt.Normalize(vmin=0, vmax=max_elev))
    plt.colorbar(sm1).set_label('Altitude')

    sm2 = plt.cm.ScalarMappable(cmap=cmap2, norm=plt.Normalize(vmin=0, vmax=max_depth))
    plt.colorbar(sm2).set_label('Profondeur d\'eau')

    plt.show()

def map_stats(dem, lake_dem, scale):
    surface = dem.size

    continent = lake_dem >= 0
    continent_surface = continent.sum()

    lake = continent & (lake_dem>dem)
    lake_surface = lake.sum()

    print('---   General    ---')
    print('Grid size:    {:5d}x{:5d}'.format(dem.shape[0], dem.shape[1]))
    print('Map size:     {:5d}x{:5d}'.format(int(dem.shape[0]*scale), int(dem.shape[1]*scale)))
    print()
    print('---   Surfaces   ---')
    print('Continents:        {:6.2%}'.format(continent_surface/surface))
    print('-> Ground:         {:6.2%}'.format((continent_surface-lake_surface)/surface))
    print('-> Lakes:          {:6.2%}'.format(lake_surface/surface))
    print('Oceans:            {:6.2%}'.format(1-continent_surface/surface))
    print()
    print('---  Elevations  ---')
    print('Mean elevation:      {:4.0f}'.format(dem.mean()))
    print('Mean ocean depth:    {:4.0f}'.format((dem*~continent).sum()/(surface-continent_surface)))
    print('Mean continent elev: {:4.0f}'.format((dem*continent).sum()/continent_surface))
    print('Lowest elevation:    {:4.0f}'.format(dem.min()))
    print('Highest elevation:   {:4.0f}'.format(dem.max()))

if __name__ == "__main__":
    import sys
    import os

    scale = 1
    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])
    if len(sys.argv) > 2:
        scale = int(sys.argv[2])

    def load_map(name, dtype, shape):
        dtype = np.dtype(dtype)
        with open(name, 'rb') as f:
            data = f.read()
        if len(data) < shape[0]*shape[1]*dtype.itemsize:
            data = zlib.decompress(data)
        return np.frombuffer(data, dtype=dtype).reshape(shape)

    shape = np.loadtxt('size', dtype='u4')
    dem = load_map('dem', '>i2', shape)
    lakes = load_map('lakes', '>i2', shape)

    map_stats(dem, lakes, scale)
    view_map(dem, lakes, scale)
