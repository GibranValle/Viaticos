"""
Este bot se encarga de extrar la fecha de tipo string y convertirla a datetime, para poder
utilizar las funciones que esta clase tiene y poder encontrar el numero de mes, semana y día

Tambien convierte el importe de tipo string con simbolo "$" a flotante

Y puede quitar el simbolo "-" de un string, y convertirlo a flotante

Gibran Valle
Revisión final: 29/02/2020

    Nota:  Este es el bot más simple del proyecto
"""


def estructurarFecha(fecha_in):
    import pandas as pd
    # convertir la columna fecha a objeto de fecha
    # usar formato por defecto para semana y dia
    fecha = pd.to_datetime(fecha_in, dayfirst=True)

    # extraer fecha a numero de mes
    mes = fecha.dt.month

    # extraer fecha a numero de semana
    semana = fecha.dt.week

    # extrar el numero de dia
    # 0L - 6D
    dia = fecha.dt.dayofweek + 2

    # cambiar el formato despues de usar los metodos de semana y dia
    fecha = fecha.dt.strftime('%d/%m/%Y')

    return fecha, mes, semana, dia


def estructurarImporte(importe_in):
    importe = importe_in.replace('[\$,]', '', regex=True).astype(float)
    return importe


def estructurarImporteNegativo(importe_negativo):
    importe_negativo = str(importe_negativo)
    importe = importe_negativo.replace("-", "")
    return importe
