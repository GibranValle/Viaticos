"""
Bot creador de plantilla de vale azul para comprobación de
gastos no deducibles personalizable en pdf.
    Este archivo tiene todas las funciones privadas y el bot que se debe llamar es:
        CreadorValePlantilla()

Gibran Valle
Revisión final: 14/03/2020
FUNCIONANDO CORRECTAMENTE
"""
from reportlab.lib.colors import black, transparent
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# ------------------------------------------- CONSTANTES ------------------------------------------------------------
# tamaños de hoja carta en cm
letter_width, letter_height = letter
# rayas perpendiculares
X1 = 4.25 * cm  # raya vertical 1
X2 = 9 * cm  # raya vertical 2
X3 = 10 * cm  # raya vertical 3
CENTRO_TITLE = 9 * cm
CENTRO_LABEL = 5.7 * cm
CENTRO_SYMBOL = 14 * cm
CENTRO_CONCEPTOS = 11 * cm
CENTRO_CUENTA = 6.5 * cm
CENTRO_NOMBRE = 11 * cm
CENTRO_IMPORTE = 15.6 * cm
# dimensiones
ALTURA_RENGLON = 0.7 * cm
LARGO_RENGLON = 12.5 * cm
ESPACIO = 0.5 * cm
SALTO_VALE = 3 * cm
# ajuste desconocido
AJUSTE = 0.2 * cm
# font size
SIZE_TITLE = 16
SIZE_TEXT = 13
SIZE_LABEL = 11
# LIMITES
LIMITE_CONCEPTOS_VALE_SIMPLE = 16
LIMITE_CONCEPTOS_VALE_DOBLE = 8
NOMBRE_DEFECTO = "vale_plantilla.pdf"
# VARIABLES
largo_cuenta = X1
largo_nombre = X2 - X1
largo_importe = LARGO_RENGLON - X2
largo_suma_importe = LARGO_RENGLON - X3
# margenes
margen_x = (letter_width - LARGO_RENGLON) / 2
# ------------------------ EDITAR PARA GENERAR EL VALE A TU GUSTO ------------------------------------------
VALES_POR_HOJA = 2
CONCEPTOS_EN_VALE_A = 1
CONCEPTOS_EN_VALE_B = 1


# ------------------------------- BOT PARA PROYECTO FINAL ---------------------------------------------
def CrearPlantillaVale(num_subvales, num_conceptos_vale_a, num_conceptos_vale_b, nombrePlantilla=NOMBRE_DEFECTO):
    """Crear una plantilla de vale personalizada para el proyectofinal

    :param num_subvales: 1 para vales simple, 2 para vale doble
    :param num_conceptos_vale_a: los conceptos en el vale simple o primer subvale
    :param num_conceptos_vale_b: los conceptos en el subvale 2, aplicable solo en vale doble
    :param nombrePlantilla: nombre de la plantilla pdf
    :return: guarda la plantilla en la raiz con el nombre: nombrePlantilla
    Gibran Valle
    Revisión final: 11/03/2020
    """
    debug = 0
    # 1) INICIAR EL CANVAS
    ruta = "plantillas/" + nombrePlantilla + ".pdf"
    cvs = canvas.Canvas(ruta, bottomup=0)
    cvs.setPageSize(letter)

    # ELEGIR EL COLOR DE CANVAS
    cvs.setStrokeColorRGB(0.7, 0.7, 0.7)  # choose your line color

    # CALCULAR MARGEN SUPERIOR
    tupla = calcularMargenY(num_subvales, num_conceptos_vale_a, num_conceptos_vale_b)
    altura_vale_a, margen_y, margen_y_final = tupla
    espacio_entre_vales = margen_y + altura_vale_a + SALTO_VALE + AJUSTE

    # CREAR LOS STRINGS
    status = creadorPlantilla(num_subvales, num_conceptos_vale_a, num_conceptos_vale_b, cvs, margen_y)

    # CREAR LAS FORMAS DINAMICAS
    forma(cvs, num_subvales, num_conceptos_vale_a, num_conceptos_vale_b, margen_y, espacio_entre_vales)

    # FINALIZAR GUARDANDO EL DOCUMENTO, SOLO SE PUEDE GUARDAR UNA VEZ
    cvs.save()
    if status:
        print("margen superior: {:.2f}".format(margen_y / cm)) if debug else 0
        print("margen inferior: {:.2f}".format(margen_y_final / cm)) if debug else 0
        print("Vale creado correctamente") if debug else 0
        return 1
    else:
        return -1


