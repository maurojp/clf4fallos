import sys
import random
import json
import numpy as np
import csv

sys.path.append('..\\tools\\')

from miscTools import progressBar

# Conforma un dataset con los casos positivos de la clase y la misma cantidad de negativos aleatorios
def mul_to_bin(dataset, clase, campo):
    if clase:
        # Selecciona positivos y negativos de la clase
        positivos = [s for s in dataset if s[campo] == clase]
        negativos = [s for s in dataset if s[campo] != clase]
        if len(positivos) > len(negativos):
            muestra_negativos = negativos #Queda desbanlanceado pero no hay suficientes negativos
        else:
            muestra_negativos = random.sample(negativos, len(positivos))
        return positivos + muestra_negativos
    else:
        return False

# Procesa el archivo creando un archivo clases con los valores de campo.
# Por cada clase genera un dataset balanceado (si es posible).
# Cada dataset queda almacenado en dos archivos atributos_{nivel}_{clase} y etiquetas_{nivel}_{clase}.

def procesarArchivo(archivo, nivel, etiqueta, campo):
    """
        Genera a partir del archivo JSON un dataset Binomial por cada clase del nivel seleccionado
        @params:
            archivo         - Required  : ruta del archivo .JSON (Str)
            nivel           - Required  : nivel que se procesa (Int)
            etiqueta        - Required  : etiqueta del dataset, identifica la clase en un nivel dividido (Int)
            campo           - Required  : nombre del campo cuyas clases dividen el problema (Str)
        """
    with open(archivo, 'r', encoding='latin-1') as read_file:
        dataset_list = json.load(read_file)

    # Iterar para generar una lista "atributos" con diccionarios { clase: etiqueta, atributos: lista_preprocesada }
    # y una lista "etiquetas" { clase: etiqueta, etiquetas: lista de etiquetas } por cada clase encontrada en el nivel.

    # Extraigo etiquetas
    labels_column = np.array([s[campo] for s in dataset_list])

    # Lista de etiquetas
    labels = np.unique(labels_column)

    atributos = []
    etiquetas = []
    count = 0
    for clase in labels:
        # Genero un dataset binomial para la clase
        dataset_binario = mul_to_bin(dataset_list, clase, campo)
        # Guardo etiquetas con valor 1 para los positivos y 0 para los negativos # [s['voz'] for s in dataset_binario]
        etiquetas.append(
            {'clase': clase, 'etiquetas': [1 if s[campo] == clase else 0 for s in dataset_binario]})
        # Guardo los atributos
        atributos.append({'clase': clase, 'atributos': [s['texto'] for s in dataset_binario]})
        #print('Clase ', clase, ' procesada.')
        count += 1
        # Barra de progreso
        progressBar(count, len(labels), prefix='Progreso:', suffix='Completado', length=50)

    # Guardar las clases
    with open('data\\clases_' + str(nivel) + '_' + str(etiqueta) + '.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(labels)

    # Guardar los datasets
    for i in range(len(labels)):
        # Guardar archivo etiquetas_CLASE.csv
        with open('data\\etiquetas_' + str(nivel) + '_' + str(etiqueta) + '_' + str(etiquetas[i]['clase']) + '.csv', 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(etiquetas[i]['etiquetas'])
        # Guardar archivo atributos_CLASE.csv
        with open('data\\atributos_' + str(nivel) + '_' + str(etiqueta) + '_' + str(atributos[i]['clase']) + '.csv', 'w', newline='', encoding='latin-1') as f:
            write = csv.writer(f)
            write.writerows(atributos[i]['atributos'])

    return labels

def dividirDataset(archivo, clases_padre, campo_padre, campo_hijo, nivel):
    """
        Divide el Dataset de acuerdo a las clases_padre
        @params:
            archivo         - Required  : ruta del archivo .JSON (Str)
            clases_padre    - Required  : lista de clases padre (Lst)
            campo_padre     - Required  : nombre del campo padre en el JSON (Str)
            campo_hijo      - Required  : nombre del campo hijo en el JSON (Str)
            nivel           - Required  : nivel que se divide (hijo) (Int)
        """
    with open(archivo, 'r', encoding='latin-1') as read_file:
        dataset_list = json.load(read_file)

    # Separamos los sumarios de acuerdo a las clases de nivel padre
    dataset_dividido = []
    count = 0
    for v_1 in clases_padre:
        #print('Agrupando sumarios de Nivel 2 con padre ', v_1)
        # Agrego a la lista un diccionario { 'padre_1' = _id_nivel1_, 'sumarios_2' = _lista_de_hijos_ }
        dataset_dividido.append({'padre': v_1, 'sumarios': [s for s in dataset_list if
                                                               s[campo_padre] == v_1 and s[campo_hijo] != None]})
        count += 1
        # Barra de progreso
        progressBar(count, len(clases_padre), prefix='Progreso:', suffix='Completado', length=50)

    # Guardado de los datasets
    for i in range(len(clases_padre)):
        with open('data\\dataset_preprocesado_' + str(nivel) + '_' + str(dataset_dividido[i]['padre']) + '.json', 'w') as fp:
            json.dump(dataset_dividido[i]['sumarios'], fp)
