#!/usr/bin/python

# Created by: Jose G. Fernandez Trincado
# Date: 2013 July 02
# Program: This program calculate the photometry aperture
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

#Run, program. 
#Example: 
#   Next program: ./Run_6-Aperture_Photometry.py images.fit

#[1] ***************************************************************************************************************** 

os.system('rm Mag.dat file_phot.coor temp_daofind.txt logfile_temp.dat salida_1.txt salida_2.txt') #Security by if cut the system
os.system('rm den*.fits den*.fit') #Security by if cut the system

#IRAF, Parameters:

#[2] ***************************************************************************************************************** 

#Sigma Clipped mean

def sigma_clipped_mean(data,n_iterate):
  init_data=data
  for i in np.arange(n_iterate):
    fwhm_mean=np.mean(init_data)
    std3=np.std(init_data)*3.
    min_s=fwhm_mean-std3
    max_s=fwhm_mean+std3
    mask=(min_s<=init_data)&(init_data<=max_s)
    init_data=init_data[mask]
  return np.mean(init_data), len(init_data), np.std(init_data)

#[3] ***************************************************************************************************************** 

#Programm

if len(sys.argv[:]) < 2.:
	
	print '********************************************************'
	print '   Warning: ./Run_6-Aperture_Photometry.py images.fit   '
	print '********************************************************'

else:

#[4] ***************************************************************************************************************** 

#IRAF, stat

	data_img=pyfits.open(sys.argv[1])	

#Parameters of the header

	rdnoise=float(data_img[0].header['RDNOISE'])                     # Read noise, header
	gain=float(data_img[0].header['GAIN'])                           # Gain, header
	exptime=float(data_img[0].header['EXPTIME'])                     # Exposure time
	scale_img=float(0.540694661105714)                               # Scale
	ra=data_img[0].header['RAJ2_D']                                  # RA_J2000
	dec=data_img[0].header['DECJ2_D']                                # DEC_J2000

#IRAF, imstat

	stat_int=iraf.imstat(sys.argv[1],fields='min,max,mode,mean',Stdout=1)
	statdata=''.join(stat_int).split()
	min_img, max_img, mode_sky, mean_img=float(statdata[5]), float(statdata[6]), float(statdata[7]), float(statdata[8])

#Mode: Sky Background 

	if mode_sky <0.:

		print '\n Mode is negative \n Next image .....\n'
		report=open('Report_Phot_Mag_negative.dat','a')
		report.write(sys.argv[1])
		report.close()

	else:

#[5] ***************************************************************************************************************** 

#Initial parameters

		sigma_fs=np.sqrt(mode_sky*gain+rdnoise*rdnoise)/gain          # Sigma background
		sigma_fs=2.*sigma_fs                                          # 2-Sigma background
		Data_min_init=int(mode_sky)                                   # Data min
		Data_min_end=min_img                                          # Alternative Data min
		Data_max=75000                                                # Data max

#Run Daofind	

		def daofind_(fwhm_0,img_0,out_0,d_min,d_max):
	
			iraf.noao(_doprint=0)
			iraf.digiphot(_doprint=0)
			iraf.daophot(_doprint=0)
			iraf.noao.digiphot.daophot.daofind.starmap=""
			iraf.noao.digiphot.daophot.daofind.skymap=""                #Parameters of Datapars
			iraf.noao.digiphot.daophot.daofind.scale=scale_img
			iraf.noao.digiphot.daophot.daofind.fwhmpsf=fwhm_0           #Change
			iraf.noao.digiphot.daophot.daofind.sigma=sigma_fs
			iraf.noao.digiphot.daophot.daofind.datamin=d_min
			iraf.noao.digiphot.daophot.daofind.datamax=d_max
			iraf.noao.digiphot.daophot.daofind.noise='poisson'
			iraf.noao.digiphot.daophot.daofind.gain='GAIN'
			iraf.noao.digiphot.daophot.daofind.readnoise=rdnoise
			iraf.noao.digiphot.daophot.daofind.epadu=gain
			iraf.noao.digiphot.daophot.daofind.exposure='EXPTIME'
			iraf.noao.digiphot.daophot.daofind.airmass=''
			iraf.noao.digiphot.daophot.daofind.filter='FILTER'           #Parameters of findpars
			iraf.noao.digiphot.daophot.daofind.thresho=3.                #---> Internal parameters
			iraf.noao.digiphot.daophot.daofind.boundary='nearest'
			iraf.noao.digiphot.daophot.daofind.constant=0.
			iraf.noao.digiphot.daophot.daofind.interactive='No'
			iraf.noao.digiphot.daophot.daofind.cache='No'
			iraf.noao.digiphot.daophot.daofind.verify='No'
			iraf.noao.digiphot.daophot.daofind.update='No'
			iraf.noao.digiphot.daophot.daofind.verbose='No'
			iraf.noao.digiphot.daophot.daofind.graphic=''
			iraf.noao.digiphot.daophot.daofind.display=''
			iraf.noao.digiphot.daophot.daofind(img_0,out_0,Stdout='/dev/null')

			out_daofind=sc.genfromtxt(out_0,dtype=str)

			file_daofind=open('temp_daofind.txt','a')			
			for i in np.arange(len(out_daofind)):
			  file_daofind.write(out_daofind[i,0]+'  '+out_daofind[i,1]+'\n')
			file_daofind.close()

