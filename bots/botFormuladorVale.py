"""
Las funciones de este bot son las siguientes:
    1)  Extrae los datos de los vales que se deben crear
    2)  Crea un diccionario con los datos obtenidos
    3)  Llena los formularios correspondientes con la nomenclatura:
        "vale + fecha + .pdf"
    4)  Se guarda en la carpeta outputs

Gibran Valle
Revisión final: 14/03/2020

Nota:
        Se acaba de agregar el generador de plantillas
        Ya no es necesario precargar vales hechos
        Permite más libertad de personalización

        Este es el bot más complejo de tooooodo el proyecto *FUNCIONANDO*
"""

import pdfrw

from bots.botContador import numero_a_texto as num2wrd
from bots.botEstructurador import estructurarImporteNegativo as ein
from bots.botCreadorVale import CrearPlantillaVale as cpv
import string

# CARACTERES MAXIMO
MAXIMOS_RENGLON_ENTERO = 87
MAXIMOS_RENGLON_ENTERO_LETRA = 77
MAXIMOS_RENGLON_FECHA = 25
MAXIMOS_RENGLON_IMPORTE = 15
MAXIMOS_RENGLON_USUARIO = 20


# ----------------------------- FUNCIONES LLAMADAS DESDE EL MAIN ---------------------------------------------
def llenarVales(vales, usuario):
    """ Llena la plantilla que ahora se va a generar automáticamente
    :param vales:  cuantas hojas de vales se van a generar y posteriormente llenar
    :param usuario:  el nombre de la persona a quien se eroga el vale
    :return:    genera el archivo pdf en el directorio outputs
                con el nombre vale + fecha de gasto +.pdf
    """
    debug = 1
    # filtra solo estas columnas
    valores = vales[["fecha", "semana", "dia", "concepto", "detalles", "importe", "grupo"]]

    # invertir indice del dataframe
    valores = valores.iloc[::-1]

    # reset al index para poder iterar
    valores.reset_index(drop=True, inplace=True)
    print("valores: ")
    print(valores.head())
    # SEPARAR EN VALES DIARIOS, MAXIMO 3 CONCEPTOS POR DIA Y AGRUPAR POR SEMANA
    conceptos_totales = len(valores.fecha)
    lista_vales = botSeparador(valores, conceptos_totales)
    print(
        "{} conceptos no deducibles\nlista de vales separador por dia: {}\n".format(conceptos_totales, lista_vales)) \
        if debug else 0

    # AGRUPA LOS VALES, MAXIMO 2 VALES POR HOJA
    vales_agrupados = botAgrupador(lista_vales)

    # LLENAR LAS LISTAS DE DATOS, CREAR DICCIONARIOS Y LLENAR FORMULARIO PDF
    botCreadorVales(vales_agrupados, valores, usuario)