# -------------------------------FUNCIONES PRIVADAS PARA PROYECTO FINAL ---------------------------------------------
def roundedBox(canvas, x0=4.5 * cm, y0=2.5 * cm, width=12.5 * cm, heigh=1.63 * cm, linewidth=1.5, radius=0.25 * cm):
    canvas.setLineWidth(linewidth)
    canvas.roundRect(x0, y0, width, heigh, radius)


def rectInterna(canvas, x0, x1, y0, renglones, altura_renglon, linewidth=0.5, title=0):
    canvas.setLineWidth(linewidth)
    # escalar x1 razon desconocida
    x1 *= 1.355
    # empezar en x0, y0+altura renglon
    for i in range(1, renglones):
        canvas.setLineWidth(linewidth * 2.3) if (title == 1 and i == 1) else canvas.setLineWidth(linewidth)
        # x0,y0,x1,y1
        canvas.line(x0, y0 + altura_renglon * i, x1, y0 + altura_renglon * i)


def creadorPlantilla(num_subvales, num_conceptos_vale_a, num_conceptos_vale_b, canvas, margen_y):
    debug = 0
    # VALIDAR DATOS
    status = validarDatos(num_subvales, num_conceptos_vale_a, num_conceptos_vale_b)
    if status == - 1:
        return - 1

    # 2) EMPEZAR A CALCULAR LA POSICION DE LOS BORDES
    for i in range(1, num_subvales + 1):
        if i == 2:
            num_conceptos = num_conceptos_vale_b
            y0 += SALTO_VALE
            print("creando segundo subvale") if debug else 0
        else:
            num_conceptos = num_conceptos_vale_a
            if num_subvales == 1:
                y0 = margen_y
            elif num_subvales == 2:
                y0 = margen_y
            print("creando primer subvale") if debug else 0
        # BORDE 1: IMPORTE_LETRA
        x0 = margen_x
        renglones = 2
        alto_borde = ALTURA_RENGLON * renglones
        roundedBox(canvas, x0=x0, y0=y0, width=LARGO_RENGLON, heigh=alto_borde)
        # HACER EL GRID INTERNO
        rectInterna(canvas, x0=x0, x1=LARGO_RENGLON, y0=y0, renglones=renglones, altura_renglon=ALTURA_RENGLON)
        # moverse 9cm y 10cm en x, para hacer 2 lineas verticales de y0 a y1
        canvas.line(x0 + 9 * cm, y0, x0 + 9 * cm, y0 + ALTURA_RENGLON)
        canvas.line(x0 + 10 * cm, y0, x0 + 10 * cm, y0 + ALTURA_RENGLON)

        # BORDE 2: CONCEPTO
        # editar y0
        y0 += alto_borde + ESPACIO
        renglones = 1 + num_conceptos
        alto_borde = ALTURA_RENGLON * renglones
        roundedBox(canvas, x0=x0, y0=y0, width=LARGO_RENGLON, heigh=alto_borde)
        # HACER EL GRID INTERNO
        rectInterna(canvas, x0=x0, x1=LARGO_RENGLON, y0=y0, renglones=renglones, altura_renglon=ALTURA_RENGLON, title=1)

        # BORDE 3: CARGUESE A
        # sólo editar y0
        y0 += alto_borde + ESPACIO * 2
        renglones = 4
        alto_borde = ALTURA_RENGLON * renglones
        roundedBox(canvas, x0=x0, y0=y0, width=LARGO_RENGLON, heigh=alto_borde)
        # HACER EL GRID INTERNO
        rectInterna(canvas, x0=x0, x1=LARGO_RENGLON, y0=y0, renglones=renglones, altura_renglon=ALTURA_RENGLON, title=1)
        # moverse 9cm y 10cm en x, para hacer 2 lineas verticales de y0 a y1
        canvas.line(x0 + X1, y0, x0 + X1, y0 + alto_borde)
        canvas.line(x0 + X2, y0, x0 + X2, y0 + alto_borde)

        # BORDE 4: FECHA Y FIRMA
        # sólo editar y0
        y0 += alto_borde + ESPACIO
        renglones = 2
        alto_borde = ALTURA_RENGLON * renglones
        roundedBox(canvas, x0=x0, y0=y0, width=LARGO_RENGLON, heigh=alto_borde)
        # HACER EL GRID INTERNO
        rectInterna(canvas, x0=x0, x1=LARGO_RENGLON, y0=y0, renglones=renglones, altura_renglon=ALTURA_RENGLON)
        # moverse 9cm y 10cm en x, para hacer 2 lineas verticales de y0 a y1
        canvas.line(x0 + X1, y0, x0 + X1, y0 + alto_borde)
        canvas.line(x0 + X2, y0, x0 + X2, y0 + alto_borde)

    return 1


