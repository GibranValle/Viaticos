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
    valores = vales[["fecha", "semana", "dia", "concepto", "detalles", "importe"]]

    # invertir indice del dataframe
    valores = valores.iloc[::-1]

    # reset al index para poder iterar
    valores.reset_index(drop=True, inplace=True)
    print("valores: ")
    print(valores.head())
    # SEPARAR EN VALES DIARIOS, MAXIMO 3 CONCEPTOS POR DIA Y AGRUPAR POR SEMANA
    conceptos_totales = len(valores.fecha)
    lista_vales = botSeparador(valores, conceptos_totales)
    prints = lista_vales
    print(
        "\n\n{} conceptos no deducibles\nlista de vales separador por dia: {}\n".format(conceptos_totales, prints)) \
        if debug else 0

    # AGRUPA LOS VALES, MAXIMO 2 VALES POR HOJA
    # LISTA DE INDICES PARA ITERAR
    num_vales = len(lista_vales)
    vales_dobles = int(num_vales / 2)
    vale_simple = num_vales % 2
    lista_agrupada = botAgrupador(lista_vales, vales_dobles, vale_simple)
    print_list = lista_agrupada
    conceptos_por_vale = []
    print("se llenarán {} vales dobles + {} vale simple\n".format(vales_dobles, vale_simple)) if debug else 0
    print("Hojas de vales: {}\n\nDataframe vales:".format(lista_agrupada)) if debug else 0

    # LLENAR LAS LISTAS DE DATOS, CREAR DICCIONARIOS Y LLENAR FORMULARIO PDF
    botCreadorVales(lista_agrupada, valores, usuario)


