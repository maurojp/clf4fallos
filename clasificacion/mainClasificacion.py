import sys
import csv
import json
sys.path.append('..\\tools\\')
sys.path.append('..\\preprocesamiento\\')

from miscTools import progressBar
from procesamientoTexto import procesarTexto
from clasificador import clasificar

if (len(sys.argv) > 1):

    archivo = str(sys.argv[1])

    print("Secuencia de clasificación de sumarios...")

    #Lectura del archivo de sumarios a clasificar
    # TODO: Ver el tema del encoding
    with open(archivo, 'r', encoding='utf-8') as read_file:
        sumarios_list = json.load(read_file)

    # preprocesamos los sumarios
    sumarios_preprocesados = procesarTexto(sumarios_list, False)

    # Lectura de clases de Nivel 1 desde carpeta datasets
    with open('..\\datasets\\data\\clases_1_1.csv', newline='') as f:
        reader = csv.reader(f)
        clases = list(reader)
    clases_1 = clases[0]

    # Lectura del archivo de clases a ignorar
    with open('ignorar_clases.csv', newline='') as f:
        reader = csv.reader(f)
        clases = list(reader)
    ignorar_clases = clases[0]

    # Iteración de los sumarios a clasificar
    count_sumarios = 0
    for s in sumarios_preprocesados:

        print('Clasificación para el sumario ' + str(count_sumarios)+'\n')

        # Clasificación a Nivel 1

        resultados_1 = []
        for c in clases_1:
            if (c not in ignorar_clases):
                resultado = clasificar(1, 1, c, s['texto'])
                if resultado[0] == '1':
                    resultados_1.append(c)
        print('Clasificación para Nivel 1 para sumario: ', str(count_sumarios), 'Clases probables: ', *resultados_1)

        # Iteración de las etiquetas predichas en Novel 1
        for division_2 in resultados_1:
            # Lectura de clases de Nivel 2 y división predicha desde carpeta datasets
            with open('..\\datasets\\data\\clases_2_' + str(division_2) + '.csv', newline='') as f:
                reader = csv.reader(f)
                clases = list(reader)
            clases_2 = clases[0]

            # Clasificación a Nivel 2

            resultados_2 = []
            for c in clases_2:
                if (c not in ignorar_clases):
                    resultado = clasificar(2, division_2, c, s['texto'])
                    if resultado[0] == '1':
                        resultados_2.append(c)
            print('Clasificación para Nivel 2 y división ' + str(division_2) + ' para sumario: ', str(count_sumarios), 'Clases probables: ', *resultados_2)
    count_sumarios += 1
else:
    print("Falta el argumento Archivo.")