# ---------------------- BOTS QUE YA FUNCIONAN Y ESTAN PROBADOS ------------------------------------
def botCreadorVales(vales_agrupados, valores, usuario):
    # FUNCIONANDO OK
    print(valores)
    # recordar el indice donde se quedó en cada iteración
    # INSTANCIAR VARIABLES
    index = 0
    debug = 0
    suma = 0

    # VARIABLES DEL SUBVALE 1 DE 2
    fecha = ""
    conceptoA = ""
    conceptoB = ""
    conceptoC = ""
    conceptoD = ""
    conceptoE = ""
    conceptoF = ""
    conceptoG = ""
    conceptoH = ""
    conceptoI = ""
    conceptoJ = ""
    conceptoK = ""
    conceptoL = ""
    conceptoM = ""
    conceptoN = ""
    conceptoO = ""
    saldo_diario = ""

    # VARIABLES DEL SUBVALE 2 DE 2
    conceptoA2 = ""
    conceptoB2 = ""
    conceptoC2 = ""
    conceptoD2 = ""
    conceptoE2 = ""
    conceptoF2 = ""
    conceptoG2 = ""
    conceptoH2 = ""
    conceptoI2 = ""
    conceptoJ2 = ""
    conceptoK2 = ""
    conceptoL2 = ""
    conceptoM2 = ""
    conceptoN2 = ""
    conceptoO2 = ""
    saldo_diario2 = ""
    fecha2 = ""

    # VARIABLES DEL SUBVALE 1 DE 1
    conceptoA3 = ""
    conceptoB3 = ""
    conceptoC3 = ""
    conceptoD3 = ""
    conceptoE3 = ""
    conceptoF3 = ""
    conceptoG3 = ""
    conceptoH3 = ""
    conceptoI3 = ""
    conceptoJ3 = ""
    conceptoK3 = ""
    conceptoL3 = ""
    conceptoM3 = ""
    conceptoN3 = ""
    conceptoO3 = ""
    saldo_diario3 = ""
    fecha3 = ""

    # ITERAR POR CADA HOJA DE VALE PARA LLENAR EL DICCIONARIO NECESARIO PARA LLENAR LA PLANTILLA PDF
    for hoja, key in enumerate(vales_agrupados, 1):
        value = vales_agrupados[key]

        # ITERAR PARA ENCONTRAR EL TAMAÑO DEL SUBVALE
        contador = 0
        for i, v in enumerate(value):
            # print("i: {} v: {}".format(i, v))
            if v > 0:
                contador += 1
                # print("contador: {}".format(contador))

        print("size: {} values: {}".format(contador, value)) if debug else 0
        size = contador

        # extraer de la tupla
        conceptosA, conceptosB = value

        nombre = "vale" + str(hoja)
        print("\nhoja: {}, value: {}, size: {}".format(hoja, value, size)) if debug else 0
        print("conceptosA: {}, conceptosB: {}".format(conceptosA, conceptosB)) if debug else 0

        """
        #  ----------  AQUI SE CREA LA PLANTILLA PARA EL VALE --------------- 
        """
        status = cpv(size, conceptosA, conceptosB, nombre)
        if status:
            print("VALE CREADO CORRECTAMENTE\n") if debug else 0

        # CREAR UN DICCIONARIO DOBLE
        if size == 2:
            # botCreadorValesDoble_Test()
            # intentar iterar por cada valor
            # sumar los conceptos que tiene
            conceptos_por_vale = sum(value)

            print("{} conceptos por vale doble".format(conceptos_por_vale)) if debug else 0
            # cada vale doble cuenta con 2 subvales individuales iterar por cada uno
            for subvale, conceptos_por_subvale in enumerate(value):
                suma = 0
                print("hoja:{} subvale: {}, conceptos por subvale: {}".format(hoja, subvale,
                                                                              conceptos_por_subvale)) if debug else 0
                # ahora iterar por cada concepto
                for concepto_index in range(1, conceptos_por_subvale + 1):
                    print("concepto: {}, index: {}".format(concepto_index, index)) if debug else 0

                    if subvale == 0:
                        concepto = valores.concepto[index]
                        detalle = valores.detalles[index]
                        importe = -1 * valores.importe[index]
                        suma += importe
                        importe = str(importe)
                        if concepto_index == 1:
                            fecha = valores.fecha[index]
                            fecha = fecha.center(MAXIMOS_RENGLON_FECHA)
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoA = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoA: {}".format(conceptoA)) if debug else 0
                        elif concepto_index == 2:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoB = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoB: {}".format(conceptoB)) if debug else 0
                        elif concepto_index == 3:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoC = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoC: {}".format(conceptoC)) if debug else 0
                        elif concepto_index == 4:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoD = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoD: {}".format(conceptoD)) if debug else 0
                        elif concepto_index == 5:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoE = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoE: {}".format(conceptoE)) if debug else 0
                        elif concepto_index == 6:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoF = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoF: {}".format(conceptoF)) if debug else 0
                        elif concepto_index == 7:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoG = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoG: {}".format(conceptoG)) if debug else 0
                        elif concepto_index == 8:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoH = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoH: {}".format(conceptoH)) if debug else 0
                        elif concepto_index == 9:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoI = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoI: {}".format(conceptoI)) if debug else 0
                        elif concepto_index == 10:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoJ = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoJ: {}".format(conceptoJ)) if debug else 0
                        elif concepto_index == 11:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoK = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoK: {}".format(conceptoK)) if debug else 0
                        elif concepto_index == 12:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoL = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoL: {}".format(conceptoL)) if debug else 0
                        elif concepto_index == 13:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoM = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoM: {}".format(conceptoM)) if debug else 0
                        elif concepto_index == 14:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoN = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoN: {}".format(conceptoN)) if debug else 0
                        elif concepto_index == 15:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoO = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoO: {}".format(conceptoO)) if debug else 0

                        # sumar los importes por concepto para generar el importe diario
                        saldo_diario = suma
                        print("saldo diario: {}".format(saldo_diario)) if debug else False
                    if subvale == 1:
                        concepto = valores.concepto[index]
                        detalle = valores.detalles[index]
                        importe = -1 * valores.importe[index]
                        suma = importe if concepto == 1 else suma + importe
                        importe = str(importe)
                        if concepto_index == 1:
                            fecha2 = valores.fecha[index]
                            fecha2 = fecha2.center(MAXIMOS_RENGLON_FECHA)
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoA2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoA: {}".format(conceptoA)) if debug else 0
                        elif concepto_index == 2:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoB2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoB: {}".format(conceptoB)) if debug else 0
                        elif concepto_index == 3:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoC2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoC: {}".format(conceptoC)) if debug else 0
                        elif concepto_index == 4:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoD2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoD: {}".format(conceptoD)) if debug else 0
                        elif concepto_index == 5:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoE2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoE: {}".format(conceptoE)) if debug else 0
                        elif concepto_index == 6:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoF2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoF: {}".format(conceptoF)) if debug else 0
                        elif concepto_index == 7:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoG2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoG: {}".format(conceptoG)) if debug else 0
                        elif concepto_index == 8:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoH2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoH: {}".format(conceptoH)) if debug else 0
                        elif concepto_index == 9:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoI2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoI: {}".format(conceptoI)) if debug else 0
                        elif concepto_index == 10:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoJ2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoJ: {}".format(conceptoJ)) if debug else 0
                        elif concepto_index == 11:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoK2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoK: {}".format(conceptoK)) if debug else 0
                        elif concepto_index == 12:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoL2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoL: {}".format(conceptoL)) if debug else 0
                        elif concepto_index == 13:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoM2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoM: {}".format(conceptoM)) if debug else 0
                        elif concepto_index == 14:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoN2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoN: {}".format(conceptoN)) if debug else 0
                        elif concepto_index == 15:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoO2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoO: {}".format(conceptoO)) if debug else 0
                        # sumar los importes por concepto para generar el importe diario
                        saldo_diario2 = suma
                        print("saldo diario: {}".format(saldo_diario2)) if debug else False

                    # aumentar el index
                    index += 1
                    print("index: {}".format(index)) if debug else 0

            # LLENAR TUPLA CON LOS DATOS DE CADA SUBVALE
            datos_subvale0 = (fecha, conceptoA, conceptoB, conceptoC, conceptoD, conceptoE, conceptoF,
                              conceptoG, conceptoH, conceptoI, conceptoJ, conceptoK, conceptoL,
                              conceptoM, conceptoN, conceptoO, saldo_diario)
            print("datos val0: {}".format(datos_subvale0)) if debug else False
            datos_subvale1 = (fecha2, conceptoA2, conceptoB2, conceptoC2, conceptoD2, conceptoE2, conceptoF2,
                              conceptoG2, conceptoH2, conceptoI2, conceptoJ2, conceptoK2, conceptoL2,
                              conceptoM2, conceptoN2, conceptoO2, saldo_diario2)
            print("datos val1: {}".format(datos_subvale1)) if debug else False
            # LLENAR TUPLA PARA EL VALE
            datos_vale_doble = (datos_subvale0, datos_subvale1)
            # LLENAR EL DICCIONARIO CON LOS DATOS DEL VALE
            diccionario_doble = botllenadordiccionarioDoble(datos_vale_doble, usuario)
            print("el diccionario doble queda: {}".format(diccionario_doble)) if debug else False
            # LLENAR LA PLANTILLA GENERADA ANTERIORMENTE
            status = botllenadorPlantillas(nombre, diccionario_doble)
            if status:
                print("VALE LLENADO CORRECTAMENTE") if debug else False

        # CREAR UN DICCIONARIO SIMPLE
        elif size == 1:
            # reiniciar la suma
            suma = 0
            conceptos_por_vale_simple = sum(value)

            print("conceptos a iterar: {}".format(conceptos_por_vale_simple)) if debug else 0
            print("{} conceptos por vale simple".format(conceptos_por_vale)) if debug else 0
            # cada vale simple cuenta con 1 subvale individual no es necesario iterar
            subvale = 0
            print("hoja: {} subvale{}, conceptos por subvale: {}".
                  format(hoja, subvale, conceptos_por_vale_simple)) if debug else 0

            for concepto_index in range(1, conceptos_por_vale_simple + 1):
                print("\nconcepto: {}, index: {}".format(concepto, index)) if debug else 0
                concepto = valores.concepto[index]
                detalle = valores.detalles[index]
                importe = -1 * valores.importe[index]
                suma += importe
                importe = str(importe)
                print(" VALE SENCILLO") if debug else 0
                print("VALORES: {} {} {} ".format(concepto, detalle, importe)) if debug else False
                if concepto_index == 1:
                    fecha3 = valores.fecha[index]
                    fecha3 = fecha3.center(MAXIMOS_RENGLON_FECHA)
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoA3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoA: {}".format(conceptoA)) if debug else 0
                elif concepto_index == 2:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoB3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoB: {}".format(conceptoB)) if debug else 0
                elif concepto_index == 3:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoC3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoC: {}".format(conceptoC)) if debug else 0
                elif concepto_index == 4:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoD3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoD: {}".format(conceptoD)) if debug else 0
                elif concepto_index == 5:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoE3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoE: {}".format(conceptoE)) if debug else 0
                elif concepto_index == 6:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoF3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoF: {}".format(conceptoF)) if debug else 0
                elif concepto_index == 7:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoG3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoG: {}".format(conceptoG)) if debug else 0
                elif concepto_index == 8:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoH3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoH: {}".format(conceptoH)) if debug else 0
                elif concepto_index == 9:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoI3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoI: {}".format(conceptoI)) if debug else 0
                elif concepto_index == 10:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoJ3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoJ: {}".format(conceptoJ)) if debug else 0
                elif concepto_index == 11:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoK3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoK: {}".format(conceptoK)) if debug else 0
                elif concepto_index == 12:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoL3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoL: {}".format(conceptoL)) if debug else 0
                elif concepto_index == 13:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoM3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoM: {}".format(conceptoM)) if debug else 0
                elif concepto_index == 14:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoN3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoN: {}".format(conceptoN)) if debug else 0
                elif concepto_index == 15:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoO3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoO: {}".format(conceptoO)) if debug else 0

                # sumar los importes por concepto para generar el importe diario
                saldo_diario3 = suma
                print("saldo diario: {}".format(saldo_diario3)) if debug else False
                # aumentar el index
                index += 1
                print("index: {}".format(index)) if debug else 0

            # LLENAR TUPLA CON LOS DATOS DE CADA SUBVALE
            datos_vale_simple = (fecha3, conceptoA3, conceptoB3, conceptoC3, conceptoD3, conceptoE3, conceptoF3,
                                 conceptoG3, conceptoH3, conceptoI3, conceptoJ3, conceptoK3, conceptoL3,
                                 conceptoM3, conceptoN3, conceptoO3, saldo_diario3)
            # LLENAR EL DICCIONARIO SIMPLE CON LOS DATOS
            diccionario_simple = botllenadordiccionarioSimple(datos_vale_simple, usuario)
            print("el diccionario simple queda: {}".format(diccionario_simple)) if debug else 0
            # LLENAR LA PLANTILLA GENERADA ANTERIORMENTE
            status = botllenadorPlantillas(nombre, diccionario_simple)
            if status:
                print("VALE LLENADO CORRECTAMENTE") if debug else 0


