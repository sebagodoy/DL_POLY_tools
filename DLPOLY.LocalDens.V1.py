#!/usr/bin/env python3

print('------------------------------------------------------------------')
print(' Genera histogramas y tablas de distribución de densidades locales')
print(' desde partición de caja')
print('  > De momento opera solamente en coordenadas cartesianas')
print(' para sistemas ortogonales.')
print('  > Opera por moléculas, considerando su posición en su centro de masa')
print('------------------------------------------------------------------')


##################################################################################
#####################
# Cantidad de moléculas
iField = input('\n    > Archivo FIELD (def/FIELD) : ')
if iField == '':
	iField='FIELD'
with open(iField, 'r') as f:
	fieldfile = f.readlines()
	f.close()
print('    Archivo hallado, recoge data', end='...\n')

iLine = 0; TotalMolec=0; MolTypes=[]
#Cantidad total de moleculas
while iLine < len(fieldfile):
	ThisLine=fieldfile[iLine]
	if ThisLine[:9] == 'MOLECULES':
		TotalMolec= int(ThisLine.split()[1]); iLine+=1
		break # Ya halló, sale
	else:
		iLine+=1
# Nombres y tipos
while (iLine < len(fieldfile)) and (len(MolTypes)<TotalMolec):
	ThisLine=fieldfile[iLine]
	if ThisLine[:7] == 'NUMMOLS' or ThisLine[:7]=='nummols':
		#Ingresa data de molécula
		tmpName=fieldfile[iLine-1].split()[0]
		tmpNMolecs=int(ThisLine.split()[1])
		tmpNAtoms=int(fieldfile[iLine+1].split()[1])
		#Nombres y masas atómicas
		tmpAtomCounter=0; tmpNames=[]; tmpMasas=[]; 
		iLine+=2 #primera línea atómica
		while tmpAtomCounter < tmpNAtoms:
			tmpAtomCounter+=int(fieldfile[iLine].split()[3])
			for i in range(int(fieldfile[iLine].split()[3])):
				tmpNames.append(fieldfile[iLine].split()[0])
				tmpMasas.append(float(fieldfile[iLine].split()[1]))

			iLine+=1
		
		#Compila, añade a registro en MolTypes
		tmp=[tmpName, tmpNMolecs, tmpNAtoms, tmpNames, tmpMasas]
		# [ Molec tipo 1 , N molecs tipo 1 , N Atoms en Molec tipo 1,
		# 			[Atom 1, Atom 2, ...], [Masa Atom 1, Masa atom 2, ...]]
		MolTypes.append(tmp)
	else:
		iLine+=1


# Reporta TotalMolec y MolTypes
print('    Halla '+str(TotalMolec)+' tipos de moléculas:')
for iMol in MolTypes:
	print('        > Moléculas '+iMol[0]+' , '+str(iMol[1])+' de '+str(iMol[2])+' sitios:')
	print('          Sitio(Masa) ', end='')
	linePrintCount=0
	for i in range(len(iMol[3])):
		print(iMol[3][i]+'('+str(iMol[4][i])+')  ', end='')
		linePrintCount+=1
		if linePrintCount >3:
			print('\n                      ', end='')
			linePrintCount=0
	


#####################
# Entrada Config
iFile = input('\n\n    > Archivo CONFIG (def=CONFIG) : ')
if iFile == '':
	iFile = 'CONFIG'

with open(iFile, 'r') as f:
	content = f.readlines()
	f.close()

print('    Archivo hallado, recoge data', end=' . . .\n')

FileTitle = " ".join(content[0].split())

SubTitle = content[1].split()
IncludeDataKey = int(SubTitle[0])
## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if not IncludeDataKey == 2:
	print('    Sólo programado para archivos en formato CONFIG que ')
	print('    incluyan posiciones, velocidades y fuerzas.')
	print('    Lo, lamento. Quizás en el futuro!\n')
	print('    Por ahora sugiero hacer un breve test-run sólo')
	print('    para generar archivo con velocidades y fuerzas.')
	quit()
## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Reporta

Box = []
for i in range(2,5):
	tmpVect=[]
	for j in content[i].split():
		tmpVect.append(float(j))
	Box.append(tmpVect)

print('    Vectores de celda (1) '+str(Box[0]))
print('                      (2) '+str(Box[1]))
print('                      (3) '+str(Box[2]))

##################################################################################
# Limites de corte
#QueryChopAxis = False
#while QueryChopAxis == False:
#	QueryChopAxis = input('\n    > Secciona en axis (x/y/def=z) : ')
#	if QueryChopAxis == '' or QueryChopAxis == 'z':
#		QueryChopAxis = 'z'
#		AxIndex = 2
#	elif QueryChopAxis == 'x':
#		AxIndex = 0
#	elif QueryChopAxis == 'y':
#		AxIndex = 1
#	else:
#		QueryChopAxis = False
#		print('        ah?, de nuevo ...')
#
#LimMin = float(input('    > Mínima posición en axis '+QueryChopAxis+' : '))
#if LimMin < -Box[AxIndex][AxIndex]/2.:
#	LimMin = -Box[AxIndex][AxIndex]/2.
#	print('        Excede mínimo, usa minimo de '+str(LimMin))
#if Box[AxIndex][AxIndex]/2. < LimMin:
#	LimMin = Box[AxIndex][AxIndex]/2.*0.9
#	print('        Excede máximo, usa minimo de '+str(LimMin))
#
#LimMax = float(input('    > Máxima posición en axis '+QueryChopAxis+' : '))
#if LimMax < LimMin:
#	LimMax = LimMin*1.1
#	print('        Menor que mínimo, usa máximo de '+str(LimMax))
#if Box[AxIndex][AxIndex]/2. < LimMax:
#	LimMax = Box[AxIndex][AxIndex]/2.
#	print('        Mayor que máximo, usa áximo de '+str(LimMax))

##################################################################################
# Tools
def FixNum(iNum, **kwargs):
	tmpNDec=str(kwargs.get('dec', 8))
	tmpMode=str(kwargs.get('mode', 'f'))
	tmpFormat = '{:.'+tmpNDec+tmpMode+'}'
	return tmpFormat.format(iNum)



##################################################################################
#print('------------------------------------------------------------------')

# Centros de masa
QuyCM = input('    > Reduce sitios a centros de masa moleculares? (def=y/n) : ')
if QuyCM == '':
	QuyCM='y'
if not (QuyCM == 'y' or QuyCM == 'n'):
	print('    Qué?, nah, bye!'); quit()

# Genera lista de centro de masa de moléculas completas
print('    Reduce sitios a centros de masa de moléculas\n\n')
Data=[]; NewMolecCounter=0; NewSiteCounter=0; MolecCounterPerType=[]
iLine=5
for i in MolTypes: # Para cada tipo de molécula i en MolTypes[i1, i2, i3, ...]
	for j in range(i[1]): # Para las i[1] moléculas de ese tipo
		tmpMasaMolec=0.
		tmpCMx=0.; tmpCMy=0.; tmpCMz=0.
		# SECCIÓN PUEDE OPTIMIZARSE juntando x,y,z en vector

		if QuyCM == 'y':
			for k in range(i[2]): # Para los i[2] átomos en este tipo de molécula
				tmpPos = content[iLine+4*k+1].split()
				tmpCMx+=float(tmpPos[0])*i[4][k]
				tmpCMy+=float(tmpPos[1])*i[4][k]
				tmpCMz+=float(tmpPos[2])*i[4][k]
				tmpMasaMolec+=i[4][k]
			tmpCMx*=(1./tmpMasaMolec)
			tmpCMy*=(1./tmpMasaMolec)
			tmpCMz*=(1./tmpMasaMolec)
			
			# Añade molec
			Data.append([tmpCMx, tmpCMy, tmpCMz])
		elif QuyCM == 'n':
			for k in range(i[2]): # Para los i[2] átomos en este tipo de molécula
				tmpPos = content[iLine+4*k+1].split()
				tmpCMx=float(tmpPos[0])
				tmpCMy=float(tmpPos[1])
				tmpCMz=float(tmpPos[2])
				Data.append([tmpCMx, tmpCMy, tmpCMz])

		# Actualiza iLine a siguiente molécula
		iLine+=4*i[2]



