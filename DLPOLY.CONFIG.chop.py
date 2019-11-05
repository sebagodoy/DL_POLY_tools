#!/usr/bin/env python3

print('------------------------------------------------------------------')
print(' Extrae sección de archivo CONFIG')
print('  > De momento opera solamente en coordenadas cartesianas')
print(' para sistemas ortogonales.')
print('  > Opera por sitios, pensado para modelos uniatómicos. Podría ')
print('  partir moléculas formadas por más de un sitio')
print('------------------------------------------------------------------')


##################################################################################
# Entrada
iFile = input('\n    > Archivo (def=CONFIG) : ')
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


# Colecta, purga y traslada Data
print('    Purgando y trasladando data')
Data = []; NewAtomCounter = 0
iLine = 5
while iLine < len(content)-2:
	tmpCoordChek = float(content[iLine+1].split()[AxIndex]) #Coord
	if not (tmpCoordChek < LimMin or LimMax < tmpCoordChek):
		NewAtomCounter+=1
		tmpName = content[iLine].split()[0]+'    '+str(NewAtomCounter)+'\n'
		tmpVel = content[iLine+2]
		tmpMom = content[iLine+3]
		# Corrige posición
		tmpPos = content[iLine+1].split()
		tmpPos[AxIndex] = str(float(tmpPos[AxIndex])-NewCenter) #Coord

		Data.append([tmpName, tmpPos, tmpVel, tmpMom])
	iLine+=4


##################################################################################
# Escribe
NewFile = iFile+'_chop'
print('    Escribiendo archivo '+NewFile)
with open(NewFile, 'w') as nf:
	# header
	nf.write('  '+FileTitle+' - Seccion del original \n')

	# SubTitle
	SubTitle[2] = str(NewAtomCounter)
	SubTitle = "    ".join(SubTitle)
	nf.write('    '+SubTitle+'\n')

	#Box
	for i in Box:
		nf.write('     ')
		for j in i:
			nf.write(str(FixNum(j))+'        ')
		nf.write('\n')
	#Coord
	for iAtom in Data:
		#Nombre
		nf.write(iAtom[0])
		#Posición
		for j in iAtom[1]:
			nf.write('    '+str(j))
		nf.write('\n')
		#Vel
		nf.write(iAtom[2])
		#Mom
		nf.write(iAtom[3])
print('------------------------------------------------------------------')
print('    Nuevos vectores de celda (1) '+str(Box[0]))
print('                             (2) '+str(Box[1]))
print('                             (3) '+str(Box[2]))
print('    Se mantienen '+str(NewAtomCounter)+' sitios\n')

print('    Bye\n')






