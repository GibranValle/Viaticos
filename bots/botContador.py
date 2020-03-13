"""
Este bot se encarga de encontrar el saldo diario dentro del dataframe
Suma todos los gastos que tengan la misma semana y el mismo dia
Además, aquí está la función para convertir el importe numérico a importe con letra

Gibran Valle
Revisión final: 29/02/2020
"""


def saldoDiario(semanas, dias, importes):
    import pandas as pd
    # CALCULAR EL SALDO DIARIO
    # VARIABLES A RETORNAR

    n = 0
    m = 0
    suma = 0.0
    semana = 0
    dia = 0
    contador = 0
    saldo = []
    for i in semanas:
        # VALORES INICIALES
        if n == 0:
            semana = semanas[n]
            dia = dias[n]
        # SI ESTÁ DENTRO DE LA MISMA SEMANA
        if semana == semanas[n] and dia == dias[n]:
            contador += 1
            suma += importes[n]
            # print(" -  week: day: count:  sum: ".format(n, semana, dia, contador, suma))
        # ROMPE CORTA LA SUMA
        if semana != semanas[n] or dia != dias[n]:
            # forzar un ciclo for
            for i in range(m, n + 1):
                saldo.append(suma)
            # desplazamiento
            m = n
            contador = 0
            # empieza a sumar el entero nuevo
            suma = importes[n]
            if semana != semanas[n]:
                semana = semanas[n]
            if dia != dias[n]:
                dia = dias[n]
            # print(" -  week: day: count:  sum: ".format(n, semana, dia, contador, suma))
        n += 1

    saldo_diario = pd.Series(saldo)
    return saldo_diario


def numero_a_texto(entero):
    from math import floor
    miles = ("", "un mil ", "dos mil ", "tres mil ", "cuatro mil ", "cinco mil ", "seis mil ", "siete mil ",
             "ocho mil ", "nueve mil ")
    cientos = ("", "ciento ", "doscientos ", "trescientos ", "cuatrocientos ", "quinientos ", "seiscientos ",
               "setecientos ", "ochocientos ", "novecientos ")
    decimos = ("", "dieci", "veinti", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa")
    unidades = ("", "un", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve")
    especiales = ("diez", "once", "doce", "trece", "catorce", "quince")

    # (	un mil + quinientos + setenta + y 	+ cinco + pesos + (50  		 + /100)    M.N.
    # (	un mil + quinientos + veinti  +   	+ cinco + pesos + (100		 + /100)    M.N.
    # (	un mil + quinientos + dieci   +   	+ cinco + pesos	+ (0		 + /100)    M.N.
    # (	un mil + quinientos + dieci   +   	+ cinco + pesos + (15		 + /100)    M.N.
    str0 = '('
    str1 = ''
    str2 = ''
    str3 = ''
    str4 = ''
    str5 = ''
    str6 = ' pesos'
    str7 = ' '
    str8 = '/100 M.N.)'
    strtemp = ''

    mil = 0
    cien = 0
    diez = 0
    uno = 0
    res = 0
    cents = 0
    tempCents = 0
    temp = 0
    temp2 = 0

    # extraer centavos
    # 1500.15 * 100 = 150015 - (1500.15 / 1) * 100 = 15
    tempCents = entero * 100
    temp2 = floor(entero)
    temp2 = round(temp2)
    temp = temp2 * 100
    cents = tempCents - temp
    strtemp = str(int(cents))
    str7 += strtemp

    res = temp2
    entero = res

    # miles de pesos
    if entero > 999:
        mil = res / 1000  # 1572
        mil = floor(mil)  # millares = 1
        res = entero - (mil * 1000)  # 572
        cien = res / 100
        cien = floor(cien)  # centenas = 5
        res = res - (cien * 100)  # 72
        diez = res / 10
        diez = floor(diez)  # decenas = 7
        res = res - (diez * 10)  # 2
        uno = res  # unidades = 2

    elif res > 99:
        cien = res / 100
        cien = floor(cien)  # centenas = 5
        res = entero - (cien * 100)  # 72
        diez = res / 10
        diez = floor(diez)  # decenas = 7
        res = res - (diez * 10)  # 2
        uno = res  # unidades = 2

        if cien == 1 and uno == 0 and diez == 0:
            str2 = 'cien'

    elif res > 9:
        diez = res / 10
        diez = floor(diez)  # decenas = 7
        res = entero - (diez * 10)  # 2
        uno = res  # unidades = 2


    elif res > 0:
        uno = res  # unidades = 2
        if (uno == 1):
            str6 = ' peso'

    if uno == 0 and diez == 2:
        str4 = 'veinte'

    str1 = miles[mil]

    if str2 != 'cien':
        str2 = cientos[cien]

    if diez == 1 and (0 <= uno < 6):
        str5 = especiales[uno]

    elif str4 == 'veinte':
        str5 = 'veinte'

    else:
        str3 = decimos[diez]
        str5 = unidades[uno]

    if diez > 2 and uno != 0:
        str4 = ' y '

    string = str0
    string += str1
    string += str2
    string += str3
    string += str4
    string += str5
    string += str6
    string += str7
    string += str8

    return string