##################################################################################
#####################
# División en Bins
print('    Estructura de Bins (asume Lx=Ly<Lz)')

#Estructura de Bins
NbinsXY=int(input('    > Cantidad de bins en X e Y : '))
sizeXYBin = Box[0][0]/float(NbinsXY)

NbinsZ=int(Box[2][2]/sizeXYBin)
sizeZBin = Box[2][2]/float(NbinsZ)

BinSize=[sizeXYBin, sizeXYBin, sizeZBin]
VolBin=sizeXYBin*sizeXYBin*sizeZBin

#Reporta
print('        Genera '+str(NbinsXY*NbinsXY*NbinsZ)+' bins en arreglo ', end='')
print(str(NbinsXY)+' x '+str(NbinsXY)+' x '+str(NbinsZ))
print('        cada uno con volumen  : '+str(FixNum(VolBin, dec=2))+' \AA^3')
print('            dimensiones (\AA) : ', end='')
print(str(FixNum(sizeXYBin, dec=1))+' x '+str(FixNum(sizeXYBin, dec=1))+' x '+str(FixNum(sizeZBin, dec=1)))

#Genera BinMatrix
print('    Generando estructura de bins ... ', end=':')
BinMatrix=[]
for i in range(NbinsXY):
	tmpX=[]
	for j in range(NbinsXY):
		tmpY=[]
		for k in range(NbinsZ):
			tmpY.append(0)
		tmpX.append(tmpY)
	BinMatrix.append(tmpX)

print(str(len(BinMatrix))+' x '+str(len(BinMatrix[0]))+' x '+str(len(BinMatrix[0][0])))

#####################
# División en Bins
print('    Asignando lista molecular a bins . . . ')
for iCoords in Data:# Para cada centro de masa
	# Index de Bin, de coordenadas trasladadas
	# index parte de [0][0][0]
	tmpX=int((iCoords[0]+Box[0][0]/2.)/sizeXYBin)
	tmpY=int((iCoords[1]+Box[1][1]/2.)/sizeXYBin)
	tmpZ=int((iCoords[2]+Box[2][2]/2.)/sizeZBin)
	# Asigna
	BinMatrix[tmpX][tmpY][tmpZ]+=1

# Generando lista de densidades
print('    Enlistando densidades')
DensList=[]
for i in range(len(BinMatrix)):
	for j in range(len(BinMatrix[0])):
		for k in range(len(BinMatrix[0][0])):
			DensList.append(float(BinMatrix[i][j][k])/VolBin)

# Histograma
print('    Generando histograma')
import numpy as np
import matplotlib.pyplot as plt
#plt.hist(DensList, bins='auto', alpha=0.3)
#plt.hist(DensList, bins=np.arange(0.0, 0.003, 0.0001), alpha=0.3)
#plt.show()

#for i in range(len(DensList)):
#	plt.plot(DensList[i],float(i)/1e3,'.')
#
YY=[]
for i in range(len(DensList)):
	YY.append(i/1e-3)
plt.plot(DensList,YY,'.')
plt.show()	

QHistoBins=[]; QHistoCant=[]
for i in range(len(DensList)):
	if DensList[i] in QHistoBins:
		QHistoCant[QHistoBins.index(DensList[i])]+=1
	else:
		QHistoBins.append(DensList[i])
		QHistoCant.append(1.0)

plt.plot(QHistoBins, QHistoCant, '.')
plt.show()