# ---------------------- BOTS QUE YA FUNCIONAN Y ESTAN PROBADOS ------------------------------------
def botCreadorVales(lista_agrupada, valores, usuario):
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
                print("hoja:{} subvale: {}, conceptos por subvale: {}".format(hoja, subvale,
                                                                              conceptos_por_subvale)) if debug else 0
                # ahora iterar por cada concepto
                for concepto_index in range(1, conceptos_por_subvale + 1):
                    print("\n")
                    print("concepto: {}, index: {}".format(concepto_index, index)) if debug else 0

                    if subvale == 0:
                        concepto = valores.concepto[index]
                        detalle = valores.detalles[index]
                        importe = -1 * valores.importe[index]
                        suma += importe
                        importe = str(importe)
                        if concepto_index == 1:
                            fecha = valores.fecha[index]
                            print("fecha: {}".format(fecha))
                            conceptoA = concepto + ": " + detalle + "-" + "$" + importe
                            print("conceptoA: {}".format(conceptoA)) if debug else 0
                        elif concepto_index == 2:
                            conceptoB = concepto + ":" + detalle + " - $" + importe
                            print("conceptoB: {}".format(conceptoB)) if debug else 0
                        elif concepto_index == 3:
                            conceptoC = concepto + ":" + detalle + " - $" + importe
                            print("conceptoC: {}".format(conceptoC)) if debug else 0
                        elif concepto_index == 4:
                            conceptoD = concepto + ":" + detalle + " - $" + importe
                            print("conceptoD: {}".format(conceptoD)) if debug else 0
                        elif concepto_index == 5:
                            conceptoE = concepto + ":" + detalle + " - $" + importe
                            print("conceptoE: {}".format(conceptoE)) if debug else 0
                        elif concepto_index == 6:
                            conceptoF = concepto + ":" + detalle + " - $" + importe
                            print("conceptoF: {}".format(conceptoF)) if debug else 0
                        elif concepto_index == 7:
                            conceptoG = concepto + ":" + detalle + " - $" + importe
                            print("conceptoG: {}".format(conceptoG)) if debug else 0
                        elif concepto_index == 8:
                            conceptoH = concepto + ":" + detalle + " - $" + importe
                            print("conceptoH: {}".format(conceptoH)) if debug else 0
                        elif concepto_index == 9:
                            conceptoI = concepto + ":" + detalle + " - $" + importe
                            print("conceptoI: {}".format(conceptoI)) if debug else 0
                        elif concepto_index == 10:
                            conceptoJ = concepto + ":" + detalle + " - $" + importe
                            print("conceptoJ: {}".format(conceptoJ)) if debug else 0
                        elif concepto_index == 11:
                            conceptoK = concepto + ":" + detalle + " - $" + importe
                            print("conceptoK: {}".format(conceptoK)) if debug else 0
                        elif concepto_index == 12:
                            conceptoL = concepto + ":" + detalle + " - $" + importe
                            print("conceptoL: {}".format(conceptoL)) if debug else 0
                        elif concepto_index == 13:
                            conceptoM = concepto + ":" + detalle + " - $" + importe
                            print("conceptoM: {}".format(conceptoM)) if debug else 0
                        elif concepto_index == 14:
                            conceptoN = concepto + ":" + detalle + " - $" + importe
                            print("conceptoN: {}".format(conceptoN)) if debug else 0
                        elif concepto_index == 15:
                            conceptoO = concepto + ":" + detalle + " - $" + importe
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
                            # REINICIAR SUMA
                            suma = 0
                            fecha2 = valores.fecha[index]
                            print("fecha: {}".format(fecha2))
                            conceptoA2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoA2: {}".format(conceptoA2)) if debug else 0
                        elif concepto_index == 2:
                            conceptoB2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoB2: {}".format(conceptoB2)) if debug else 0
                        elif concepto_index == 3:
                            conceptoC2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoC2: {}".format(conceptoC2)) if debug else 0
                        elif concepto_index == 4:
                            conceptoD2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoD2: {}".format(conceptoD2)) if debug else 0
                        elif concepto_index == 5:
                            conceptoE2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoE2: {}".format(conceptoE2)) if debug else 0
                        elif concepto_index == 6:
                            conceptoF2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoF2: {}".format(conceptoF2)) if debug else 0
                        elif concepto_index == 7:
                            conceptoG2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoG2: {}".format(conceptoG2)) if debug else 0
                        elif concepto_index == 8:
                            conceptoH2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoH2: {}".format(conceptoH2)) if debug else 0
                        elif concepto_index == 9:
                            conceptoI2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoI2: {}".format(conceptoI2)) if debug else 0
                        elif concepto_index == 10:
                            conceptoJ2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoJ2: {}".format(conceptoJ2)) if debug else 0
                        elif concepto_index == 11:
                            conceptoK2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoK2: {}".format(conceptoK2)) if debug else 0
                        elif concepto_index == 12:
                            conceptoL2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoL2: {}".format(conceptoL2)) if debug else 0
                        elif concepto_index == 13:
                            conceptoM2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoM2: {}".format(conceptoM2)) if debug else 0
                        elif concepto_index == 14:
                            conceptoN2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoN2: {}".format(conceptoN2)) if debug else 0
                        elif concepto_index == 15:
                            conceptoO2 = concepto + ":" + detalle + " - $" + importe
                            print("conceptoO2: {}".format(conceptoO2)) if debug else 0

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
            # print("el diccionario doble queda: {}".format(diccionario_doble)) if debug else False
            print("el diccionario doble queda: {}".format(diccionario_doble))  # temporal
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
                print("\n\nconcepto: {}, index: {}".format(concepto, index)) if debug else 0
                concepto = valores.concepto[index]
                detalle = valores.detalles[index]
                importe = -1 * valores.importe[index]
                suma += importe
                importe = str(importe)
                print(" VALE SENCILLOOOOOOOOOOOOOOO")
                print("VALORES: {} {} {} ".format(concepto, detalle, importe)) if debug else False
                if concepto_index == 1:
                    fecha3 = valores.fecha[index]
                    print("fecha3: {}".format(fecha3))
                    conceptoA3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoA3) if debug else False
                elif concepto_index == 2:
                    conceptoB3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoB3) if debug else False
                elif concepto_index == 3:
                    conceptoC3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoC3) if debug else False
                elif concepto_index == 4:
                    conceptoD3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoD3) if debug else False
                elif concepto_index == 5:
                    conceptoE3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoE3) if debug else False
                elif concepto_index == 6:
                    conceptoF3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoF3) if debug else False
                elif concepto_index == 7:
                    conceptoG3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoG3) if debug else False
                elif concepto_index == 8:
                    conceptoH3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoH3) if debug else False
                elif concepto_index == 9:
                    conceptoI3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoI3) if debug else False
                elif concepto_index == 10:
                    conceptoJ3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoJ3) if debug else False
                elif concepto_index == 11:
                    conceptoK3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoK3) if debug else False
                elif concepto_index == 12:
                    conceptoL3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoL3) if debug else False
                elif concepto_index == 13:
                    conceptoM3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoM3) if debug else False
                elif concepto_index == 14:
                    conceptoN3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoN3) if debug else False
                elif concepto_index == 15:
                    conceptoO3 = concepto + ":" + detalle + " - $" + importe
                    print(conceptoO3) if debug else False

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
            print("fecha otra vez: {}".format(fecha))
            # LLENAR TUPLA PARA EL VALE
            diccionario_simple = botllenadordiccionarioSimple(datos_vale_simple, usuario)
            print("el diccionario simple queda: {}".format(diccionario_simple))  # temporal
            print("el diccionario simple queda: {}".format(diccionario_simple)) if debug else 0
            # TODO LLENAR FORMULARIO DOBLE PDF
            status = botllenadorPlantillas(nombre, diccionario_simple)
            if status:
                print("VALE LLENADO CORRECTAMENTE") if debug else 0