def botAgrupador(lista_vales):
    """
    Probada 01/06
    Ordena la lista de vales y decide cuantos vales generar, asi como si serán dobles o simples
    Deben de pertenecer a la misma ruta y semana para estar dentro de un mismo vale
    Deben ser del mismo dia para aparecer dentro del mismo subvale
    :param lista_vales: lista de conceptos por subvale
    :return: diccionario con los conceptos agruapdos,
    """
    debug = 0
    diccionario = {}
    size = len(lista_vales)
    print("tamaño: {}".format(size))

    # FUNCION 1, ORDENAR VALES
    vale_doble = 0
    vale_simple = 0
    orden = []
    for index, concepto in enumerate(lista_vales):

        if index % 2 > 0:
            print("\nindex par") if debug else 0
            print(concepto) if debug else 0

            if concepto > 0:
                print("vale doble") if debug else 0
                vale_doble += 1
                orden.append(2)

            else:
                print("vale simple") if debug else 0
                vale_simple += 1
                orden.append(1)

    print("se llenarán {} vales dobles y {} vales simples".format(vale_doble, vale_simple)) if debug else 0
    print("el orden es: {}".format(orden)) if debug else 0

    # FUNCION DOS, CREAR DICCIONARIO
    contador = 0
    index = 0
    print("\n Nueva funcion \n")
    for sub_index, conceptos in enumerate(orden):
        print("subindex: {} conceptos: {}".format(sub_index, conceptos)) if debug else 0
        if conceptos == 2:
            vector_i = lista_vales[index:index + conceptos]
            index += conceptos
            # AGREGAR AL DICCIONARIO
            contador += 1
            llave_i = "vale" + str(sub_index + 1)
            diccionario.update({llave_i: vector_i})

            if debug:
                print("hacer vale doble")
                print(vector_i)
                print("creando la key con nombre: {}".format(llave_i))
            # print("diccionario actualizado: {}".format(diccionario))

        else:
            vector_i = [lista_vales[index], 0]
            index += conceptos + 1
            # AGREGAR AL DICCIONARIO
            contador += 1
            llave_i = "vale" + str(sub_index + 1)
            diccionario.update({llave_i: vector_i})

            if debug:
                print("hacer vale simple")
                print(vector_i)
                print("creando la key con nombre: {}".format(llave_i))
                # print("diccionario actualizado: {}".format(diccionario))

    print("diccionario actualizado: {}".format(diccionario)) if debug else 0
    return diccionario