def forma(canvas, num_subvales, num_conceptos_vale_a, num_conceptos_vale_b, margen_y, espacio_entre_vales):
    debug = 0
    # VALIDAR DATOS
    status = validarDatos(num_subvales, num_conceptos_vale_a, num_conceptos_vale_b)
    if status == - 1:
        return - 1
    # CREACION DE TEXTO ESTÁTICO

    form = canvas.acroForm
    for sub_vale in range(1, num_subvales + 1):
        offset = margen_y + AJUSTE if sub_vale == 1 else espacio_entre_vales

        # BOX 1 - FIJA
        canvas.setFont("Helvetica", SIZE_TITLE)
        xcentro = CENTRO_TITLE
        ycentro = offset + ALTURA_RENGLON / 2
        canvas.drawCentredString(xcentro, ycentro, "Comprobante de gastos")
        xcentro = CENTRO_SYMBOL
        canvas.drawCentredString(xcentro, ycentro, "$")
        # calcular salto de renglon (fija)
        sr = ALTURA_RENGLON * 2 + ESPACIO

        # BOX 2 - VARIABLE EN FUNCION DE CONCEPTOS
        xcentro = CENTRO_CONCEPTOS
        ycentro += sr
        canvas.setFont("Helvetica", SIZE_TEXT)
        canvas.drawCentredString(xcentro, ycentro, "Conceptos")
        # alternar entre vale 1 y vale 2
        renglones = num_conceptos_vale_a if sub_vale == 1 else num_conceptos_vale_b
        sr = ALTURA_RENGLON * renglones + 1 + ESPACIO * 2

        # LABEL - FIJA
        ycentro += sr
        xcentro = CENTRO_LABEL
        canvas.setFont("Helvetica", SIZE_LABEL)
        canvas.drawCentredString(xcentro, ycentro, "Carguese a:")
        sr = ALTURA_RENGLON

        # BOX 3 - FIJA
        ycentro += sr
        canvas.setFont("Helvetica", SIZE_TEXT)
        xcentro = CENTRO_CUENTA
        canvas.drawCentredString(xcentro, ycentro, "No. de cuenta")
        xcentro = CENTRO_NOMBRE
        canvas.drawCentredString(xcentro, ycentro, "Nombre")
        xcentro = CENTRO_IMPORTE
        canvas.drawCentredString(xcentro, ycentro, "Importe")
        sr = ESPACIO + ALTURA_RENGLON * 4

        # BOX 4 - FIJA
        ycentro += sr
        xcentro = CENTRO_CUENTA
        canvas.setFont("Helvetica", SIZE_TEXT)
        canvas.drawCentredString(xcentro, ycentro, "Fecha")
        xcentro = CENTRO_NOMBRE
        canvas.drawCentredString(xcentro, ycentro, "Autorizado por:")
        xcentro = CENTRO_IMPORTE
        canvas.drawCentredString(xcentro, ycentro, "Recibido:")

        # ------------------------------------- FORMAS --------------------------------------------------------------
        # PRIMER BOX
        nombre = "Importe" if sub_vale == 1 else "Importe2"
        print("offset: {}".format(offset / cm)) if debug else 0
        y0 = letter_height - ALTURA_RENGLON - offset + AJUSTE
        x0 = margen_x + LARGO_RENGLON - largo_suma_importe
        form.textfield(name=nombre, tooltip='$100.00', x=x0, y=y0,
                       width=largo_suma_importe, borderWidth=0, height=ALTURA_RENGLON, fillColor=transparent,
                       textColor=black, forceBorder=False)
        nombre = "ImporteLetra" if sub_vale == 1 else "ImporteLetra2"
        y0 -= ALTURA_RENGLON
        x0 = margen_x
        form.textfield(name=nombre, tooltip='cien pesos 00/100 m.n.', x=x0, y=y0,
                       width=LARGO_RENGLON, borderWidth=0, height=ALTURA_RENGLON, fillColor=transparent,
                       textColor=black,
                       forceBorder=False)
        y0 = y0 - ALTURA_RENGLON * 2 - ESPACIO
        print("posicion: {}".format(y0 / cm)) if debug else 0

        # SEGUNDO BOX
        # RENGLONES DE CONCEPTOS
        renglones = num_conceptos_vale_a if sub_vale == 1 else num_conceptos_vale_b
        for num_concepto in range(1, renglones + 1):
            print("conceptos: {}".format(num_concepto)) if debug else 0
            # forma de conceto enesimo
            concepto = switch_concepto(num_concepto, sub_vale)
            print("nombre: {}".format(concepto)) if debug else 0
            form.textfield(name=concepto, tooltip='taxi hospital - terminal $50.00', x=x0, y=y0,
                           width=LARGO_RENGLON, borderWidth=0, height=ALTURA_RENGLON, fillColor=transparent,
                           textColor=black,
                           forceBorder=False)
            y0 -= ALTURA_RENGLON
        y0 -= ESPACIO * 2

        # TERCER BOX
        for renglon in range(1, 4):
            cuenta = switch_cuenta(renglon, sub_vale)
            y = y0 - ALTURA_RENGLON * renglon
            form.textfield(name=cuenta, tooltip='', x=margen_x,
                           y=y,
                           width=largo_cuenta, borderWidth=0, height=ALTURA_RENGLON, fillColor=transparent,
                           textColor=black,
                           forceBorder=False)

            nombre = switch_nombre(renglon, sub_vale)
            form.textfield(name=nombre, tooltip='', x=margen_x + X1,
                           y=y,
                           width=largo_nombre, borderWidth=0, height=ALTURA_RENGLON, fillColor=transparent,
                           textColor=black,
                           forceBorder=False)

            importe = switch_importe(renglon, sub_vale)
            form.textfield(name=importe, tooltip='', x=margen_x + X2,
                           y=y,
                           width=largo_importe, borderWidth=0, height=ALTURA_RENGLON, fillColor=transparent,
                           textColor=black,
                           forceBorder=False)
        y0 -= (ALTURA_RENGLON * 4 + ESPACIO)

        # CUARTO BOX
        y = y0 - ALTURA_RENGLON
        nombre = "Fecha" if sub_vale == 1 else "Fecha2"
        form.textfield(name=nombre, tooltip='', x=margen_x,
                       y=y,
                       width=largo_cuenta, borderWidth=0, height=ALTURA_RENGLON, fillColor=transparent,
                       textColor=black,
                       forceBorder=False)

        nombre = "Autorizado" if sub_vale == 1 else "Autorizado2"
        form.textfield(name=nombre, tooltip='', x=margen_x + X1,
                       y=y,
                       width=largo_nombre, borderWidth=0, height=ALTURA_RENGLON, fillColor=transparent,
                       textColor=black,
                       forceBorder=False)

        nombre = "Recibido" if sub_vale == 1 else "Recibido2"
        form.textfield(name=nombre, tooltip='', x=margen_x + X2,
                       y=y,
                       width=largo_importe, borderWidth=0, height=ALTURA_RENGLON, fillColor=transparent,
                       textColor=black,
                       forceBorder=False)


