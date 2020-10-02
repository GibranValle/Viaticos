import pandas as pd

"""
Permite acomodar los valores del dataframe en un nuevo dataframe de la siguiente forma
...............................................
RUTA
FECHA
CLASIFICACION | CONCEPTO O TRAYECTO | IMPORTE
CASETAS AUTORIZADAS | X | X
GASOLINA | X | X
HOSPEDAJE | X | X
AUTOBUS | X | X
PAQUETERIA | X | X
REFACCIONES O HERRAMIENTA | X | X
ESTACIONAMIENTO | X | X
OTROX | X | X

ALIMENTOS/TAXI | X | X
-------------------- TOTAL POR DIA:

LISTA DE CATEGORIAS
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

Gibran Valle
Inicio de implementación 15/09/2020
"""
import pandas as pd


def organizador(conceptos):
    size = len(conceptos)
    print("tamaño: {}".format(size))
    for index in range(size):
        dia = conceptos.dia[index]
        semana = conceptos.semana[index]

        ruta = conceptos.grupo[index]
        fecha = conceptos.fecha[index]
        clasificacion = conceptos.clasificacion[index]
        concepto = conceptos.concepto[index]
        importe = conceptos.importe[index]

        if index == 0:
            # print("INICIO DE ITERACION")
            fechaInicial = fecha
            semanaInicial = semana
            diaInicial = dia
            rutaInicial = ruta

            contadorDias = 1
            contadorSemanas = 1
            contadorRutas = 1

            saldoDiario = 0

            print("ULTIMO DIA")
            print("Ruta: {}".format(ruta))
            print("fecha: {}, semana: {}, dia: {}".format(fechaInicial, semanaInicial, diaInicial))
            print("{}: ${}".format(concepto, importe))

        else:
            # validar que sea la misma ruta, si es ruta diferente cambiar la semana
            if ruta != rutaInicial:
                rutaInicial = ruta
                if semana != semanaInicial:
                    semanaInicial = semana
                    print("\nNueva ruta y nueva Semana, {}".format(fecha))
                    print("Ruta: {}".format(ruta))
                    contadorSemanas += 1
                    contadorRutas += 1
                    saldoDiario = 0

                elif dia != diaInicial:
                    diaInicial = dia
                    print("\nNuevo dia, {}".format(fecha))
                    print("Ruta: {}".format(ruta))
                    contadorDias += 1
                    saldoDiario = 0
            else:
                if dia != diaInicial:
                    diaInicial = dia
                    print("\nNuevo dia, {}".format(fecha))
                    print("Ruta: {}".format(ruta))
                    contadorDias += 1
                    saldoDiario = 0

            # clasificar viatico conforme al reporte
            if clasificacion == "transporte":
                if (concepto.find("Caseta") != -1) or (concepto.find("caseta") != -1):
                    print("CASETA: ${}".format(importe))
                elif (concepto.find("Gasolina") != -1) or (concepto.find("gasolina") != -1):
                    print("GASOLINA: ${}".format(importe))
                elif (concepto.find("Autobus") != -1) or (concepto.find("autobus") != -1):
                    print("AUTOBUS: ${}".format(importe))
                elif (concepto.find("Autobús") != -1) or (concepto.find("autobús") != -1):
                    print("AUTOBUS: ${}".format(importe))
                elif (concepto.find("Estacionamiento") != -1) or (concepto.find("estacionamiento") != -1):
                    print("ESTACIONAMIENTO: ${}".format(importe))
                elif (concepto.find("Taxi") != -1) or (concepto.find("taxi") != -1):
                    print("TAXI: ${}".format(importe))
            elif clasificacion == "hospedaje":
                if (concepto.find("Hotel") != -1) or (concepto.find("hotel") != -1):
                    print("HOSPEDAJE: ${}".format(importe))
            elif clasificacion == "alimento":
                print("CONSUMO: ${}".format(importe))
            else:
                if (concepto.find("Paquete") != -1) or (concepto.find("paquete") != -1):
                    print("PAQUETERIA O ENVIO: ${}".format(importe))
                elif (concepto.find("Envio") != -1) or (concepto.find("envio") != -1):
                    print("PAQUETERIA O ENVIO: ${}".format(importe))
                elif (concepto.find("Envío") != -1) or (concepto.find("envío") != -1):
                    print("PAQUETERIA O ENVIO: ${}".format(importe))

                elif (concepto.find("Herramienta") != -1) or (concepto.find("herramienta") != -1):
                    print("HERRAMIENTA O REFACCION: ${}".format(importe))
                elif (concepto.find("Refac") != -1) or (concepto.find("refac") != -1):
                    print("HERRAMIENTA O REFACCION: ${}".format(importe))
                else:
                    print("OTRO: ${}".format(importe))

            saldoDiario += importe

            # llenar una tupla con todos los datos para crear un diccionario
            datosPorDia = ()

    print("SE ITERARON {} RUTAS, {} SEMANAS Y {} DIAS".format(contadorRutas, contadorSemanas, contadorDias))
