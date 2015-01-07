#!/usr/bin/python
# Copyright (c) 2014 J. G. Fern\'andez-Trincado
# Cosmicray.py is open source and free program developed and maintained by J. G. Fern\'andez-Trincado.
#__________________________________________________________________________________________________________________________
# **************   If you have used this code in your research, please consider acknowledging this program   **************
# The standard acknowledgement:
# Funding for Cosmicray.py has been provided by Centre Centre national d'\'etudes spatiale (CNES) through
# Phd grant 0101973 and UTINAM Institute of the Universit\'e de Franche-Comte, supported by the Region de Franche-Comte and
# Institut des Sciences de l'Univers (INSU). 
#__________________________________________________________________________________________________________________________

import numpy as np
import scipy as sc
import pylab as plt
import pyfits

#__________________________________________________________________________________________________________________________
# Input ...
 
#image1, image2 = 'Spectral_image_1', 'Spectral_image_2'
image1, image2 = 'Example_image_1.fits','Example_image_2.fits'
#__________________________________________________________________________________________________________________________

def mask_cosmicsray(input_resid,name_output,threshold,n_thrd,im_0):

        x_ = input_resid
        x_[  x_  <= threshold*n_thrd ]                 = 99999.
        x_[( x_  >  threshold*n_thrd) & (x_ < 99999.) ] = 0
        x_[  x_  == 99999. ]                = 1.

        hdu = pyfits.PrimaryHDU(x_)
        hdulist = pyfits.HDUList([hdu])
        hdulist.writeto(name_output+'_maskcr.fits')
	mask_cr    = pyfits.open(name_output+'_maskcr.fits')
	reject_msk = mask_cr[0].data*im_0

	hdu2 = pyfits.PrimaryHDU(reject_msk)
	hdulist2 = pyfits.HDUList([hdu2])
	hdulist2.writeto(name_output+'_correct_cr.fits')


im_1, im_2     = pyfits.open(image1)  , pyfits.open(image2)
resid1, resid2 = im_1[0].data - im_2[0].data, im_2[0].data - im_1[0].data
std1, std2     = np.std(im_1[0].data) , np.std(im_2[0].data) #np.std(resid1), np.std(resid2) # np.std(im_1[0].data) , np.std(im_2[0].data)
n_thrd = 1.                                     # 3-Sigma 
mask_cosmicsray(resid1,image1, std1,n_thrd,im_1[0].data)
mask_cosmicsray(resid2,image2, std2,n_thrd,im_2[0].data)

