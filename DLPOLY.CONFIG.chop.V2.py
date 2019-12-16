#!/usr/bin/env python3

print('------------------------------------------------------------------')
print(' Extrae sección de archivo CONFIG')
print('  > De momento opera solamente en coordenadas cartesianas')
print(' para sistemas ortogonales.')
print('  > Opera por moléculas (desde V2), dejando sólo moléculas completamente ')
print('  contenidas en la sección que se conserva, por lo que la densidad')
print('  podría variar.')
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
		tmp=[fieldfile[iLine-1].split()[0], int(ThisLine.split()[1]), int(fieldfile[iLine+1].split()[1])]
		MolTypes.append(tmp)
		iLine+=1
	else:
		iLine+=1
# Reporta TotalMolec y MolTypes
print('    Halla '+str(TotalMolec)+' tipos de moléculas:')
for iMol in MolTypes:
	print('        > '+str(iMol[1])+' moléculas de '+str(iMol[2])+' sitios , llamadas '+iMol[0])

print('')

#####################
# Entrada Config
iFile = input('\n    > Archivo CONFIG (def=CONFIG) : ')
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
QueryChopAxis = False
while QueryChopAxis == False:
	QueryChopAxis = input('\n    > Secciona en axis (x/y/def=z) : ')
	if QueryChopAxis == '' or QueryChopAxis == 'z':
		QueryChopAxis = 'z'
		AxIndex = 2
	elif QueryChopAxis == 'x':
		AxIndex = 0
	elif QueryChopAxis == 'y':
		AxIndex = 1
	else:
		QueryChopAxis = False
		print('        ah?, de nuevo ...')

LimMin = float(input('    > Mínima posición en axis '+QueryChopAxis+' : '))
if LimMin < -Box[AxIndex][AxIndex]/2.:
	LimMin = -Box[AxIndex][AxIndex]/2.
	print('        Excede mínimo, usa minimo de '+str(LimMin))
if Box[AxIndex][AxIndex]/2. < LimMin:
	LimMin = Box[AxIndex][AxIndex]/2.*0.9
	print('        Excede máximo, usa minimo de '+str(LimMin))

LimMax = float(input('    > Máxima posición en axis '+QueryChopAxis+' : '))
if LimMax < LimMin:
	LimMax = LimMin*1.1
	print('        Menor que mínimo, usa máximo de '+str(LimMax))
if Box[AxIndex][AxIndex]/2. < LimMax:
	LimMax = Box[AxIndex][AxIndex]/2.
	print('        Mayor que máximo, usa áximo de '+str(LimMax))

##################################################################################
# Tools
def FixNum(iNum, **kwargs):
	tmpNDec=str(kwargs.get('dec', 8))
	tmpMode=str(kwargs.get('mode', 'f'))
	tmpFormat = '{:.'+tmpNDec+tmpMode+'}'
	return tmpFormat.format(iNum)



##################################################################################
print('------------------------------------------------------------------')
print('    Escalando caja')
# Arregla Box
SpanLimits = LimMax-LimMin
NewCenter = (LimMax+LimMin)/2.
Box[AxIndex][AxIndex] = SpanLimits


# Purga según toda la molécula está contenida, colecta en Data[]
print('    Purga data dejando sólo moléculas completas en nueva caja')
print('                                      (densidad puede variar)')
Data=[]; NewMolecCounter=0; NewSiteCounter=0; MolecCounterPerType=[]
iLine=5
for i in MolTypes: # Para cada tipo de molécula
	ThisMolecCounter=0
	for j in range(i[1]): # Cada molécula de ese tipo
		# Recorre átomos de molécula para evaluar si incluir
		IncludeMolecBool = True
		for k in range(i[2]): 
			tmpCoordCheck = float(content[iLine+1+4*k].split()[AxIndex])
			#Salir de esta molécula si alguno de los siguientes falla
			if (tmpCoordCheck < LimMin or LimMax < tmpCoordCheck):
				IncludeMolecBool = False
				break #sale de for k sitios
	
		#Evalúa si guardar
		if IncludeMolecBool == True:
			NewMolecCounter+=1
			ThisMolecCounter+=1
			for k in range(i[2]):
				NewSiteCounter+=1
				tmpName = content[iLine+4*k].split()[0]+'    '+str(NewSiteCounter)+'\n'
				tmpVel = content[iLine+4*k+2]
				tmpForc = content[iLine+4*k+3]
				# Corrige posición
				tmpPos = content[iLine+4*k+1].split()
				tmpPos[AxIndex]=str(float(tmpPos[AxIndex])-NewCenter)
				# Añade
				Data.append([tmpName, tmpPos, tmpVel, tmpForc])

		# Actualiza iLine a siguiente molécula
		iLine+=4*i[2]
	MolecCounterPerType.append(ThisMolecCounter)


##################################################################################
# Escribe
NewFile = iFile+'_chop'
print('    Escribiendo archivo '+NewFile)
with open(NewFile, 'w') as nf:
	# header
	nf.write('  '+FileTitle+' - Seccion del original \n')

	# SubTitle
	SubTitle[2] = str(NewSiteCounter)
	SubTitle = "    ".join(SubTitle)
	nf.write('    '+SubTitle+'\n')

	#Box
	for i in Box:
		nf.write('     ')
		for j in i:
			nf.write(str(FixNum(j))+'    ')
		nf.write('\n')
	#Coord
	for iAtom in Data:
		#Nombre
		nf.write(iAtom[0])
		#Posición
		for j in iAtom[1]:
			nf.write('        '+str(j))
		nf.write('\n')
		#Vel
		nf.write(iAtom[2])
		#Mom
		nf.write(iAtom[3])
print('------------------------------------------------------------------')
print('    Nuevos vectores de celda (1) '+str(Box[0]))
print('                             (2) '+str(Box[1]))
print('                             (3) '+str(Box[2]))
print('    Se mantienen en total '+str(NewMolecCounter)+' moléculas, '+str(NewSiteCounter)+' sitios')
for i in range(len(MolTypes)):
	print('        > '+str(MolecCounterPerType[i])+' moleculas tipo '+MolTypes[i][0], end='')
	print(' de '+str(MolTypes[i][2])+' sitios = '+str(MolecCounterPerType[i]*MolTypes[i][2])+' sitios')

print('\n    Bye\n')






