#!/usr/bin/python

# Created by: J. G. Fernandez-Trincado
# Last update: 2015/01/07

# This program was created to convert .fits image to .ascii file using "Pyfits" from Python
# 1. input_name = is the list of images .fits
# 2. The parameter "CRVAL1" from FITS header is the starting wavelength
# 3. The parameter "CDELT1" from FITS header is the step in wavelength 
# 4. This program generate "XXXXXXX.fits.dat"

import numpy as np
import scipy as sc
import pyfits 

input_ = sc.genfromtxt('input_name',dtype=str)

for k in np.arange(len(input_)):

	dat = pyfits.open(input_[k])
	
	NL       = len(dat[0].data)
	starting = float(dat[0].header['CRVAL1'])
	step     = float(dat[0].header['CDELT1'])
	
	Y = dat[0].data
	
	fil_ = open(input_[k]+'.dat','a')
	
	for i in np.arange(NL): 
	
		XX = starting + i*step
	
		fil_.write(str(XX)+' '+str(Y[i])+' '+'\n')
		
	fil_.close()





