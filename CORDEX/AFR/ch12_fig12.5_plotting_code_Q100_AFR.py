import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import pandas as pd
import matplotlib
matplotlib.use('Agg')
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
path.append("my_lib/")
path.append("libraries/lib/python3.8/site-packages/")
import descartes
import geoplot as gplt
import colors as col
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
        'size'   : 11}

matplotlib.rc('font', **font)
SMALL_SIZE = 13
MEDIUM_SIZE = 16
BIGGER_SIZE = 19
matplotlib.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
matplotlib.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
matplotlib.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
matplotlib.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
matplotlib.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
matplotlib.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
matplotlib.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
RendererBase.new_gc = types.MethodType(custom_new_gc, RendererBase)

dim_text_box=17
direc=r"/home/netapp-clima/users/fdi_sant/script/CHYM/chym-esp/output/"
rivers_fp= [
"AFR_Q100_rcp85_2041-2060_change_divdra_timmean_wstk.drainage_net_ths50.csv"]
AR6 = gpd.read_file('../../create_MASKS/AR6/IPCC-WGI-reference-regions-v4_shapefile/IPCC-WGI-reference-regions-v4.shp')

id_y = [0,1,0,1,0,1,2,3,0,1,2,3]
id_x = [0,0,1,1,1,1,1,1,2,2,2,2]
tname = ["rcp85 far"]
cname = ["AFR","CMIP6","CORDEX"]
letters = ["(a)","(b)","(c)","(d)","(e)","(f)","(g)","(h)","(i)","(j)","(k)","(l)"]

dirmask='/home/clima-archive/fdi_sant/SCRIPT/PlottingSuite/python/Experiments/Mask_MED-CEU-NEU/'
filemask='Mask_MED-CEU-NEU_CORDEX006_tomask.nc'
filemaskin='Mask_MED-CEU-NEU_CORDEX006.nc'


data = xr.open_dataset('AFR-forMAP-final_maskout.nc')
mask = data['Band1']
lons = data['lon']
lats = data['lat']
bounds = np.array([-0.20,-0.10,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.10,0.20])
norm = mpl.colors.BoundaryNorm(bounds, ncolors=10)
ticks = np.array([-0.20,-0.10,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.10,0.20])

data_proj = ccrs.PlateCarree()
map_proj = ccrs.PlateCarree()
lines_proj = ccrs.Geodetic()
dpi = 600
fig, axes = plt.subplots(ncols=1,nrows=1,subplot_kw={'projection': map_proj},dpi=dpi,figsize=(8, 8))
h = 63760

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
       lwidths = np.log10(np.array(rivers1[:].drainage_net.values))/2.
       lwidths = np.where( lwidths < .3, .3, lwidths )
       lwidths = np.where( lwidths > .3, .3, lwidths )
       mapper = cm.ScalarMappable(norm=norm, cmap=col.prec_div_disc12)
       colors = mapper.to_rgba(np.array([rivers1[:].q100ch.values]))
       colors = [tuple(x) for x in colors[0,:,:].tolist()]
       lc = LineCollection(segments, linewidths=lwidths,color=colors, transform=lines_proj,zorder=5)
       axes.add_collection(lc)

h=10743
rivers_fp= [
"MED_for_AFR_divdra.drainage_net_ths50.csv"]
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
       lwidths = np.log10(np.array(rivers1[:].drainage_net.values))/2.
       lwidths = np.where( lwidths < .3, .3, lwidths )
       lwidths = np.where( lwidths > .3, .3, lwidths )
       mapper = cm.ScalarMappable(norm=norm, cmap=col.prec_div_disc12)
       colors = mapper.to_rgba(np.array([rivers1[:].q100ch.values]))
       colors = [tuple(x) for x in colors[0,:,:].tolist()]
       lc = LineCollection(segments, linewidths=lwidths,color=colors, transform=lines_proj,zorder=7)
       axes.add_collection(lc)

AR6[AR6['Acronym'].isin(['MED','SAH','WAF','CAF','NEAF','SEAF','WSAF','ESAF','MDG'])].plot(ax=axes,zorder=100,transform=lines_proj,edgecolor='black',facecolor="none",lw=1)
axes.text(19.2, 35.47, 'MED',
         horizontalalignment='center',
         verticalalignment='center',
         transform=lines_proj,zorder=101,size=dim_text_box,weight=650)
axes.text(-20.00, 24.90, 'SAH',
         horizontalalignment='center',
         verticalalignment='center',
         transform=lines_proj,zorder=101,size=dim_text_box,weight=650)
axes.text(2.5, 3.5, 'WAF',
         horizontalalignment='center',
         verticalalignment='center',
         transform=lines_proj,zorder=101,size=dim_text_box,weight=650)
axes.text(6.44,-7.46, 'CAF',
         horizontalalignment='center',
         verticalalignment='center',
         transform=lines_proj,zorder=101,size=dim_text_box,weight=650)
axes.text(54.05, 12.92, 'NEAF',
         horizontalalignment='center',
         verticalalignment='center',
         transform=lines_proj,zorder=101,size=dim_text_box,weight=650)
axes.text(48.9,-4.75, 'SEAF',
         horizontalalignment='center',
         verticalalignment='center',
         transform=lines_proj,zorder=101,size=dim_text_box,weight=650)
axes.text(11.32, -30.47, 'WSAF',
         horizontalalignment='center',
         verticalalignment='center',
         transform=lines_proj,zorder=101,size=dim_text_box,weight=650)
axes.text(36.96, -30.07, 'ESAF',
         horizontalalignment='center',
         verticalalignment='center',
         transform=lines_proj,zorder=101,size=dim_text_box,weight=650)
axes.text(50, -24.99, 'MDG',
         horizontalalignment='center',
         verticalalignment='center',
         transform=lines_proj,zorder=101,size=dim_text_box,weight=650)
for ii in range(0,1):
   axes.set_extent([-25., 60, -40, 47],map_proj)
   axes.pcolormesh(lons,lats,mask,alpha = 1., transform= data_proj,zorder=6,cmap=col.formask,norm=norm)
   ocean_50m = cfeature.NaturalEarthFeature('physical', 'ocean', '50m',
                                        edgecolor='face', facecolor=[ 1., 1., 1. ])
   axes.add_feature(ocean_50m,zorder=22)
   lakes_50m = cfeature.NaturalEarthFeature('physical', 'lakes', '110m',linewidth=0.4,
                                         edgecolor='black', facecolor=[ 1, 1, 1 ])
   axes.add_feature(lakes_50m,zorder=22)
   axes.coastlines(resolution='50m',linewidth=0.4,zorder=30)
divider = axes_grid1.make_axes_locatable(axes)
cax = divider.new_vertical(size="5%", pad=0.22, axes_class=plt.Axes, pack_start=True)
fig.add_axes(cax)
cb3 = mpl.colorbar.ColorbarBase(cax,norm=norm,cmap=col.prec_div_disc12,ticks=ticks,orientation='horizontal',extend='both',extendfrac=0.09)
cb3.ax.set_xticklabels(ticks[::1],rotation=30)
fig.subplots_adjust(top=0.895)
fig.suptitle('100-yr return period stream flow by 2050\n CORDEX RCP8.5', fontsize=18, linespacing=1.5)
outfp = r"AFR_Q100_MED_nohatching_600dpi_all0_3_colorbar_divdra.png"
plt.savefig(outfp, dpi=dpi)