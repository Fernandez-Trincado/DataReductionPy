#!/usr/bin/python

# Created by: Jose G. Fernandez Trincado
# Date: 2013 June 26
# Program: This program correct the imagen .fit (Science) by Master Bias and Trimming Section
# 1 m Reflector telescope, National Astronomical Observatory of Venezuela
# Mode f/5, 21 arcmin x 21 arcmin
# Project: Omega Centauri, Tidal Tails. 
# The program Astrometry_V1.py defined was developed by J. G. Fernandez Trincado at the Centro de Investigaciones de Astronomia "Francisco J. Duarte".
# If you have any problems, please contact J. G. Fernandez Trincado, jfernandez@cida.ve / jfernandezt87@gmail.com


import numpy as np
import scipy as sc
import pyfits
import sys, os
from pyraf import iraf

#run, program. 
#Example: 
#   Next program: ./Run_5-Basic_Corretion_Flat.py Feb.22.Feb.23.2013.hlv/ 
#                 >>> Feb.22.Feb.23.2013.hlv/

location='/home/jfernandez/Escritorio/Tesis_2013-2014_CIDA_ULA/Data_Tesis_2013_2014_CIDA-ULA/Reflector/'

#IRAF, Parameters:

trimse=str('[51:2098,1:2049]') # trimsec

if len(sys.argv[:]) < 2.:

  print '***************************************************'
  print 'Warning: ./Run_5-Basic_Corretion_Flat.py XXX.xx.XXX.xx.XXXX.hlv'
  print '***************************************************'

else:

#Function, IRAF, Statistics

	def stat_mode(im_flat):

		iraf.images()
		iraf.imutil()

		mode_f=iraf.imstatistics(
		images=im_flat,
		fields='mode',
		lower='INDEF',
		upper='INDEF',
		nclip=0,
		lsigma=3,
		usigma=3,
		binwidt=0.1,
		format='yes',
		cache='no',
		Stdout=1)

		return float(mode_f[1])


	def stat_norm(im2_flat,ope_flat,out_flat_end):

		iraf.images()
		iraf.imutil()

		iraf.imarith(
		operand1=im2_flat,
		op='/',
		operand2=ope_flat,
		result=out_flat_end,
		title='',
		divzero=0.,
		hparams='',
		pixtype='',
		calctyp='',
		verbose='no',
		noact='no',
		mode='ql')


#Execution for IRAF
	
	os.system('ls '+sys.argv[1]+'/Initial_list_Syntethic_flat_* >temp_masterflat.dat')
	data=sc.genfromtxt('temp_masterflat.dat',dtype=str)
	os.system('rm temp_masterflat.dat')

#IRAF, Execution of the reduction

	iraf.imred()
	iraf.ccdred()

	for i in np.arange(len(data)):

		index1=map(str,data[i].split('Initial_list_Syntethic_flat_'))[1]
		index0=map(str,data[i].split('Initial_list_Syntethic_flat_'))[0]
		MasterFlat=index0+'MasterFlat_'+index1+'_Good.dat.fit'
		NMasterFlat=index0+'Norm_MasterFlat_'+index1+'_Good.dat.fit'

		stat_norm(MasterFlat,stat_mode(MasterFlat),NMasterFlat)

		lis=sc.genfromtxt(data[i],dtype=str)
		print ''
		print 'Correcting by: '+MasterFlat		
		print ''

		for k in np.arange(len(lis)):

			im=map(str,lis[k].split('_BR.fit'))[0]
			outs=im+'_'+sys.argv[1]+'_BRF.fit' # output ccdproc
			n=str('no') #negative
			print ''				
			print 'Process: ['+str(k+1)+'/'+str(len(lis))+']'
			print outs

			iraf.ccdproc(images=lis[k],output=outs,ccdtype='',fixpix=n,zerocor=n,darkcor=n,flatcor='yes',illumco=n,fringec=n,readcor=n,scancor=n,biassec='',trimsec=trimse,zero='',flat=NMasterFlat,interac=n,overscan=n,trim=n)

			os.system('bzip2 '+lis[k])
			os.system('mv '+outs+' /media/jfernandez/JF/Temporal_fits_Reflector_2013_Reducidas')

#END
