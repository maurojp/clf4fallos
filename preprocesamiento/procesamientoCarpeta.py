import sys
import os
import json

sys.path.append('..\\tools\\')

from miscTools import progressBar


def procesarCarpeta(carpeta):
    """
        Procesa los archivos de fallos de la carpeta
        @params:
            carpeta           - Required  : ruta a la carpeta que contiene los fallos (Str)
        """
    if os.path.isdir(carpeta):
        # Lista de archivos de fallos individuales
        listaArchivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
        # Hay que abrir el archivo JSON extraer el texto de sumario, las voces y guardar un ROW por cada voz, el sumario e id de voz.
        sumarios = []
        index_fallos = 0
        index_sumarios = 0
        for archivo in listaArchivos:
            with open(carpeta + '\\' + archivo, 'r', encoding='latin-1') as read_file:
                data = json.load(read_file)
            # Iteramos los sumarios
            for s in data['fallo']['sumarios']:
                # Iteramos las voces
                voces = []
                # Agrego prueba por existencia de sumarios vacios
                hay_voces = data['fallo']['sumarios'][s]['sumario'].get('voces')
                if hay_voces:
                    for v in data['fallo']['sumarios'][s]['sumario']['voces']:
                        voces.append([data['fallo']['sumarios'][s]['sumario']['voces'][v]['idNivel1'],
                                      data['fallo']['sumarios'][s]['sumario']['voces'][v]['idNivel2']])
                    # Eliminamos voces duplicadas es unhashable
                    voces = [list(x) for x in {(tuple(e)) for e in voces}]
                    # Guardamos la estructura [Sumario --> Voz]
                    for i in voces:
                        sumarios.append({'texto': data['fallo']['sumarios'][s]['sumario']['texto'], 'voz_nivel_1': i[0],
                                         'voz_nivel_2': i[1]})
                    index_sumarios += 1
            index_fallos += 1
            # Barra de progreso
            progressBar(index_fallos, len(listaArchivos),    prefix = 'Progreso:', suffix = 'Completado', length = 50)

        print("Cantidad de sumarios procesados: ", index_sumarios)
        print("Cantidad de fallos procesados: ", index_fallos)

        # Guardado del archivo de sumarios

        with open('data\dataset_1_2.json', 'w') as fp:
                json.dump(sumarios, fp)

    return sumarios
