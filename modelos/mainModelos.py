import sys
import csv
from procesamientoModelos import procesarModelos

"""
Main
"""

if (len(sys.argv) > 1):

    print("Secuencia de procesamiento de modelos...")

    # Procesar modelos para datasets desde la carpeta ARGV
    # Procesar modelos de Nivel 1
    print("Generando modelos de Nivel 1 de la carpeta: ", str(sys.argv[1]))
    procesarModelos(str(sys.argv[1]), 1, 1)
    print("Todos los modelos de Nivel 1 fueron generados.")

    #Procesar modelos de nivel 2

    #Lectura de clases de Nivel 1 Para identificar divisiones de Nivel 2
    with open(str(sys.argv[1]) + '\\clases_1_1.csv', newline='') as f:
        reader = csv.reader(f)
        clases = list(reader)
    clases_1 = clases[0]

    # Itero las divisiones de Nivel 1 para generar los modelos de cada división
    print("Generando modelos de Nivel 2 de la carpeta: ", str(sys.argv[1]))
    for c in clases_1:
        print("Generando modelos de Nivel 2 - división ", str(c))
        procesarModelos(str(sys.argv[1]), 2, c)

    print("Todos los modelos de Nivel 2 fueron generados.")

else:
    print("Falta el argumento Carpeta.")