def botAgrupador(lista_vales, vales_dobles, vale_simple):
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


def botSeparador(valores, conceptos_totales):
    # FUNCIONANDO OK
    # sepana N CONCEPTOS EN N < 4 CONCEPTOS POR HOJA
    index = 0
    sa = 0  # semana previa
    da = 0  # dia previa
    cc = 0  # contador de conceptos
    lista = []
    debug = 0

    for i in range(conceptos_totales):
        s = valores.semana[i]
        d = valores.dia[i]

        if i == 0:  # inicio de iteracion
            cc = 1
            index = 0
            sa = s
            da = d
            if debug:
                print("inicio")
                print("semana: {}, dia: {}, index: {}, concepto: {}".format(s, d, i, cc))
                print("")

        elif s == sa and d == da:
            cc += 1
            if i == conceptos_totales - 1:
                print("fin de lista") if debug else 0
                lista.append(cc)
            if debug:
                print("misma semana y mismo dia")
                print("semana: {}, dia: {}, index: {}, concepto: {}".format(s, d, i, cc))
                print("")

        elif s != sa or d != da or cc > 3:
            lista.append(cc)
            index += 1
            cc = 1
            sa = s
            da = d
            if i == conceptos_totales - 1:
                print("fin de lista") if debug else 0
                lista.append(cc)
            if debug:
                print("cambio de semana o dia")
                print("semana: {}, dia: {}, index: {}, concepto: {}".format(s, d, i, cc))
                print("")

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
    fecha = diccionario["Fecha"]
    fecha = fecha.replace("/", "-")
    print("fecha: {}".format(fecha))
    nombre_entrada = "plantillas/" + nombre_plantilla + ".pdf"
    nombre_salida = "outputs/vale-" + fecha + ".pdf"
    botllenadorForma(nombre_entrada, nombre_salida, diccionario)
    return 1


def botllenadordiccionarioSimple(datos_simples, usuario):
    # FUNCIONANDO OK
    print("datos simples:")
    print(datos_simples)
    fecha, conceptoA, conceptoB, conceptoC, conceptoD, conceptoE, conceptoF, \
    conceptoG, conceptoH, conceptoI, conceptoJ, conceptoK, conceptoL, \
    conceptoM, conceptoN, conceptoO, importe = datos_simples
    importe_letra = num2wrd(float(importe))

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

    print("\n")
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
