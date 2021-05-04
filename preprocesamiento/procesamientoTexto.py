import sys
import re
import csv
import spacy
import json
import numpy as np
import es_core_news_md

sys.path.append('..\\tools\\')

from miscTools import progressBar


# Cargamos el modelo Spacy Español
nlp = spacy.load("es_core_news_md")
#nlp = es_core_news_md.load()


def lematizar(texto, nlp):
    """
        Preprocesa el texto
        @params:
            texto           - Required  : texto a preprocesar (Str)
            nlp             - Required  : modelo Spacy (Obj)
        """
    # Remuevo caracteres especiales y paso a minúsculas
    pre_texto = re.sub(r'[^A-Za-z0-9áéíóú ]+', '', texto.lower())

    # Crear doc de Spacy (Tokenizado)
    doc = nlp(pre_texto)

    # Guardar lemas removiendo stop-words y palabras menores a longitud tres
    lem_texto = [token.lemma_ for token in doc if not token.is_stop and len(token.text) > 2]

    return lem_texto


# Preprocesamiento del texto - Se hace ahora para no redundar luego. Reduce los tiempos mas de un 50%.
def procesarTexto(dataset, genera_archivo):
    """
            Preprocesa todos los textos del dataset
            @params:
                dataset                 - Required  : lista de textos (Lst)
                genera_archivo          - Required  : Indica si se persiste el dataset preprocesado (Bool)
            """
    count = 0
    for s in dataset:
        s['texto'] = lematizar(s['texto'], nlp)
        count += 1
        # Barra de progreso
        progressBar(count, len(dataset), prefix='Progreso:', suffix='Completado', length=50)
    print('Sumarios procesados:', count)

    #Guardado del dataset de sumarios preprocesado

    if genera_archivo:
        with open('data\dataset_preprocesado_1_2.json', 'w') as fp:
            json.dump(dataset, fp)

    return dataset
