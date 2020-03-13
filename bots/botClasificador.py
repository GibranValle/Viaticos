"""
Este bot se encarga de agregar una etiqueta en función del contenido del concepto del gasto.
Adicionalmente discrimina los gastos no deducibles y les agrega la etiqueta "vale"
en una columna que se llama comprobante.

Gibran Valle
Revisión final: 29/02/2020
"""


def etiquetador(tag, cadena, concepto):
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
    cadena = "Desayuno|Comida|Cena|Agua"
    alimentos = etiquetador(tag, cadena, concepto)

    # CATEGORIA NO.4 SERVICIO
    tag = "servicio"
    cadena = "Paq|Imp|Cop"
    servicios = etiquetador(tag, cadena, concepto)

    # CATEGORIA NO.6 INGRESO
    tag = "ingreso"
    cadena = "Dep|Reem"
    ingresos = etiquetador(tag, cadena, concepto)

    series = [transporte, hospedaje, alimentos, servicios, ingresos]
    categoria = pd.concat(series).sort_index()

    return categoria


def comprobante(concepto):
    import pandas as pd
    serie = pd.Series()
    tag = "vale"
    cadena = "Taxi|Vale"
    vales = etiquetador(tag, cadena, concepto)
    serie = vales
    return serie