def calcularMargenY(vales, conceptosA, conceptosB):
    # para calcular el margen automatico
    debug = 0
    print("hacer {} vales con CA: {} CB: {}".format(vales, conceptosA, conceptosB)) if debug else 0
    altura_vale_a = ESPACIO * 4 + ALTURA_RENGLON * (7 + conceptosA)
    if vales == 2:
        altura_vale_b = ESPACIO * 4 + ALTURA_RENGLON * (7 + conceptosB)
        altura_vales = altura_vale_a + altura_vale_b + SALTO_VALE * 1.5
    else:
        altura_vale_b = 0
        altura_vales = altura_vale_a + altura_vale_b + SALTO_VALE
    margen_y_calculado = (letter_height - altura_vales) / 2
    margen_y_final = letter_height - altura_vales - margen_y_calculado

    return altura_vale_a, margen_y_calculado, margen_y_final


# implementación de un switch en python
def switch_concepto(num_concepto, sub_vale):
    sufijo = "" if sub_vale == 1 else "2"
    switcher = {
        1: "ConceptoA" + sufijo,
        2: "ConceptoB" + sufijo,
        3: "ConceptoC" + sufijo,
        4: "ConceptoD" + sufijo,
        5: "ConceptoE" + sufijo,
        6: "ConceptoF" + sufijo,
        7: "ConceptoG" + sufijo,
        8: "ConceptoH" + sufijo,
        9: "ConceptoI" + sufijo,
        10: "ConceptoJ" + sufijo,
        11: "ConceptoK" + sufijo,
        12: "ConceptoL" + sufijo,
        13: "ConceptoM" + sufijo,
        14: "ConceptoN" + sufijo,
        15: "ConceptoO" + sufijo,
    }
    return switcher.get(num_concepto, "concepto invalido")