def botSeparador(valores, conceptos_totales):
    """
    Extraer valores indexados de la lista valores,
    :param valores: dataframe
    :param conceptos_totales:
    :return: lista de numero de conceptos por vale, la longitud de la lista debe ser par.
    """
    # SEPARA RUTA, SEMANA, DIA... 31/05/20
    index = 0
    semana_anterior = 0
    dia_anterior = 0
    ruta_anterior = 0
    contador_conceptos = 0
    lista = []
    debug = 1
    print("\n botFormuladorVale botSeparador \n") if debug else 0

    for concepto in range(conceptos_totales):
        semana = valores.semana[concepto]
        dia = valores.dia[concepto]
        fecha = valores.fecha[concepto]
        ruta = valores.grupo[concepto]

        if concepto == 0:  # inicio de iteración
            contador_conceptos = 1
            index = 0
            semana_anterior = semana
            dia_anterior = dia
            ruta_anterior = ruta
            if debug:
                print("inicio")
                print(fecha)
                print(
                    "semana: {}, dia: {}, index: {}, concepto: {}\n".format(semana, dia, concepto, contador_conceptos))

        elif concepto > 0:  # duracion de iteracion

            if ruta == ruta_anterior:
                print("Misma ruta") if debug else 0

                if semana == semana_anterior:
                    print("misma semana") if debug else 0

                    if dia == dia_anterior:
                        contador_conceptos += 1
                        if debug:
                            print("y mismo dia")
                            print(fecha)
                            print(ruta)
                            print("semana: {}, dia: {}, index: {}, concepto: {}\n".format(semana, dia, concepto,
                                                                                          contador_conceptos)) \
 \
                    else:  # dia diferente
                        lista.append(contador_conceptos)
                        index += 1
                        contador_conceptos = 1
                        dia_anterior = dia

                        if debug:
                            print(lista)
                            print("inicia nuevo dia")
                            print(fecha)
                            print(ruta)
                            print("semana: {}, dia: {}, index: {}, concepto: {}\n".format(semana, dia, concepto,
                                                                                          contador_conceptos))

                        if concepto == conceptos_totales - 1:
                            print("FINAL")
                            lista.append(contador_conceptos)

                            largo = len(lista)
                            if largo % 2 > 0:
                                print("CADENA IMPAR, completar con 0")
                                lista.append(0)

                else:  # semana diferente
                    lista.append(contador_conceptos)
                    index += 1
                    contador_conceptos = 1
                    semana_anterior = semana
                    if debug:
                        print(lista)
                        print("inicia otra semana")
                        print(fecha)
                        print(ruta)
                        print("semana: {}, dia: {}, index: {}, concepto: {}\n".format(semana, dia, concepto,
                                                                                      contador_conceptos))

            else:  # ruta diferente
                lista.append(contador_conceptos)
                size = len(lista)
                if size % 2 > 0:
                    print("impar, llenar con 0") if debug else 0
                lista.append(0)
                index += 1
                contador_conceptos = 1
                ruta_anterior = ruta
                semana_anterior = semana
                dia_anterior = dia
                if debug:
                    print(lista)
                    print("inicia otra ruta")
                    print(fecha)
                    print(ruta)
                    print("semana: {}, dia: {}, index: {}, concepto: {}\n".format(semana, dia, concepto,
                                                                                  contador_conceptos))

    return lista


def botllenadorPlantillas(nombre_plantilla, diccionario):
    """
    REEMPLAZA A LAS FUNCIONES:
        botllenadorPlantillaValeSimple
        botllenadorPlantillaValeDoble
    :param nombre_plantilla: archivo .pdf creado con el botCreadorVale
    :param diccionario: el diccionario creado con el botllenadorDiccionario
    :return: llena la plantilla, retorna 1 si se creó exitosamente de lo contrario -1
    """
    fecha = diccionario.get("Fecha")
    fecha = fecha.replace("/", "-")
    fecha = fecha.replace(" ", "")

    # FECHA FINAL PARA VALE DOBLE
    fecha2 = diccionario.get("Fecha2", "")
    fecha2 = fecha2.replace("/", "-")
    fecha2 = fecha2.replace(" ", "")

    # EL NOMBRE ES UN INTERVALO PARA LOS VALES DOBLES
    nombre = fecha
    if len(fecha2) > 0:
        nombre = fecha + " y " + fecha2

    nombre_entrada = "plantillas/" + nombre_plantilla + ".pdf"
    nombre_salida = "outputs/vale-" + nombre + ".pdf"
    botllenadorForma(nombre_entrada, nombre_salida, diccionario)
    return 1


def botllenadordiccionarioSimple(datos_simples, usuario):
    # FUNCIONANDO OK
    fecha, conceptoA, conceptoB, conceptoC, conceptoD, conceptoE, conceptoF, \
    conceptoG, conceptoH, conceptoI, conceptoJ, conceptoK, conceptoL, \
    conceptoM, conceptoN, conceptoO, importe = datos_simples
    importe_letra = num2wrd(float(importe))
    # centrar
    importe_letra = importe_letra.center(MAXIMOS_RENGLON_ENTERO_LETRA)
    usuario = usuario.center(MAXIMOS_RENGLON_USUARIO)
    importe = str(importe)
    importe = importe.center(MAXIMOS_RENGLON_IMPORTE)
    diccionario = {
        'Importe': importe,
        'ImporteLetra': importe_letra,
        'ConceptoA': conceptoA,
        'ConceptoB': conceptoB,
        'ConceptoC': conceptoC,
        'ConceptoD': conceptoD,
        'ConceptoE': conceptoE,
        'ConceptoF': conceptoF,
        'ConceptoG': conceptoG,
        'ConceptoH': conceptoH,
        'ConceptoI': conceptoI,
        'ConceptoJ': conceptoJ,
        'ConceptoK': conceptoK,
        'ConceptoL': conceptoL,
        'ConceptoM': conceptoM,
        'ConceptoN': conceptoN,
        'ConceptoO': conceptoC,
        "Fecha": fecha,
        "Recibido": usuario,
    }
    return diccionario


