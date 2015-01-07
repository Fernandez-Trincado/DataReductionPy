#!/usr/bin/python

# Created by: Jose G. Fernandez Trincado
# Date: 2013 June 28
# Program: This program correct the imagen .fit (Science) by Syntethic Flat
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
#   Next program: ./Run_Vfree-Synthetic_Flat.py GrupoX.dat
#                 >>> GrupoX.dat/XXX.XX.XXX.XX.XXXX.hlv*



location='/home/jfernandez/Escritorio/Tesis_2013-2014_CIDA_ULA/Data_Tesis_2013_2014_CIDA-ULA/Reflector/'

if len(sys.argv[:]) < 2.:

	print '***************************************************'
	print 'Warning: ./Run_Vfree-Synthetic_Flat.py GrupoX.dat'
	print '***************************************************'


else: 

#Combine images MEDIAN
#TASK IRAF: images.immatch.imcombine
#Function to combine images for generates Master Flat

	def Master_combina(inter_img,filt):

		iraf.images.immatch()
		iraf.images.immatch.output=filt
		iraf.images.immatch.headers=''
		iraf.images.immatch.bpmasks=''
		iraf.images.immatch.rejmasks=''
		iraf.images.immatch.nrejmasks=''
		iraf.images.immatch.expmasks=''
		iraf.images.immatch.sigmas=''
		iraf.images.immatch.logfile='STDOUT'
		iraf.images.immatch.combine='median'
		iraf.images.immatch.reject='avsigclip'
		iraf.images.immatch.project='no'
		iraf.images.immatch.outtype='real'
		iraf.images.immatch.outlimits=''
		iraf.images.immatch.offsets='none'
		iraf.images.immatch.masktype='none'
		iraf.images.immatch.maskvalue=0.
		iraf.images.immatch.blank=1.0
		iraf.images.immatch.scale='mode'
		iraf.images.immatch.zero='none'
		iraf.images.immatch.weight='mode'
		iraf.images.immatch.statsec=''
		iraf.images.immatch.expname=''
		iraf.images.immatch.lthreshold='INDEF'
		iraf.images.immatch.hthreshold='INDEF'
		iraf.images.immatch.nlow=1.
		iraf.images.immatch.nhigh=1.
		iraf.images.immatch.nkeep=1.
		iraf.images.immatch.mclip='yes'
		iraf.images.immatch.lsigma=3.
		iraf.images.immatch.hsigma=3.
		iraf.images.immatch.rdnoise=7.
		iraf.images.immatch.gain=1.68
		iraf.images.immatch.snoise=0.
		iraf.images.immatch.sigscale=0.1
		iraf.images.immatch.pclip=-0.5
		iraf.images.immatch.grow=0.
		iraf.images.immatch.imcombine(inter_img)


	data=sc.genfromtxt(sys.argv[1],dtype=str)

#Lee lista dentro de los directorios, estas listas contienen la ruta de las imagenes ya clasificadas por filtro y tiempo de exposicion. 

	for i in np.arange(len(data)):

		temp='/Initial_list_Syntethic_flat_'
		os.system('ls '+data[i]+temp+'* >temporal_classified.dat')

		data_clas=sc.genfromtxt('temporal_classified.dat',dtype=str)

		for j in np.arange(len(data_clas)):

			if data_clas[j] == data[i]+temp+'I60':

				os.system('cat '+data[i]+temp+'I60 >> MasterFlat_I60_Good.dat')

			elif data_clas[j] == data[i]+temp+'I90':

				os.system('cat '+data[i]+temp+'I90 >> MasterFlat_I90_Good.dat')

			elif data_clas[j] == data[i]+temp+'V60':

				os.system('cat '+data[i]+temp+'V60 >> MasterFlat_V60_Good.dat')

			elif data_clas[j] == data[i]+temp+'V90':

				os.system('cat '+data[i]+temp+'V90 >> MasterFlat_V90_Good.dat')

			else: 

				pass

		os.system('rm temporal_classified.dat')


	os.system('ls MasterFlat_*_Good.dat >list_temp_gen.dat')

	data_end=sc.genfromtxt('list_temp_gen.dat',dtype=str)
	
	for k in np.arange(len(data_end)):

		print 'Generating Master Flat: '+data_end[k]
		print ''
		Master_combina('@'+data_end[k],data_end[k]+'.fit')
		print 'End of the process'
		print ''

		for h in np.arange(len(data)):

			os.system('cp '+data_end[k]+'.fit '+data[h]+'/')

		os.system('rm '+data_end[k]+'.fit')

	os.system('rm list_temp_gen.dat MasterFlat_*_Good.dat')


#END
