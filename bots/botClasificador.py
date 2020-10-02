"""
Este bot se encarga de agregar una etiqueta en función del contenido del concepto del gasto.
Adicionalmente discrimina los gastos no deducibles y les agrega la etiqueta "vale" o "factura"
en una columna que se llama comprobante.
Gibran Valle
Revisión final: 14/03/2020
"""
import pandas as pd


def etiquetador(tag, cadena, concepto):
    """
    Este bot regresa unicamente indices que cumplan con las condiciones
    :param tag:
    :param cadena:
    :param concepto:
    :return:
    """
    test = concepto.str.contains(pat=cadena)
    test = test.map({
        True: tag,
        False: "otro"
    })
    test = test[test == tag]
    return test


def clasificador(concepto):
    import pandas as pd
    categoria = pd.Series()
    """    Comentario multilinea:
    Clasifica los Movimientos diarios de mis viaticos segun el concepto
    Categorias a implementar
    1) Transporte
      a) uber
      b) autobus
      c) taxi
      d) avion
      e) gasolina
      f) caseta
      g) estacionamiento
      h) otro
    2) Hospedaje
      a) hotel
    3) Alimento
      a) desayuno
      b) comida
      c) cena
      d) otro
    4) Servicio
      a) refacciones
      b) paqueteria
      c) herramienta
      d) material
      e) consumibles
      f) impresiones y  copias
    5) Otro
    6) Ingreso
       a) Deposito viaticos
       b) Reembolso viaticos 
    """

    # CATEGORIA NO.1 TRANSPORTE
    tag = "transporte"
    cadena = "Auto|Uber|Taxi|Avi|Vuelo|Gas|Caseta|Estacionamiento"
    transporte = etiquetador(tag, cadena, concepto)

    # CATEGORIA NO.2 HOSPEDAJE
    tag = "hospedaje"
    cadena = "Hotel"
    hospedaje = etiquetador(tag, cadena, concepto)

    # CATEGORIA NO.3 ALIMENTOS
    tag = "alimento"
    cadena = "Desayuno|Comida|Cena|Agua|Consumo"
    alimentos = etiquetador(tag, cadena, concepto)

    # CATEGORIA NO.4 SERVICIO
    tag = "servicio"
    cadena = "Paq|Imp|Cop"
    servicios = etiquetador(tag, cadena, concepto)

    # CATEGORIA NO.4 SERVICIO
    tag = "material menor"
    cadena = "Material"
    servicios = etiquetador(tag, cadena, concepto)

    # CATEGORIA NO.6 INGRESO
    tag = "ingreso"
    cadena = "Dep|Reem"
    ingresos = etiquetador(tag, cadena, concepto)

    series = [transporte, hospedaje, alimentos, servicios, ingresos]
    categoria = pd.concat(series).sort_index()
    return categoria


def tipoComprobante(concepto, mapear):
    """
    Este bot encuentra los conceptos que consideramos como no deducibles,
    los cuales necesitan un vale, buscando el texto taxi
    Nota: los taxis con factura causan controversia
    Por lo que se agregó una verificación de que no exista la palabra
    factura en los conceptos
    :param concepto:
    :return: regresa un agrego mapeado de vales
    """
    tag = "vale"
    tag2 = "factura"
    cadena = "Taxi|Vale|vale|taxi"
    cadena2 = "Factura|factura"

    comprobante = concepto.str.contains(cadena) & ~concepto.str.contains(cadena2)
    # realizar el mapeo aquí ??
    if mapear:
        comprobante = comprobante.map({
            True: tag,
            False: tag2
        })

    return comprobante