def botllenadordiccionarioDoble(datos_dobles, usuario):
    # FUNCIONANDO OK
    datos_uno, datos_dos = datos_dobles
    fecha, conceptoA, conceptoB, conceptoC, conceptoD, conceptoE, conceptoF, \
    conceptoG, conceptoH, conceptoI, conceptoJ, conceptoK, conceptoL, \
    conceptoM, conceptoN, conceptoO, importe = datos_uno
    fecha2, conceptoA2, conceptoB2, conceptoC2, conceptoD2, conceptoE2, conceptoF2, \
    conceptoG2, conceptoH2, conceptoI2, conceptoJ2, conceptoK2, conceptoL2, \
    conceptoM2, conceptoN2, conceptoO2, importe2 = datos_dos

    importe_letra = num2wrd(float(importe))
    importe_letra2 = num2wrd(float(importe2))

    # centrar
    importe_letra = importe_letra.center(MAXIMOS_RENGLON_ENTERO_LETRA)
    importe = str(importe)
    importe = importe.center(MAXIMOS_RENGLON_IMPORTE)
    # centrar
    importe_letra2 = importe_letra2.center(MAXIMOS_RENGLON_ENTERO_LETRA)
    usuario = usuario.center(MAXIMOS_RENGLON_USUARIO)
    importe2 = str(importe2)
    importe2 = importe2.center(MAXIMOS_RENGLON_IMPORTE)
    diccionario = {
        'Importe': importe,
        'ImporteLetra': importe_letra,
        'ConceptoA': conceptoA,
        'ConceptoB': conceptoB,
        'ConceptoC': conceptoC,
        'ConceptoD': conceptoD,
        'ConceptoE': conceptoE,
        'ConceptoF': conceptoF,
        'ConceptoG': conceptoG,
        'ConceptoH': conceptoH,
        'ConceptoI': conceptoI,
        'ConceptoJ': conceptoJ,
        'ConceptoK': conceptoK,
        'ConceptoL': conceptoL,
        'ConceptoM': conceptoM,
        'ConceptoN': conceptoN,
        'ConceptoO': conceptoC,
        "Fecha": fecha,
        "Recibido": usuario,

        'Importe2': importe2,
        'ImporteLetra2': importe_letra2,
        'ConceptoA2': conceptoA2,
        'ConceptoB2': conceptoB2,
        'ConceptoC2': conceptoC2,
        'ConceptoD2': conceptoD2,
        'ConceptoE2': conceptoE2,
        'ConceptoF2': conceptoF2,
        'ConceptoG2': conceptoG2,
        'ConceptoH2': conceptoH2,
        'ConceptoI2': conceptoI2,
        'ConceptoJ2': conceptoJ2,
        'ConceptoK2': conceptoK2,
        'ConceptoL2': conceptoL2,
        'ConceptoM2': conceptoM2,
        'ConceptoN2': conceptoN2,
        'ConceptoO2': conceptoC2,
        "Fecha2": fecha2,
        "Recibido2": usuario,
    }
    return diccionario


def botllenadorForma(input_pdf_path, output_pdf_path, data_dict):
    # FUNCIONANDO OK
    ANNOT_KEY = '/Annots'
    ANNOT_FIELD_KEY = '/T'
    ANNOT_VAL_KEY = '/V'
    ANNOT_RECT_KEY = '/Rect'
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'
    pantilla_formulario = "plantillas/vale_pantilla.pdf"
    pantilla_salida = "plantillas/vale.pdf"

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    annotations = template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                    )
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


# ----------------------- FUNCIONES OBSOLETAS NO INCLUIR EN NOTEBOOKS ----------------------------------------------
# OBSOLETA
def botllenadorPlantillaValeSimple(diccionario):
    """
    ESTA FUNCION ES OBSOLETA USAR botllenadorPlantillas en su lugar
    :param diccionario:
    :return:
    """
    fecha = diccionario["Fecha"]
    fecha = fecha.replace("/", "-")
    botllenadorForma("plantillas/vale_plantilla.pdf", "outputs/vale-" + fecha + ".pdf", diccionario)


#OBSOLETA
def botllenadorPlantillaValeDoble(diccionario):
    """
    ESTA FUNCION ES OBSOLETA USAR botllenadorPlantillas en su lugar
    :param diccionario:
    :return:
    """
    fecha = diccionario["Fecha"]
    fecha = fecha.replace("/", "-")
    botllenadorForma("plantillas/vales_plantilla.pdf", "outputs/vales-" + fecha + ".pdf", diccionario)


#OBSOLETA
def botCreadorValesSimple(concepto_por_vale, valores, usuario):
    """
    OBSOLETA
    :param concepto_por_vale:
    :param valores:
    :param usuario:
    :return:
    """
    # recuperar valores segun la lista de vales_al_dia
    conceptoA = ""
    conceptoB = ""
    conceptoC = ""
    total_dia = ""
    fecha = ""
    total = 0

    for j in concepto_por_vale:
        # PRIMER VALE
        if j == 0:  # CREAR EL CONCEPTO A
            fecha = valores.fecha[j]
            concepto = valores.concepto[j]
            detalle = valores.detalles[j]
            importe = ein(valores.importe[j])
            conceptoA = concepto + ": " + detalle + " - " + importe
            total += -1 * valores.importe[j]
        elif j == 1:  # CONCEPTO B
            concepto = valores.concepto[j]
            detalle = valores.detalles[j]
            importe = ein(valores.importe[j])
            conceptoB = concepto + ": " + detalle + " - " + importe
            total += -1 * valores.importe[j]
        elif j == 2:  # CONCEPTO C
            concepto = valores.concepto[j]
            detalle = valores.detalles[j]
            importe = ein(valores.importe[j])
            conceptoC = concepto + ": " + detalle + " - " + importe
            total += -1 * valores.importe[j]

    # PRECURSOR DE DICCIONARIO
    datos = (fecha, conceptoA, conceptoB, conceptoC, total_dia)

    # LLENAR DICCIONARIO
    diccionario = botllenadordiccionarioSimple(datos, usuario)
    return diccionario