def switch_cuenta(num_cuenta, sub_vale):
    sufijo = "" if sub_vale == 1 else "2"
    switcher = {
        1: "No de Cuenta A" + sufijo,
        2: "No de Cuenta B" + sufijo,
        3: "No de Cuenta C" + sufijo,
    }
    return switcher.get(num_cuenta, "cuenta invalida")


def switch_nombre(num_nombre, sub_vale):
    sufijo = "" if sub_vale == 1 else "2"
    switcher = {
        1: "NombreA" + sufijo,
        2: "NombreB" + sufijo,
        3: "NombreC" + sufijo,
    }
    return switcher.get(num_nombre, "cuenta invalida")


def switch_importe(num_importe, sub_vale):
    sufijo = "" if sub_vale == 1 else "2"
    switcher = {
        1: "ImporteA" + sufijo,
        2: "ImporteB" + sufijo,
        3: "ImporteC" + sufijo,
    }
    return switcher.get(num_importe, "cuenta invalida")


def validarDatos(num_subvales, num_conceptos_vale_a, num_conceptos_vale_b):
    # VALIDACION DE PARAMETROS
    if num_subvales == 1 and num_conceptos_vale_a > LIMITE_CONCEPTOS_VALE_SIMPLE:
        print("ERROR: VALE DEMASIADO GRANDE")
        return -1
    elif num_subvales == 2 and (num_conceptos_vale_a + num_conceptos_vale_b) > LIMITE_CONCEPTOS_VALE_DOBLE:
        print("ERROR: VALE DEMASIADO GRANDE")
        return -1
    elif num_subvales > 2:
        print("ERROR: VALE DEMASIADO GRANDE")
        return -1
