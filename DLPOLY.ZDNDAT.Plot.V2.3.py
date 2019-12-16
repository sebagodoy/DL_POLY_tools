#!/usr/bin/env python3

##################################################################################
#	Grafica archivos ZDNDAT
#	V.2. 	Agrega reconocer varios tipos de sitios
#	V.2.1	Agrega eleccion de plotear y escalamiento
#	V.2.2	Agrega promedio, permite limitar rangos
#       V.2.3   Agrega N datos en promedio y error estandar de la media
##################################################################################



print('------------------------------------------------------------------')
print(' Plotea archivo ZDNDAT generado por \'DL_POLY\' con z\'den i\'')
print('------------------------------------------------------------------')


##################################################################################
# Entrada
iFile = input('\n    > Archivo (def=ZDNDAT) : ')
if iFile == '':
	iFile = 'ZDNDAT'

with open(iFile, 'r') as f:
	content = f.readlines()
	f.close()

print('    Archivo hallado, recoge data', end=' . . .')


Names=[content[2].split()[0]]
zDatAll=[]; denDatAll=[]
zDat=[]; denDat=[]

iLine = 3
while iLine < len(content)-1:
	ThisLine = content[iLine].split()
	if len(ThisLine) > 1:
		zDat.append(float(ThisLine[0]))
		denDat.append(float(ThisLine[1]))
	else:
		Names.append(ThisLine[0])
		#Agrega anteriores, reset a zero
		zDatAll.append(zDat); denDatAll.append(denDat)
		zDat=[];denDat=[]
		
	iLine+=1

zDatAll.append(zDat); denDatAll.append(denDat) # Última linea
print('Listo!')

zIni = zDat[0]; zFin = zDat[len(zDat)-1]
#print('    Desde ')

print('    Se han detectado '+str(len(Names))+' tipos de sitios : ', end='')
for i in Names:
	print(i, end='  ')
print('')

##################################################################################
# Purga y escalado
print('    Purga y escalamiento (float, 0 = omite, def/1 = original) : ')
print('        (Index) sitio : factor    |    num -> num/factor ')

zDatPlot=[]; denDatPlot=[]; NamesPlot=[]

for i in range(len(Names)):
	tmpShowQuy = input('        > ('+str(i)+') '+Names[i]+' : ')
	if tmpShowQuy == '':
		NamesPlot.append(Names[i])
		zDatPlot.append(zDatAll[i])
		denDatPlot.append(denDatAll[i])

	elif float(tmpShowQuy) != 0.:
		NamesPlot.append(Names[i]+'*(1/'+str(tmpShowQuy)+')')
		zDatPlot.append(zDatAll[i])
		tmpDat=[]
		for j in denDatAll[i]:
			tmpDat.append(j/float(tmpShowQuy))
		denDatPlot.append(tmpDat)

if len(NamesPlot) < 1:
	print('    Al menos debe dejar que una serie para trabajar, adios!\n')
	quit()

zMin = zDatPlot[0][0]
zMax = zDatPlot[0][len(zDatPlot[0])-1]
#print(zMin)
#print(zMax)

##################################################################################
# Tools
import numpy as np
import matplotlib.pyplot as plt

def FixNum(iNum, **kwargs):
	tmpNDec=str(kwargs.get('dec', 4))
	tmpMode=str(kwargs.get('mode', 'f'))
	tmpFormat = '{:.'+tmpNDec+tmpMode+'}'
	return tmpFormat.format(iNum)

def PlotNow():
	print('Ploteando . . . ', end='. . . hecho!\n')
	for i in range(len(NamesPlot)):
		plt.plot(zDatPlot[i], denDatPlot[i], '.-', label=NamesPlot[i], linewidth=0.5)
	plt.legend()
	plt.show()

##################################################################################
# Plot
print('------------------------------------------------------------------')
if input('    Graficar ahora? (def~y/n) :') != 'n':
	PlotNow()

OtraVuelta = True
while OtraVuelta == True:
	# while de promedios
	OtroProm =  True
	while OtroProm == True:
		QuyProm = input('    Calcular promedio? (y/def=n/salir) : ')
		if  QuyProm == 'y':
			# Cosas para calcular promedios
			# Index
			if len(NamesPlot)==1:
				tmpIndex=0
			else:
				tmpIndex=1e5
			while tmpIndex < 0. or len(NamesPlot)-1 < tmpIndex:
				tmpIndex = int(input('        > Index sitio : '))
			# Inicio
			tmpIniZ = float(input('        > Desde z ='))
			if tmpIniZ > zMax:
				tmpIniZ = zMax*0.9
				print('         --> Mayor que máximo, usa '+str(tmpIniZ))
			# Fin
			tmpFinZ = float(input('        > Hasta z ='))
			if tmpFinZ < tmpIniZ:
				tmpFinZ = zMax
				print('         --> Menor que mínimo, usa '+str(tmpFinZ))
			# Promedia
			tmpDen=[]
			for i in range(len(denDatPlot[tmpIndex])):
				if tmpIniZ < zDatPlot[tmpIndex][i] and zDatPlot[tmpIndex][i] < tmpFinZ:
					tmpDen.append(denDatPlot[tmpIndex][i])
			print('        Promedio = '+str(FixNum(np.average(tmpDen), dec=8)))
			print('        Std desv = '+str(FixNum(np.std(tmpDen), dec=8)))
			print('        Err Std  = '+str(FixNum(np.std(tmpDen)/np.sqrt(len(tmpDen)), dec=8)))
			print('        N Ptos   = '+str(len(tmpDen)))
			
		elif QuyProm == 'salir':
			print('\nBye!\n');quit()
		else:
			OtroProm=False
	#Plot
	QuyPlot = input('    Graficar de nuevo? (y/def=n/salir) : ')
	if  QuyPlot == 'y':
		PlotNow()
	elif QuyPlot == 'salir':
		print('\nBye!\n');quit()
		OtraVuelta = False




print('    Bye!\n')









