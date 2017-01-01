############################################################## 
# Date: 20/05/16
# Name: plot_atm_dms.py
# Author: Alek Petty
# Description: Script to plot ATM overlaid on a DMS image
# Input requirements: DMS image and ATM data for specific case studies

import matplotlib
matplotlib.use("AGG")
import numpy as np
from pylab import *
import numpy.ma as ma
from skimage.morphology import watershed, disk
from skimage.filters import rank
from mpl_toolkits.basemap import Basemap
from matplotlib import rc
import mpl_toolkits.basemap.pyproj as pyproj 
from glob import glob
import os
from osgeo import osr, gdal
from scipy import ndimage

#may need this if reading in ATM data after 2013 (hdf5 format)
#import h5py


rcParams['axes.labelsize'] =8
rcParams['xtick.labelsize']=8
rcParams['ytick.labelsize']=8
rcParams['legend.fontsize']=8
rcParams['font.size']=8
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})


rawdatapath = '../../../DATA/'
imagePath = rawdatapath+'IMAGERY/P1/'
figpath='./Figures/'

#norm = ro.MidpointNormalize(midpoint=0)

m=pyproj.Proj("+init=EPSG:3413")


year = int(date[0:4])
image_path = glob(imagePath+'P1.tif')

geo = gdal.Open(image_path[0]) 
band1 = geo.GetRasterBand(1)
band2 = geo.GetRasterBand(2)
band3 = geo.GetRasterBand(3)
red = band1.ReadAsArray()
green = band2.ReadAsArray()
blue = band3.ReadAsArray()

dms = (0.299*red + 0.587*green + 0.114*blue)
#normalize
dms=dms/np.amax(dms)
#dms = ma.masked_where(dms<1, dms)
#print '1'
#denoised = rank.median(dms, disk(2))
print '2'
markers = rank.gradient(dms, disk(5)) < 10
# disk(5) is used here to get a more smooth image
print '3'
markers = ndimage.label(markers)[0]
print '4'
#gradient = rank.gradient(dms, disk(2))
print '5'
labels = watershed(dms, markers)
print '6'

trans = geo.GetGeoTransform()
width = geo.RasterXSize
height = geo.RasterYSize

x1 = np.linspace(trans[0], trans[0] + width*trans[1] + height*trans[2], width)
y1 = np.linspace(trans[3], trans[3] + width*trans[4] + height*trans[5], height)
xT, yT = meshgrid(x1, y1)


lonDMS, latDMS = m(xT[0, 0], yT[0, 0], inverse=True)
lonDMS_str = '%.2f' %lonDMS
latDMS_str = '%.2f' %latDMS

#(T, threshImage) = cv2.threshold(src, thresh, maxval, type)

#--------------------------------------------------
sizex = np.amax(xT) - np.amin(xT)
sizey = np.amax(yT) - np.amin(yT)
ratio = sizey/sizex

res=1
textwidth=4
fig = figure(figsize=(textwidth,textwidth*1.25*ratio))
ax=gca()
im2 = pcolormesh(xT[::res, ::res], yT[::res, ::res], dms[::res, ::res], vmin = 0, vmax = 255, cmap = cm.gist_gray, rasterized=True)
subplots_adjust(bottom=0.09, left=0.11, top = 0.94, right=0.99, hspace=0.22)
savefig(figpath+'dms.png', dpi=300)
close(fig)

# display results
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 8), sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
ax = axes.ravel()

ax[0].imshow(dms, cmap=plt.cm.gray, interpolation='nearest')
ax[0].set_title("Original")

ax[1].imshow(dms, cmap=plt.cm.spectral, interpolation='nearest')
ax[1].set_title("Local Gradient")

ax[2].imshow(markers, cmap=plt.cm.spectral, interpolation='nearest')
ax[2].set_title("Markers")

ax[3].imshow(dms, cmap=plt.cm.gray, interpolation='nearest')
ax[3].imshow(labels, cmap=plt.cm.spectral, interpolation='nearest', alpha=.7)
ax[3].set_title("Segmented")

savefig(figpath+'dms_watershed.png', dpi=300)




