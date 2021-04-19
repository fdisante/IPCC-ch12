import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import pandas as pd
import matplotlib
matplotlib.use('Agg')
#matplotlib.use('pdf')
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import matplotlib as mpl
from shapely.geometry import Point, LineString
from matplotlib.backend_bases import GraphicsContextBase, RendererBase
import types
from matplotlib.colors import ListedColormap
from matplotlib.colors import BoundaryNorm
from matplotlib import cm
import matplotlib
import matplotlib.colors as mcolors
from sys import path
path.append("../my_lib/")
path.append("../libraries/lib/python3.8/site-packages/")
import descartes
import geoplot as gplt
import colors as col
from matplotlib.transforms import offset_copy
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from matplotlib.transforms import offset_copy
from mpl_toolkits import axes_grid1



class GC(GraphicsContextBase):
    def __init__(self):
        super().__init__()
        self._capstyle = 'round'

def custom_new_gc(self):
    return GC()
font = {'family' : 'arial',
        'weight' : 'normal',
        'size'   : 24}

matplotlib.rc('font', **font)
SMALL_SIZE = 24
MEDIUM_SIZE = 30
BIGGER_SIZE = 36
matplotlib.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
matplotlib.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
matplotlib.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
matplotlib.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
matplotlib.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
matplotlib.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
matplotlib.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
RendererBase.new_gc = types.MethodType(custom_new_gc, RendererBase)
dim_text_box=34

direc=r"/home/netapp-clima/users/fdi_sant/script/CHYM/chym-esp/output/"
rivers_fp= [
"WAS_for_ASIA_IPCC_divdra.drainage_net_ths50.csv"]

fname = 'Regions_for_ASIA.shp'

id_y = [0,1,0,1,0,1,2,3,0,1,2,3]
id_x = [0,0,1,1,1,1,1,1,2,2,2,2]
tname = ["rcp85 far"]
cname = ["EUR","CMIP6","CORDEX"]
letters = ["(a)","(b)","(c)","(d)","(e)","(f)","(g)","(h)","(i)","(j)","(k)","(l)"]

dirmask='/home/clima-archive/fdi_sant/SCRIPT/PlottingSuite/python/Experiments/Mask_MED-CEU-NEU/'
filemask='Mask_MED-CEU-NEU_CORDEX006_tomask.nc'
filemaskin='Mask_MED-CEU-NEU_CORDEX006.nc'

bounds = np.array([-0.20,-0.10,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.10,0.20])
norm = mpl.colors.BoundaryNorm(bounds, ncolors=10)
ticks = np.array([-0.20,-0.10,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.10,0.20])


data_proj = ccrs.PlateCarree()
map_proj = ccrs.PlateCarree()
lines_proj = ccrs.Geodetic()
dpi = 600
fig = plt.figure(dpi=dpi,figsize=(15, 10))
axes = plt.axes(projection=ccrs.PlateCarree())
h = 49462

for ii in range(0,1):
   print(ii)
   print(direc+rivers_fp[ii])
   rivers = pd.read_csv(direc+rivers_fp[ii])
   rivers["line_id"] = pd.to_numeric(rivers["line_id"])
   rivers["q100ch"] = pd.to_numeric(rivers["q100ch"])
   rivers1 = rivers.loc[rivers.line_id.values == 2]
   for j in range(h,0,-1):
     rivers1 = rivers.loc[rivers.line_id.values == j]
     maxc = rivers1.shape[0]-1
     if j%100 == 0:
       print(j)
     if maxc > 0:
       points = np.array([rivers1[:].x.values,rivers1[:].y.values]).T.reshape(-1, 1, 2)
       segments = np.concatenate([points[:-1], points[1:]], axis=1)
       lwidths = np.log10(np.array(rivers1[:].drainage_net.values))/3.
       lwidths = np.where( lwidths < 0.3, 0.3, lwidths )
       lwidths = np.where( lwidths > 0.3, 0.3, lwidths )
       mapper = cm.ScalarMappable(norm=norm, cmap=col.prec_div_disc12)
       colors = mapper.to_rgba(np.array([rivers1[:].q100ch.values]))
       colors = [tuple(x) for x in colors[0,:,:].tolist()]
       lc = LineCollection(segments, linewidths=lwidths,color=colors, zorder=5)
       axes.add_collection(lc)

rivers_fp= [
"EAS_for_ASIA_IPCC_divdra.drainage_net_ths50.csv"]
h = 43264

