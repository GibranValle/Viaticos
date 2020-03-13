# Clasificador y comprobador de Viáticos
Actualmente en mi empresa trabajamos 20 empleados en el área de servicio técicnom, cada uno necesita comprobar los gastos que se realizan diariamente agrupados por semana, la carga de trabajo y los horarios extendidos fuera de casa y la oficina, dificultan la entrega de estos en tiempo y forma.

Algunos de los compañeros, los que llevan bastante tiempo en la empresa, están acostumbrados a realizar sus comprobaciones a mano, la base de datos la generan en una librera, y el reporte de gastos de igual forma se transcribe de su libreta a una hoja impresa, además, cuando existen gastos no deducibles, se debe elaborar un vale azul para compensar la ausencia de una factura. Esto supone un procedimiento muy tedioso, y además, corren el riesgo de perder su libreta y quedarse sin un respaldo de sus comprobaciones de viaticos entregada. 

Mediante una aplicación movil de uso general se puede adquirir la información de los gastos que se realizan diariamente, sin embargo, al no ser especializada a esta tarea, el formato no es el ideal para almancenarlo directamente en la base de datos.

Con ayuda del proyecto que se presenta, se pueden organizar los datos, para así poder almacenarlos en una base de datos de fácil acceso, y más importante lo que permitiría ahorrar bastante tiempo en la comprobación de estos gastos, es la automatización de la generación reporte  y de los vales que se deben presentar en el departamento de contabilidad. 

Al tener un error en la comprobación final (reporte) también se pierde bastante tiempo en la actualización de la base de datos y del mismo reporte. Entonces vincular el proceso de edición para poder actualizar simultáneamente la base de datos y el reporte. 

Adicionalmente se podría generar un reporte estadístico con fines de control también para el área de contabilidad. 

## Metodología 

Utilizando la metolodogía ALEVPA:

### Adquisición:
Los datos se adquieren sin formato de la app "Mi presupuesto" la cual es de uso general para finanzas personales, el archivo está en formato .xls (excel), esta parte facilita el registro de los gastos y los ingresos que tenemos durante el mes.
Los datos más importantes de adquirir son los siguientes:
* a) Fecha del movimiento.
* b) Concepto.
* c) Detalles.
* d) Importe.


### Limpieza:
El archivo extriado de la app, tiene algunas columnas que no son de interés, sin embargo, la aplicación no presenta la libertar para configurar y descartarlas desde antes de exportarlas. Pero afortunadamente los datos ya vienen limpios en cierta forma, la unica limpieza que se debe realizar es la siguiente:
* a) Si existen celdas vacias, donde se calcula el gasto mensual, se debe retirar
* b) El eje de fecha está en formato string, se debe convertir a formato datetime para poder utilizar los métodos que pandas provee
* c) El eje de importe está en formato string, se debe elimitar el símbolo $ y convertirlo a flotante

### Estructuración:
El dataset que se genera desde esta app, no cumple con todas los ejes de análisis que necesitamos, por lo tanto se debe eleborar:

* a) Organizar las series del dataframe en un orden predeterminado, para la facilitar la navegación en la base de datos que se va a generar. 
* b) Elegir la categoria a la cual corresponde el gasto, p.ej. (transporte, hospedaje, alimentos, etc.) 

### Procesamiento:
Para demostrar que los datos se estan organizando correctamente y no habra discrepancia entre los gastos hechos y los gatos comprobados se debe realizar lo siguiente: 

* a) Calcular el saldo diario, usualmente están al rededor de $1000 mensuales, si existe una diferencia muy grande serviría como alerta. 
* b) Generar un vale para cada gasto no deducible, o cuando la factura del gasto no se consiguió a tiempo.
* d) Elaborar un archivo excel con un formato agradable a la vista para poder consultarla, cuando se necesite realizar una aclaracion. 

### Visualización:
* a) Semanalmente se debe tener el reporte que cumpla con el formato que se maneja en la empresa.
* b) Los vales generados deben respetar tambien el formato de vale azul. Se necesita transformar el importe numerico a una representacion de texto p.ej. (CIEN PESOS...)
* c) Con la estructuración de los datos podemos generar estadisticas de los gastos por:
    - categoria
    - ciudad
    - semana
    - mes
    
### Instrucciones:
    1)  El usuario debe ingresar un archivo .xls en el directorio raiz
    2)  El programa genera un nuevo archivo .xlsx con mejor formato
    3)  El usuario debe copiar los valores de este nuevo archivo .xlsx y pegarlos en su base de datos manualmente
    4)  El programa separa los gastos no deducibles, genera una plantilla formulario .pdf
        que se puede editar posteriormente con cualquier programa de lectura de PDF

    Notas:
    1)  El proyecto funciona correctamente utilizando las plantillas de vale estándar
        TODO: IMPLEMENTAR LA GENERACIÓN Y LLENADO AUTOMÁTICO DE UN VALE PERSONALIZADO
    2)  El proyecto necesita más tiempo para pulir el algoritmo final, el cual
        generará la plantilla formulario de reporte semanal y lo llenará automáticamente
    3)  Cuando todos los algoritmos estén listos, se empaquetará el programa para
        que los empleados de la empresas puedan utilizarlo en las PC de la oficina.

    VISIÓN DEL PROYECTO:
    A)  Como mejoras pendientes que no podré implementar por falta de conocimiento de base de datos:
        TODO: EXPORTAR LOS VALORES A UNA BASE DE DATOS ACCESIBLE DESDE LA NUBE
    B)  Como proyecto paralelo se desea poder crear una app específica que logre implementar
        todos los algoritmos de este proyecto.