#OBSOLETA
def botCreadorValesDoble(concepto_por_vale, valores, usuario):
    """
    OBSOLETA
    :param concepto_por_vale:
    :param valores:
    :param usuario:
    :return:
    """
    print(valores)
    # recuperar valores segun la lista de vales_al_dia
    debug = 0
    suma = 0

    fecha = ""
    conceptoA = ""
    conceptoB = ""
    conceptoC = ""
    saldo_diario = ""

    conceptoA2 = ""
    conceptoB2 = ""
    conceptoC2 = ""
    saldo_diario2 = ""
    fecha2 = ""

    datos_uno = ()
    datos_dos = ()

    index_inicial = 0
    # index para un loop que no empieza en 0
    for index, i in enumerate(concepto_por_vale):
        suma = 0
        for j in range(concepto_por_vale[index]):
            # formula para encontrar el indice en el bucle
            count = j + concepto_por_vale[index] * index

            if index == 0:
                if j == 0:
                    fecha = valores.fecha[count]
                    concepto = valores.concepto[count]
                    detalle = valores.detalles[count]
                    importe = -1 * valores.importe[count]
                    suma += importe
                    importe = str(importe)
                    conceptoA = concepto + ": " + detalle + " - $" + importe
                    print(conceptoA) if debug else False
                elif j == 1:
                    concepto = valores.concepto[count]
                    detalle = valores.detalles[count]
                    importe = -1 * valores.importe[count]
                    suma += importe
                    importe = str(importe)
                    conceptoB = concepto + ": " + detalle + " - $" + importe
                    print(conceptoB) if debug else False
                elif j == 2:
                    concepto = valores.concepto[count]
                    detalle = valores.detalles[count]
                    importe = -1 * valores.importe[count]
                    suma += importe
                    importe = str(importe)
                    conceptoC = concepto + ": " + detalle + " - $" + importe
                    print(conceptoC) if debug else False

                # sumar los importes por concepto para generar el importe diario
                saldo_diario = suma
                print("saldo diario: {}".format(saldo_diario2)) if debug else False

            if index == 1:
                if j == 0:
                    fecha2 = valores.fecha[count]
                    concepto = valores.concepto[count]
                    detalle = valores.detalles[count]
                    importe = -1 * valores.importe[count]
                    suma += importe
                    importe = str(importe)
                    conceptoA2 = concepto + ": " + detalle + " - $" + importe
                    print(conceptoA2) if debug else False
                elif j == 1:
                    concepto = valores.concepto[count]
                    detalle = valores.detalles[count]
                    importe = -1 * valores.importe[count]
                    suma += importe
                    importe = str(importe)
                    conceptoB2 = concepto + ": " + detalle + " - $" + importe
                    print(conceptoB2) if debug else False
                elif j == 2:
                    concepto = valores.concepto[count]
                    detalle = valores.detalles[count]
                    importe = -1 * valores.importe[count]
                    suma += importe
                    importe = str(importe)
                    conceptoC2 = concepto + ": " + detalle + " - $" + importe
                    print(conceptoC2) if debug else False

                # sumar los importes por concepto para generar el importe diario
                saldo_diario2 = suma
                print("saldo diario: {}".format(saldo_diario2)) if debug else False

        # crear el list de datos
        datos_uno = (fecha, conceptoA, conceptoB, conceptoC, saldo_diario)
        datos_dos = (fecha2, conceptoA2, conceptoB2, conceptoC2, saldo_diario2)

    # enviar los archivos para el diccionario
    datos = (datos_uno, datos_dos)
    diccionario = botllenadordiccionarioDoble(datos, usuario)
    print(diccionario) if debug else False
    return diccionario


def botAgrupador_viejo(lista_vales, vales_dobles, vale_simple):
    # FUNCIONANDO OK
    debug = 0

    # PROBAR CREACION DE DICCIONARIO
    diccionario = {}

    print("iterar {} veces, sobrante: {}".format(vales_dobles, vale_simple)) if debug else 0

    # contador para el numero de vale en el if
    contador = 0
    for i in range(vales_dobles):
        # DESEMPAQUE DE LA LISTA, CONCETOS EN VALE
        vale_a, vale_b, *_ = lista_vales
        print("a: {}, b: {}".format(vale_a, vale_b)) if debug else 0
        vector_i = [vale_a, vale_b]

        # AGREGAR AL DICCIONARIO
        contador += 1
        llave_i = "vale" + str(i + 1)
        print("creando la key con nombre: {}".format(llave_i)) if debug else 0
        diccionario.update({llave_i: vector_i})
        print("diccionario actualizado: {}".format(diccionario)) if debug else 0

        # eliminar de la lista
        del lista_vales[:2]
        print("remanente de la sublista: {}".format(lista_vales)) if debug else 0

    # SOLO PUEDE HABER 1 VALE SIMPLE POR CADA ITERACION, SI EXISTE PROCEDER
    if vale_simple == 1:
        print("lista: {}".format(lista_vales)) if debug else 0
        vector_i = [lista_vales[0]]

        # AGREGAR AL DICCIONARIO
        llave_i = "vale" + str(contador + 1)
        print("creando la key con nombre: {}".format(llave_i)) if debug else 0
        diccionario.update({llave_i: vector_i})
        print("diccionario actualizado: {}".format(diccionario)) if debug else 0

        # eliminar ultimo valor de la lista
        del lista_vales[:1]
        print("remanente de la sublista: {}".format(lista_vales)) if debug else 0

    return diccionario


