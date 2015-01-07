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
#   Next program: ./Run_3-Basic_Corretion.py Feb.22.Feb.23.2013.hlv/ 
#                 >>> Feb.22.Feb.23.2013.hlv/*.fit

location='/home/jfernandez/Escritorio/Tesis_2013-2014_CIDA_ULA/Data_Tesis_2013_2014_CIDA-ULA/Reflector/'

#IRAF, Parameters:

trimse=str('[51:2098,1:2049]') # trimsec


if len(sys.argv[:]) < 2.:

  print '***************************************************'
  print 'Warning: ./Run_3-Basic_Corretion.py XXX.xx.XXX.xx.XXXX.hlv'
  print '***************************************************'
  

else:


	os.system('ls '+sys.argv[1]+'/Science/*.fit >temp_science.dat')
	data=sc.genfromtxt('temp_science.dat',dtype=str)
	MasterBias=location+sys.argv[1]+'/Master_Bias.fit'
	iraf.imred()
	iraf.ccdred()

#IRAF, Execution of the reduction

	num=len(data)

	for i in np.arange(len(data)):

		im=map(str,data[i].split('.fit'))[0]
		outs=im+'_B.fit' # output ccdproc
		outsrotate=im+'_BR.fit' # output rotating
		n=str('no') #negative
		print ''				
		print 'Process: ['+str(i+1)+'/'+str(num)+']'
		print data[i]+' ----> '+outs


		iraf.ccdproc(images=data[i],output=outs,ccdtype='',fixpix=n,zerocor='yes',darkcor=n,flatcor=n,illumco=n,fringec=n,readcor=n,scancor=n,biassec='',trimsec=trimse,zero=MasterBias,interac=n,overscan=n,trim='yes')

		iraf.noao()
		iraf.images()
		iraf.imutil()

		statdata=iraf.imstat(outs,fields='mean,min,max',Stdout=1)
		statdata_min=''.join(statdata).split()[5]
		statdata_max=''.join(statdata).split()[6]
		statdata_mean=''.join(statdata).split()[4]
		print 'Min: '+str(statdata_min)+' Max: '+str(statdata_max)+' Mean: '+str(statdata_mean)
		print ''
		print 'Correcting the image below and rotating:'

#IRAF, (ROTATING the image)

		iraf.images()
		iraf.imgeom()

#IRAF, Execution

		iraf.rotate(input=outs,output=outsrotate,rotation=180.0)
		print outs+' ----> '+outsrotate
		print ''

#SYSTME, Compress

		os.system('bzip2 '+data[i])
		os.system('bzip2 '+location+outs)

#IRAF, Manipulating the information of the header (.fit)

		intro=pyfits.open(outsrotate,mode='update',save_backup=False)
	
		printheader=intro[0].header
	
		DATEOBS=printheader['DATE-OBS']
		LTOBS=printheader['LT-OBS'] #start time of the observation
		RAOBS=printheader['RA-OBS']
		DECOBS=printheader['DEC-OBS']
	
		if DECOBS[0] == 'S':
	
			RA=RAOBS.replace("h",":").replace("m",":").replace("s","").replace(" ","")
			DEC=DECOBS.replace("g",":").replace("m",":").replace("s","").replace("S","-").replace(" ","")
	
		else:
	
			RA=RAOBS.replace("h",":").replace("m",":").replace("s","").replace(" ","")
			DEC=DECOBS.replace("g",":").replace("m",":").replace("s","").replace("N","").replace(" ","")
	
	
		yearO=DATEOBS[6]+DATEOBS[7]+DATEOBS[8]+DATEOBS[9]
		monthO=DATEOBS[0]+DATEOBS[1]
		dayO=DATEOBS[3]+DATEOBS[4]
	
		print '********   Date of the Observation  ********'
		print dayO, monthO, yearO, RA, DEC, LTOBS
		print ''

#IRAF, current season

		iraf.astutil()
		epoca1=iraf.asttimes(files="",header="no",observa="NOV",year=yearO,month=monthO,day=dayO,time=LTOBS,Stdout=1)	
		epoca2=''.join(epoca1).split()
		epocafin=epoca2[6]
		JD=epoca2[7]
		
		print ""
		print "Epoch: ", epocafin
		print "JD: ", JD
		print ""

#IRAF, current season to epoch J2000 


		filtemp_f=open('temp.precess','w')
		coord_f=RA+" "+DEC
		filtemp_f.write(str(coord_f))
		filtemp_f.close()
	
		result_f=iraf.precess(input='temp.precess',startyear=epocafin,endyear=2000,Stdout=1)
		
		result_f=''.join(result_f).split()
	
		RAJ2000=result_f[0]
		DECJ2000=result_f[1]
	
		os.system('skycoor -d '+RAJ2000+' '+DECJ2000+' >convert.precess')
		corv=sc.genfromtxt('convert.precess')

	
		printheader.update('RAJ2000',RAJ2000) #Write in the header, sexagesimal
		printheader.update('DECJ2000',DECJ2000) #Write in the header, sexagesimal
		printheader.update('RAJ2_d',str(corv[0])) #Write in the header, decimal degree
		printheader.update('DECJ2_d',str(corv[1])) #Write in the header, decimal degree
		printheader.update('JD',JD) #Write in the header
		printheader.update('EC',epocafin) #Write in the header
	
		intro.close()
		os.system('rm temp.precess')
		os.system('rm convert.precess')		

os.system('rm temp_science.dat')
os.system('mv logfile Register_correction_Bias.txt')
os.system('mv Register_correction_Bias.txt '+location+sys.argv[1])

#END
