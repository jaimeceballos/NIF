from fpdf import FPDF
import barcode, os, shutil

TAMANIO_CODIGO = 50

def digitoverificador(valor):
	total = 0
	valorasc = 0

	letras = {
		1 : "A", 2 : "B", 3 : "C", 4 : "D", 5 : "E",
		6 : "F", 7 : "G", 8 : "H", 9 : "I", 10 : "J",
		11 : "K", 12 : "M", 13 : "N", 14 : "P", 15 : "R",
		16 : "S", 17 : "T", 18 : "U", 19 : "V", 20 : "W",
		21 : "X", 22 : "Y", 23 : "Z",
	}

	for x in range(0,12):
		valorAsc = ord(valor[x])
		if x in [0,4,8]:
			total += valorAsc
		elif x in [1,5,9]:
			total += valorAsc * 2
		elif x in [2,6,10]:
			total += valorAsc * 4
		elif x in [3,7,11]:
			total += valorAsc * 8

	indiceLetra = total - int((total / 23) * 23) + 1

	return letras[indiceLetra]

def completar(numero):
	while len(numero) < 8:
		numero = str(0)+numero
	return numero

def crear_barcode(numero):
	filename = os.path.join('generated','temp',str(numero))
	print filename
	writer = barcode.writer.ImageWriter()
	code = barcode.Code39(numero,writer = writer,add_checksum = False)
	archivo = code.save(filename)
	return archivo

def generar_codigos(provincia,ciudad,numeroInicial,cantidad):
	total_imagenes = cantidad * 2
	paginas =  calcular_cantidad_paginas(total_imagenes)
	archivo = FPDF('P','mm','A4')
	archivo.add_page()
	for pagina in range(0,paginas):
		eje_x = 0
		for linea in range(0,12):
			if(cantidad <= 0):
				break
			for codigo in range(0,2):
				if(cantidad <= 0):
					break
				numero =  completar(str(numeroInicial))
				numero = str(provincia) + str(ciudad) + numero
				digito = digitoverificador(numero)
				numero = numero + str(digito)
				for imagen in range(0,2):
					archivo.image(crear_barcode(numero),eje_x * 50, linea * 25 , TAMANIO_CODIGO)
					eje_x += 1
				cantidad = cantidad -1
				numeroInicial += 1
			eje_x = 0
		if(cantidad > 0):
			archivo.add_page()
	archivo.output(os.path.join('generated','codigos.pdf'),'F')
	shutil.rmtree(os.path.join('generated','temp'))

def calcular_cantidad_paginas(cantidad):
	resto = (cantidad / 48.0) - (cantidad / 48)
	if( resto > 0 ):
		return ((cantidad / 48 ) + 1)
	return (cantidad / 48)

def borrar_anterior():
	os.remove(os.path.join('generated','codigos.pdf'))
	os.makedirs(os.path.join('generated','temp'))