def botCreadorVales_viejo(lista_agrupada, valores, usuario):
    # FUNCIONANDO OK
    print(valores)
    # recordar el indice donde se quedó en cada iteración
    # INSTANCIAR VARIABLES
    index = 0
    debug = 0
    suma = 0

    # VARIABLES DEL SUBVALE 0
    fecha = ""
    # TODO PROBAR EL GENERADOR DE CADENAS
    # # A - Z
    # lista_letras = string.ascii_uppercase
    # nombre_base = "concepto"
    # for letra in range(26):
    #     tag = nombre_base + lista_letras[letra]
    #     print(tag)
    #     exec(tag + " = 'hello'")

    conceptoA = ""
    conceptoB = ""
    conceptoC = ""
    conceptoD = ""
    conceptoE = ""
    conceptoF = ""
    conceptoG = ""
    conceptoH = ""
    conceptoI = ""
    conceptoJ = ""
    conceptoK = ""
    conceptoL = ""
    conceptoM = ""
    conceptoN = ""
    conceptoO = ""
    saldo_diario = ""

    # VARIABLES DEL SUBVALE 1
    conceptoA2 = ""
    conceptoB2 = ""
    conceptoC2 = ""
    conceptoD2 = ""
    conceptoE2 = ""
    conceptoF2 = ""
    conceptoG2 = ""
    conceptoH2 = ""
    conceptoI2 = ""
    conceptoJ2 = ""
    conceptoK2 = ""
    conceptoL2 = ""
    conceptoM2 = ""
    conceptoN2 = ""
    conceptoO2 = ""
    saldo_diario2 = ""
    fecha2 = ""

    # VARIABLES DEL SUBVALE 3
    conceptoA3 = ""
    conceptoB3 = ""
    conceptoC3 = ""
    conceptoD3 = ""
    conceptoE3 = ""
    conceptoF3 = ""
    conceptoG3 = ""
    conceptoH3 = ""
    conceptoI3 = ""
    conceptoJ3 = ""
    conceptoK3 = ""
    conceptoL3 = ""
    conceptoM3 = ""
    conceptoN3 = ""
    conceptoO3 = ""
    saldo_diario3 = ""
    fecha3 = ""

    # SUBDICCIONARIOS
    datos_subvale0 = ()
    datos_subvale1 = ()
    datos_vale_doble = ()
    datos_vale_simple = ()

    # ITERAR POR CADA HOJA DE VALE PARA LLENAR EL DICCIONARIO NECESARIO PARA LLENAR LA PLANTILLA PDF
    for hoja, key in enumerate(lista_agrupada, 1):
        value = lista_agrupada[key]
        size = len(value)

        if size == 2:
            conceptosA, conceptosB = value
        elif size == 1:
            # extraer 1 elemento de la tupla usar ","
            conceptosA, = value
            conceptosB = 0

        nombre = "vale" + str(hoja)
        print("\nhoja: {}, value: {}, size: {}".format(hoja, value, size)) if debug else 0
        print("conceptosA: {}, conceptosB: {}".format(conceptosA, conceptosB)) if debug else 0

        """
        #  ----------  AQUI SE CREA EL VALE --------------- 
        """
        status = cpv(size, conceptosA, conceptosB, nombre)
        if status:
            print("VALE CREADO CORRECTAMENTE\n") if debug else 0

        # CREAR UN DICCIONARIO DOBLE, SIEMPRE EMPEZAR POR EL DOBLE, SI NO EXISTE PASAR AL SIMPLE
        if size == 2:
            # botCreadorValesDoble_Test()
            # intentar iterar por cada valor
            # sumar los conceptos que tiene
            conceptos_por_vale = sum(value)

            print("{} conceptos por vale doble".format(conceptos_por_vale)) if debug else 0
            # cada vale doble cuenta con 2 subvales individuales iterar por cada uno
            for subvale, conceptos_por_subvale in enumerate(value):
                suma = 0
                print("hoja:{} subvale: {}, conceptos por subvale: {}".format(hoja, subvale,
                                                                              conceptos_por_subvale)) if debug else 0
                # ahora iterar por cada concepto
                for concepto_index in range(1, conceptos_por_subvale + 1):
                    print("concepto: {}, index: {}".format(concepto_index, index)) if debug else 0

                    if subvale == 0:
                        concepto = valores.concepto[index]
                        detalle = valores.detalles[index]
                        importe = -1 * valores.importe[index]
                        suma += importe
                        importe = str(importe)
                        if concepto_index == 1:
                            fecha = valores.fecha[index]
                            fecha = fecha.center(MAXIMOS_RENGLON_FECHA)
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoA = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoA: {}".format(conceptoA)) if debug else 0
                        elif concepto_index == 2:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoB = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoB: {}".format(conceptoB)) if debug else 0
                        elif concepto_index == 3:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoC = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoC: {}".format(conceptoC)) if debug else 0
                        elif concepto_index == 4:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoD = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoD: {}".format(conceptoD)) if debug else 0
                        elif concepto_index == 5:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoE = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoE: {}".format(conceptoE)) if debug else 0
                        elif concepto_index == 6:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoF = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoF: {}".format(conceptoF)) if debug else 0
                        elif concepto_index == 7:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoG = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoG: {}".format(conceptoG)) if debug else 0
                        elif concepto_index == 8:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoH = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoH: {}".format(conceptoH)) if debug else 0
                        elif concepto_index == 9:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoI = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoI: {}".format(conceptoI)) if debug else 0
                        elif concepto_index == 10:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoJ = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoJ: {}".format(conceptoJ)) if debug else 0
                        elif concepto_index == 11:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoK = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoK: {}".format(conceptoK)) if debug else 0
                        elif concepto_index == 12:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoL = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoL: {}".format(conceptoL)) if debug else 0
                        elif concepto_index == 13:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoM = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoM: {}".format(conceptoM)) if debug else 0
                        elif concepto_index == 14:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoN = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoN: {}".format(conceptoN)) if debug else 0
                        elif concepto_index == 15:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoO = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoO: {}".format(conceptoO)) if debug else 0

                        # sumar los importes por concepto para generar el importe diario
                        saldo_diario = suma
                        print("saldo diario: {}".format(saldo_diario)) if debug else False
                    if subvale == 1:
                        concepto = valores.concepto[index]
                        detalle = valores.detalles[index]
                        importe = -1 * valores.importe[index]
                        suma = importe if concepto == 1 else suma + importe
                        importe = str(importe)
                        if concepto_index == 1:
                            fecha2 = valores.fecha[index]
                            fecha2 = fecha2.center(MAXIMOS_RENGLON_FECHA)
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoA2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoA: {}".format(conceptoA)) if debug else 0
                        elif concepto_index == 2:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoB2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoB: {}".format(conceptoB)) if debug else 0
                        elif concepto_index == 3:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoC2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoC: {}".format(conceptoC)) if debug else 0
                        elif concepto_index == 4:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoD2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoD: {}".format(conceptoD)) if debug else 0
                        elif concepto_index == 5:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoE2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoE: {}".format(conceptoE)) if debug else 0
                        elif concepto_index == 6:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoF2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoF: {}".format(conceptoF)) if debug else 0
                        elif concepto_index == 7:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoG2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoG: {}".format(conceptoG)) if debug else 0
                        elif concepto_index == 8:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoH2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoH: {}".format(conceptoH)) if debug else 0
                        elif concepto_index == 9:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoI2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoI: {}".format(conceptoI)) if debug else 0
                        elif concepto_index == 10:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoJ2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoJ: {}".format(conceptoJ)) if debug else 0
                        elif concepto_index == 11:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoK2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoK: {}".format(conceptoK)) if debug else 0
                        elif concepto_index == 12:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoL2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoL: {}".format(conceptoL)) if debug else 0
                        elif concepto_index == 13:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoM2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoM: {}".format(conceptoM)) if debug else 0
                        elif concepto_index == 14:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoN2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoN: {}".format(conceptoN)) if debug else 0
                        elif concepto_index == 15:
                            concepto = concepto + ": " + detalle + " - $" + importe
                            conceptoO2 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                            print("conceptoO: {}".format(conceptoO)) if debug else 0
                        # sumar los importes por concepto para generar el importe diario
                        saldo_diario2 = suma
                        print("saldo diario: {}".format(saldo_diario2)) if debug else False

                    # aumentar el index
                    index += 1
                    print("index: {}".format(index)) if debug else 0

            # LLENAR TUPLA CON LOS DATOS DE CADA SUBVALE
            datos_subvale0 = (fecha, conceptoA, conceptoB, conceptoC, conceptoD, conceptoE, conceptoF,
                              conceptoG, conceptoH, conceptoI, conceptoJ, conceptoK, conceptoL,
                              conceptoM, conceptoN, conceptoO, saldo_diario)
            print("datos val0: {}".format(datos_subvale0)) if debug else False
            datos_subvale1 = (fecha2, conceptoA2, conceptoB2, conceptoC2, conceptoD2, conceptoE2, conceptoF2,
                              conceptoG2, conceptoH2, conceptoI2, conceptoJ2, conceptoK2, conceptoL2,
                              conceptoM2, conceptoN2, conceptoO2, saldo_diario2)
            print("datos val1: {}".format(datos_subvale1)) if debug else False
            # LLENAR TUPLA PARA EL VALE
            datos_vale_doble = (datos_subvale0, datos_subvale1)
            diccionario_doble = botllenadordiccionarioDoble(datos_vale_doble, usuario)
            print("el diccionario doble queda: {}".format(diccionario_doble)) if debug else False
            # TODO LLENAR FORMULARIO DOBLE PDF
            status = botllenadorPlantillas(nombre, diccionario_doble)
            if status:
                print("VALE LLENADO CORRECTAMENTE") if debug else False

        # CREAR UN DICCIONARIO SIMPLE
        elif size == 1:
            # reiniciar la suma
            suma = 0
            conceptos_por_vale_simple = sum(value)

            print("conceptos a iterar: {}".format(conceptos_por_vale_simple)) if debug else 0
            print("{} conceptos por vale simple".format(conceptos_por_vale)) if debug else 0
            # cada vale simple cuenta con 1 subvale individual no es necesario iterar
            subvale = 0
            print("hoja: {} subvale{}, conceptos por subvale: {}".
                  format(hoja, subvale, conceptos_por_vale_simple)) if debug else 0

            for concepto_index in range(1, conceptos_por_vale_simple + 1):
                print("\nconcepto: {}, index: {}".format(concepto, index)) if debug else 0
                concepto = valores.concepto[index]
                detalle = valores.detalles[index]
                importe = -1 * valores.importe[index]
                suma += importe
                importe = str(importe)
                print(" VALE SENCILLO") if debug else 0
                print("VALORES: {} {} {} ".format(concepto, detalle, importe)) if debug else False
                if concepto_index == 1:
                    fecha3 = valores.fecha[index]
                    fecha3 = fecha3.center(MAXIMOS_RENGLON_FECHA)
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoA3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoA: {}".format(conceptoA)) if debug else 0
                elif concepto_index == 2:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoB3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoB: {}".format(conceptoB)) if debug else 0
                elif concepto_index == 3:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoC3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoC: {}".format(conceptoC)) if debug else 0
                elif concepto_index == 4:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoD3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoD: {}".format(conceptoD)) if debug else 0
                elif concepto_index == 5:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoE3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoE: {}".format(conceptoE)) if debug else 0
                elif concepto_index == 6:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoF3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoF: {}".format(conceptoF)) if debug else 0
                elif concepto_index == 7:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoG3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoG: {}".format(conceptoG)) if debug else 0
                elif concepto_index == 8:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoH3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoH: {}".format(conceptoH)) if debug else 0
                elif concepto_index == 9:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoI3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoI: {}".format(conceptoI)) if debug else 0
                elif concepto_index == 10:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoJ3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoJ: {}".format(conceptoJ)) if debug else 0
                elif concepto_index == 11:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoK3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoK: {}".format(conceptoK)) if debug else 0
                elif concepto_index == 12:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoL3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoL: {}".format(conceptoL)) if debug else 0
                elif concepto_index == 13:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoM3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoM: {}".format(conceptoM)) if debug else 0
                elif concepto_index == 14:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoN3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoN: {}".format(conceptoN)) if debug else 0
                elif concepto_index == 15:
                    concepto = concepto + ": " + detalle + " - $" + importe
                    conceptoO3 = concepto.center(MAXIMOS_RENGLON_ENTERO)
                    print("conceptoO: {}".format(conceptoO)) if debug else 0

                # sumar los importes por concepto para generar el importe diario
                saldo_diario3 = suma
                print("saldo diario: {}".format(saldo_diario3)) if debug else False
                # aumentar el index
                index += 1
                print("index: {}".format(index)) if debug else 0

            # LLENAR TUPLA CON LOS DATOS DE CADA SUBVALE
            datos_vale_simple = (fecha3, conceptoA3, conceptoB3, conceptoC3, conceptoD3, conceptoE3, conceptoF3,
                                 conceptoG3, conceptoH3, conceptoI3, conceptoJ3, conceptoK3, conceptoL3,
                                 conceptoM3, conceptoN3, conceptoO3, saldo_diario3)
            # LLENAR TUPLA PARA EL VALE
            diccionario_simple = botllenadordiccionarioSimple(datos_vale_simple, usuario)
            print("el diccionario simple queda: {}".format(diccionario_simple)) if debug else 0
            # TODO LLENAR FORMULARIO DOBLE PDF
            status = botllenadorPlantillas(nombre, diccionario_simple)
            if status:
                print("VALE LLENADO CORRECTAMENTE") if debug else 0