#[6] ***************************************************************************************************************** 
	
#IRAF, PSFMEASURE
	
		def psfmeasure_(img_1):
	
			iraf.noao(_doprint=0)
			iraf.obsutil(_doprint=0)
			iraf.noao.obsutil.psfmeasure.coords='mark1'
			iraf.noao.obsutil.psfmeasure.wcs='logical'
			iraf.noao.obsutil.psfmeasure.display="no"
			iraf.noao.obsutil.psfmeasure.frame='1'
			iraf.noao.obsutil.psfmeasure.level=0.5
			iraf.noao.obsutil.psfmeasure.size='FWHM'
			iraf.noao.obsutil.psfmeasure.beta='INDEF'
			iraf.noao.obsutil.psfmeasure.scale=scale_img
			iraf.noao.obsutil.psfmeasure.radius=5.
			iraf.noao.obsutil.psfmeasure.sbuffer=5.
			iraf.noao.obsutil.psfmeasure.swidth=5.
			iraf.noao.obsutil.psfmeasure.saturat=50000
			iraf.noao.obsutil.psfmeasure.ignore_='yes'
			iraf.noao.obsutil.psfmeasure.iterati=5
			iraf.noao.obsutil.psfmeasure.xcenter='INDEF'
			iraf.noao.obsutil.psfmeasure.ycenter='INDEF'
			iraf.noao.obsutil.psfmeasure.logfile='logfile_temp.dat'
			iraf.noao.obsutil.psfmeasure.imagecur='temp_daofind.txt'
			iraf.noao.obsutil.psfmeasure.graphcur=''
			iraf.noao.obsutil.psfmeasure(img_1,StdoutG='/dev/null')	

#Calculating FWHM

			fwhm_init=sc.genfromtxt('logfile_temp.dat',skip_footer=1,skiprows=4,usecols=(0,1,3,4),dtype=float)
#			fwhm_init=fwhm_init[:,3] 			   														# Col of the FWHM
			mask=(fwhm_init[:,3]<=0.4)                                  # Ellip < 0.2 , ~ 98 % point source
			x_fwh=fwhm_init[mask,0]
			y_fwh=fwhm_init[mask,1]
			fwhm_init=fwhm_init[mask,2]

#			fwhm_file=open(sys.argv[1]+'.astrometry','a')           # Initial information for the astrometry
#			for f in np.arange(len(fwhm_init)):
#				fwhm_file.write(str(x_fwh[f])+'\t'+str(y_fwh[f])+'\n')
#			fwhm_file.close()

			fwhm_sigclpmean,NstarFWHM,var_death=sigma_clipped_mean(fwhm_init,1000)
			return float('%4.2f' %(fwhm_sigclpmean)),str(NstarFWHM)

		daofind_(7.,sys.argv[1],'salida_1.txt',Data_min_init,Data_max) # Creating 'temp_daofind.txt', initial coordenates
		New_FWHM,NstarFWHM=psfmeasure_(sys.argv[1])                    # Calculating initial FWHM
		daofind_(7.,sys.argv[1],'salida_2.txt',Data_min_end,Data_max)  # New FWHM

#[7] ***************************************************************************************************************** 

#Calculating Aperture radii

		rap=New_FWHM/scale_img                                        #Aperture radii
		rap=int('%i' %(round(rap)))
		
		file_phot=sc.genfromtxt('salida_2.txt')
		file_phot1=open('file_phot.coor','a')
		for k in np.arange(len(file_phot)):
			file_phot1.write(str(file_phot[k,0])+'  '+str(file_phot[k,1])+' \n')
		file_phot1.close()
		os.system('rm  temp_daofind.txt logfile_temp.dat')

#[8] ***************************************************************************************************************** 