for ii in range(0,1):
   print(ii)
   print(direc+rivers_fp[ii])
   rivers = pd.read_csv(direc+rivers_fp[ii])
   rivers["line_id"] = pd.to_numeric(rivers["line_id"])
   rivers["q100ch"] = pd.to_numeric(rivers["q100ch"])
   rivers1 = rivers.loc[rivers.line_id.values == 2]
   for j in range(h,0,-1):
     rivers1 = rivers.loc[rivers.line_id.values == j]
     maxc = rivers1.shape[0]-1
     if j%100 == 0:
       print(j)
     if maxc > 0:
       points = np.array([rivers1[:].x.values,rivers1[:].y.values]).T.reshape(-1, 1, 2)
       segments = np.concatenate([points[:-1], points[1:]], axis=1)
       lwidths = np.log10(np.array(rivers1[:].drainage_net.values))/3.
       lwidths = np.where( lwidths < 0.3, 0.3, lwidths )
       lwidths = np.where( lwidths > 0.3, 0.3, lwidths )
       mapper = cm.ScalarMappable(norm=norm, cmap=col.prec_div_disc12)
       colors = mapper.to_rgba(np.array([rivers1[:].q100ch.values]))
       colors = [tuple(x) for x in colors[0,:,:].tolist()]
       lc = LineCollection(segments, linewidths=lwidths,color=colors, zorder=5)
       axes.add_collection(lc)

rivers_fp= [
"SEA_for_ASIA_IPCC_divdra.drainage_net_ths50.csv"]
h = 50
h = 6662

for ii in range(0,1):
   print(ii)
   print(direc+rivers_fp[ii])
   rivers = pd.read_csv(direc+rivers_fp[ii])
   rivers["line_id"] = pd.to_numeric(rivers["line_id"])
   rivers["q100ch"] = pd.to_numeric(rivers["q100ch"])
   rivers1 = rivers.loc[rivers.line_id.values == 2]
   for j in range(h,0,-1):      
     rivers1 = rivers.loc[rivers.line_id.values == j]
     maxc = rivers1.shape[0]-1
     if j%100 == 0:
       print(j)
     if maxc > 0:
       points = np.array([rivers1[:].x.values,rivers1[:].y.values]).T.reshape(-1, 1, 2)
       segments = np.concatenate([points[:-1], points[1:]], axis=1)
       lwidths = np.log10(np.array(rivers1[:].drainage_net.values))/3.
       lwidths = np.where( lwidths < 0.3, 0.3, lwidths )
       lwidths = np.where( lwidths > 0.3, 0.3, lwidths )
       mapper = cm.ScalarMappable(norm=norm, cmap=col.prec_div_disc12)
       colors = mapper.to_rgba(np.array([rivers1[:].q100ch.values]))
       colors = [tuple(x) for x in colors[0,:,:].tolist()]
       lc = LineCollection(segments, linewidths=lwidths,color=colors, zorder=5)
       axes.add_collection(lc)
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.PlateCarree(), facecolor='none',edgecolor='black',lw=2)
axes.add_feature(shape_feature,zorder=100)

axes.text(58.2, 13.3, 'ARP',
         horizontalalignment='center',
         verticalalignment='center',
         zorder=101,size=dim_text_box,weight=650)
axes.text(74., 5.4 , 'SAS',
         horizontalalignment='center',
         verticalalignment='center',
         zorder=101,size=dim_text_box,weight=650)
axes.text(71.2, 33.2, 'TIB',
         horizontalalignment='center',
         verticalalignment='center',
         zorder=101,size=dim_text_box,weight=650)
axes.text(92.6, 47.8, 'ECA',
         horizontalalignment='center',
         verticalalignment='center',
         zorder=101,size=dim_text_box,weight=650)
axes.text(127.5, 27, 'EAS',
         horizontalalignment='center',
         verticalalignment='center',
         zorder=101,size=dim_text_box,weight=650)
axes.text(114.3, 12.5, 'SEA',
         horizontalalignment='center',
         verticalalignment='center',
         zorder=101,size=dim_text_box,weight=650)
for ii in range(0,1):
    axes.set_extent([20, 180, -20, 80],map_proj)
    ocean_50m = cfeature.NaturalEarthFeature('physical', 'ocean', '50m',
                                         edgecolor='face', facecolor=[ 1, 1, 1 ])
    axes.add_feature(ocean_50m,zorder=22)
    lakes_50m = cfeature.NaturalEarthFeature('physical', 'lakes', '110m',linewidth=0.4,
                                         edgecolor='black', facecolor=[ 1, 1, 1 ])
    axes.add_feature(lakes_50m,zorder=22)
    axes.coastlines(resolution='50m',linewidth=1.,zorder=30)
divider = axes_grid1.make_axes_locatable(axes)
cax = divider.new_vertical(size="7.5%", pad=0.24, axes_class=plt.Axes, pack_start=True)
fig.add_axes(cax)
cb3 = mpl.colorbar.ColorbarBase(cax,norm=norm,cmap=col.prec_div_disc12,ticks=ticks,orientation='horizontal',extend='both',extendfrac=0.09)
cb3.ax.set_xticklabels(ticks[::1],rotation=30)
fig.subplots_adjust(top=0.855)
fig.suptitle('100-yr return period stream flow by 2050\n CORDEX RCP8.5', fontsize=34, linespacing=1.5)
outfp = r"ASIA_Q100_nohatching_colorbar_divdra.png"
plt.savefig(outfp, dpi=dpi)
