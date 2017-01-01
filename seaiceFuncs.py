
############################################################## 
# Date: 11/11/16
# Name: seaiceFuncs.py
# Author: Alek Petty
# Description: Various sea ice conc functions
# Input requirements: ice conc data


import numpy as np
from pylab import *
import numpy.ma as ma
from glob import glob



def getMeanConcDates(dataPath, poleStr='A', alg=0, date1='20151220', date2='20160105', lonlat=0, mean=0):
	if (alg==0):
		team = 'NASA_TEAM'
		team_s = 'nt'
		header = 300
		datatype='uint8'
		scale_factor=250.
	if (alg==1):
		team = 'BOOTSTRAP'
		team_s = 'bt'
		header = 0
		datatype='<i2'
		scale_factor=1000.

	if (poleStr=='AA'):
		col=316	
		row=332
		pole='ANTARCTIC'
	else:
		col=304	
		row=448
		pole='ARCTIC'
		
	print poleStr
	year = date1[0:4]
	print year
	day=0
	if (int(year)>2015):
		files = glob(dataPath+'/ICE_CONC/'+team+'/'+pole+'/NRT/'+team_s+'_'+'*.bin')	
	else:
		files = glob(dataPath+'/ICE_CONC/'+team+'/'+pole+'/daily/'+year+'/'+team_s+'_'+'*.bin')

	dates=[file.split('/')[-1][3:11] for file in files]
	#print dates
	idx1=where(array(dates)==date1)[0][0]
	idx2=where(array(dates)==date2)[0][0]
	files=files[idx1:idx2+1]
	ice_conc = ma.masked_all((size(files), row, col))

	for x in xrange(size(files)):
		fd = open(files[x], 'r')
		data = fromfile(file=fd, dtype=datatype)
		data = data[header:]
		#FIRST 300 FILES ARE HEADER INFO
		ice_conc[x] = reshape(data, [row, col])
		
	#divide by 250 to express in concentration
	ice_conc = ice_conc/scale_factor
	#GREATER THAN 250 is mask/land etc
	ice_conc = ma.masked_where(ice_conc>1., ice_conc)
	#ice_conc = ma.masked_where(ice_conc<0.15, ice_conc)
	if (mean==1):
		ice_conc=ma.mean(ice_conc, axis=0)

	if (lonlat==1):
		if (poleStr=='A'):
			psStr = 'psn'
		else:
			psStr = 'pss'

		flat = open(dataPath+'OTHER/'+psStr+'25lats_v3.dat', 'rb')
		flon = open(dataPath+'OTHER/'+psStr+'25lons_v3.dat', 'rb')
		lats = reshape(fromfile(file=flat, dtype='<i4')/100000., [row, col])
		lons = reshape(fromfile(file=flon, dtype='<i4')/100000., [row, col])
		return ice_conc, lons, lats
	else:
		return ice_conc
	