#IRAF, Calculating Phot

		def phot_(img_int,coor_img,out_img):
		
			iraf.noao()
			iraf.digiphot()
			iraf.apphot()
			iraf.noao.digiphot.apphot.phot.skyfile=''
			iraf.noao.digiphot.apphot.phot.coords=coor_img
			iraf.noao.digiphot.apphot.phot.output=out_img
			iraf.noao.digiphot.apphot.phot.plotfile=''
			iraf.noao.digiphot.apphot.phot.scale=scale_img
			iraf.noao.digiphot.apphot.phot.fwhmpsf=New_FWHM
			iraf.noao.digiphot.apphot.phot.emission='yes'
			iraf.noao.digiphot.apphot.phot.sigma=sigma_fs
			iraf.noao.digiphot.apphot.phot.datamin=Data_min_end
			iraf.noao.digiphot.apphot.phot.datamax=Data_max
			iraf.noao.digiphot.apphot.phot.noise='poisson'
			iraf.noao.digiphot.apphot.phot.ccdread='RDNOISE'
			iraf.noao.digiphot.apphot.phot.gain='GAIN'
			iraf.noao.digiphot.apphot.phot.readnoise='0.'
			iraf.noao.digiphot.apphot.phot.epadu=1.68
			iraf.noao.digiphot.apphot.phot.exposure='EXPTIME'
			iraf.noao.digiphot.apphot.phot.airmass='AIRMASS'
			iraf.noao.digiphot.apphot.phot.filter='FILTER'
			iraf.noao.digiphot.apphot.phot.obstime=''
			iraf.noao.digiphot.apphot.phot.itime='1.0'
			iraf.noao.digiphot.apphot.phot.xairmass='INDEF'
			iraf.noao.digiphot.apphot.phot.ifilter='INDEF'
			iraf.noao.digiphot.apphot.phot.otime='INDEF'
			iraf.noao.digiphot.apphot.phot.calgorithm='none'
			iraf.noao.digiphot.apphot.phot.cbox='8.0'
			iraf.noao.digiphot.apphot.phot.cthreshold='0.0'
			iraf.noao.digiphot.apphot.phot.minsnratio='1.0'
			iraf.noao.digiphot.apphot.phot.cmaxiter='10'
			iraf.noao.digiphot.apphot.phot.maxshift='5.0'
			iraf.noao.digiphot.apphot.phot.clean='no'
			iraf.noao.digiphot.apphot.phot.rclean='1.0'
			iraf.noao.digiphot.apphot.phot.rclip='2.0'
			iraf.noao.digiphot.apphot.phot.kclean='3.0'
			iraf.noao.digiphot.apphot.phot.mkcenter='no'
			iraf.noao.digiphot.apphot.phot.salgorithm='mode'
			iraf.noao.digiphot.apphot.phot.annulus='15.'
			iraf.noao.digiphot.apphot.phot.dannulus='5.'
			iraf.noao.digiphot.apphot.phot.skyvalue='0.'
			iraf.noao.digiphot.apphot.phot.smaxiter='10'
			iraf.noao.digiphot.apphot.phot.sloclip='0.'
			iraf.noao.digiphot.apphot.phot.shiclip='0.'
			iraf.noao.digiphot.apphot.phot.snreject='50'
			iraf.noao.digiphot.apphot.phot.sloreject='3.'
			iraf.noao.digiphot.apphot.phot.shireject='3.'
			iraf.noao.digiphot.apphot.phot.khist='3.'
			iraf.noao.digiphot.apphot.phot.binsize='0.1'
			iraf.noao.digiphot.apphot.phot.smooth='no'
			iraf.noao.digiphot.apphot.phot.rgrow='0.'
			iraf.noao.digiphot.apphot.phot.mksky='no'
			iraf.noao.digiphot.apphot.phot.weighting='constant'
			iraf.noao.digiphot.apphot.phot.apertures=rap
			iraf.noao.digiphot.apphot.phot.zmag='25.0'
			iraf.noao.digiphot.apphot.phot.mkapert='no'
			iraf.noao.digiphot.apphot.phot.interactive='no'
			iraf.noao.digiphot.apphot.phot.radplots='no'
			iraf.noao.digiphot.apphot.phot.icommands=''
			iraf.noao.digiphot.apphot.phot.gcommands=''
			iraf.noao.digiphot.apphot.phot.cache='no'
			iraf.noao.digiphot.apphot.phot.verify='no'
			iraf.noao.digiphot.apphot.phot.update='no'
			iraf.noao.digiphot.apphot.phot.verbose='no'
			iraf.noao.digiphot.apphot.phot(img_int)
		
#IRAF, Reading file Mag.dat

		def file_mag(int_file):

			iraf.noao(_doprint=0)
			iraf.digiphot(_doprint=0)
			iraf.ptools(_doprint=0)
	
			out_mag=iraf.noao.digiphot.ptools.txdump(int_file,fields='id, XCENTER, YCENTER, MAG, MERR, MSKY',expr='MAG!=INDEF',headers='no',parameters='yes',Stdout=1)
			out_mags=open(sys.argv[1]+'.mag','a')
			out_mags.write('#'+sys.argv[1]+'\n#AR	'+str(float(ra)/15.)+'\n#DEC	'+str(dec)+'\n#FWHM	'+str(New_FWHM)+'\n#NstarFWHM	'+str(NstarFWHM)+'\n#Sigma	'+str(sigma_fs)+'\n#Datamin	'+str(Data_min_end)+'\n#Datamax	'+str(Data_max)+'\n#GAIN	1.68'+'\n#RDNOI	7'+'\n#THRESHOLD	3'+'\n#Raperture	'+str(rap)+'\n')
	
			for h in np.arange(len(out_mag)):
				out_mags.write(out_mag[h]+' \n')
			out_mags.close()

#Photometry

		phot_(sys.argv[1],'file_phot.coor','Mag.dat')
		file_mag('Mag.dat')

		os.system('rm Mag.dat file_phot.coor temp_daofind.txt logfile_temp.dat salida_1.txt salida_2.txt')

#END
