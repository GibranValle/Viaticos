"""
Proyecto final del curso: "Python en el ámbito científico"
IPN CIC 2020

Gibran Valle
Revisión final: 13/03/2020

    Este proyecto tiene como finalidad agilizar la comprobación de viaticos
    que se erogan por los ingenieros de servicio en la empresa SEVIME.
    Está lleno de ideas ambiciosas y aunque la premisa no incluye algoritmos
    muy complejos, algunos bots ganaron cierto grado de dificultad.

Instrucciones:
    1)  El usuario debe ingresar un archivo .xls en el directorio raiz
    2)  El programa genera un nuevo archivo .xlsx con mejor formato
    3)  El usuario debe copiar los valores de este nuevo archivo .xlsx en la base de datos
    4)  El programa separa los gastos no deducibles, genera una plantilla formulario .pdf
        que se puede editar posteriormente con cualquier programa de lectura de PDF

    Notas:
    1)  El proyecto funciona correctamente utilizando las plantillas de vale estándar
        TODO: IMPLEMENTAR LA GENERACIÓN Y LLENADO AUTOMÁTICO DE UN VALE PERSONALIZADO
    2)  El proyecto necesita más tiempo para pulir el algoritmo final, el cual
        generará la plantilla formulario de reporte semanal y lo llenará automáticamente
    3)  Cuando todos los algoritmos estén listos, se empaquetará el programa para
        que los empleados de la empresas puedan utilizarlo en las PC de la oficina.

    VISIÓN DEL PROYECTO
    A)  Como mejoras pendientes que no podré implementar por falta de conocimiento de base de datos:
        TODO: EXPORTAR LOS VALORES A UNA BASE DE DATOS ACCESIBLE DESDE LA NUBE
    B)  Como proyecto paralelo se desea poder crear una app específica que logre implementar
        todos los algoritmos de este proyecto.
"""
import pandas as pd

from bots.botClasificador import clasificador as classify
from bots.botClasificador import tipoComprobante as tipo
from bots.botContador import saldoDiario as sd
from bots.botEstructurador import estructurarFecha as ef
from bots.botEstructurador import estructurarImporte as ei
from bots.botFormuladorVale import llenarVales as cv
pd.options.mode.chained_assignment = None  # default='warn'

# TAG PARA PDF
usuario = "Gibran Valle"

diccionario_vale = {
    'Importe': '100.00',
    'ImporteLetra': '(Cien pesos 00 M.N)',
    'Concepto A': '',
    'Concepto B': '',
    'Concepto C': '',
    "Fecha": "",
    "Recibido": usuario
}

# columnas extraidas de la app "Mi presupuesto"
columns_app = [
    "fecha",
    "concepto",
    "detalles",
    "metodo_pago",
    "categoria",
    "subcategoria",
    "proveedor",
    "grupo",
    "cuenta",
    "importe",
]
# columnas para borrar
drop_cols = ["metodo_pago", "subcategoria", "cuenta", "categoria"]
# columnas ordenadas segun el reporte usado
final_columns = [
    "fecha",
    "mes",
    "dia",
    "semana",
    "orden",
    "concepto",
    "detalles",
    "proveedor",
    "importe",
    "saldo diario",
    "comprobante",
    "clasificacion",
    "grupo"
]
ingreso_col = [
    "semana",
    "fecha",
    "importe",
]

# --------------- INICIO DEL PROGRAMA ------------------------------------
# cargar archivo xls en el directorio
excel = "viaticos.xls"

# dataframe completo, si no hay fecha no es una columna valida
data = pd.read_excel(excel, header=0, names=columns_app)
data = data.dropna(subset=["fecha"])
print("Archivo inicial:\n")
print(data.head())

# --------------- LIMPIEZA DEL DATAFRAME ---------------------------------
# drop columnas
data.drop(drop_cols, axis=1, inplace=True)

# convertir la columna fecha a objeto de fecha y extraer componentes para procesamiento
data["fecha"], data["mes"], data["semana"], data["dia"] = ef(data["fecha"])

# quitar simbolos para estadistico (-$)
data["importe"] = ei(data.importe)

# --------------- ESTRUCTURACION DEL DATAFRAME ---------------------------
# clasificar los conceptos
data["clasificacion"] = classify(data["concepto"])
data["clasificacion"].fillna(value="otro", inplace=True)

# Crea columna de comprobante de pago, mapeamos los datos para recibir vale o factura
data["comprobante"] = tipo(data["concepto"], mapear=True)
# tratamos los demas valores como facturas
data["comprobante"].fillna(value="factura", inplace=True)

# --------------- PROCESAMIENTO DEL DATAFRAME ---------------------------
# Crear un dataframe con los vales a elaborar
vales = data[data.comprobante == "vale"]
# limpiar valores nan
vales["detalles"].fillna(value="", inplace=True)
cv(vales, usuario)

# TODO BUSCAR UNA MANERA DE AUTOMATIZAR ESTA PARTE
# crear columna para ordenar manualmente
data["orden"] = ""

# crear serie de importes positivos
positivos = data[data.importe > 0]
ingresos = pd.DataFrame(positivos)
ingresos.reset_index(drop=True, inplace=True)  # drop para no agregar la columna de indices viejos
# elegir unicamente las columnas ingreso_col
ingresos = ingresos[ingreso_col]
ingresos["detalles"] = ""
# elegir la primer columna de la serie detalles
ingresos["detalles"][0] = "INICIO DE MES"
print("\ndataframe ingresos:\n", ingresos)
# guardar como otro archivo
ingresos.to_excel("outputs/ingresos2020.xlsx", index=False)

# actualizar dataframe sin ingresos
data = data[data.importe < 0]
data.reset_index(drop=True, inplace=True)  # drop para no agregar la columna de indices viejos
data["saldo diario"] = sd(data.semana, data.dia, data.importe)
# print("saldo: {}".format(data["saldo diario"]))

# organizar columnas conforme a la lista nueva
data = data[final_columns]

# TODO QUITAR: BORRAR MES0
data.drop(["mes"], axis=1, inplace=True)

# guardar nuevo archivo sin columna de index
data.to_excel("outputs/viaticos2020.xlsx", index=False)
print("\nDataframe final:")
print(data.head())

