import csv
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


def dummy_tokenizer(doc):
    """
        Funcion para evitar que Countvectorizer tokenize si ya esta tokenizado
        @params:
            doc           - Required  : texto a tokenizar (Str)
        """
    return doc


def procesarModelos(carpeta, nivel, etiqueta):
    """
        Funcion para evitar que Countvectorizer tokenize si ya esta tokenizado
        @params:
            carpeta       - Required  : ruta a la carpeta del dataset (Str)
            nivel         - Required  : nivel del modelo (Int)
            etiqueta      - Required  : etiqueta de la division a clasificar (Int)
        """

    # Lectura de las clases de ese Nivel y Etiqueta
    with open(carpeta + '\\clases_' + str(nivel) + '_' + str(etiqueta) + '.csv', newline='') as f:
        reader = csv.reader(f)
        clases = list(reader)
    clases = clases[0]

    # Iterar las clases para vectorizar todos los datasets
    # Genera una lista de diccionarios ---> {'clase' : _clase_ 'atributos' : _atributos_vectorizados_}

    atributos = []
    etiquetas = []

    for c in clases:
        # Lectura de las etiquetas
        with open(carpeta + '\\etiquetas_' + str(nivel) + '_' + str(etiqueta) + '_' + str(c) + '.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        # Guardar las etiquetas de la clase
        etiquetas.append({'clase': c, 'etiquetas': data[0]})

        # Lectura de los atributos
        with open(carpeta + '\\atributos_' + str(nivel) + '_' + str(etiqueta) + '_' + str(c) + '.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        # Diccionario de tokens
        count_vect = CountVectorizer(analyzer='word', tokenizer=dummy_tokenizer, lowercase=False, token_pattern=None, decode_error="replace")

        # Matriz BoW
        X_train_counts = count_vect.fit_transform(data)

        # Persistir el diccionario de tokens para la clase
        with open('data\\vecVocabulario_' + str(nivel) + '_' + str(etiqueta) + '_' + str(c) + '.pkl', 'wb') as f:
            pickle.dump(count_vect.vocabulary_, f)

        # Tranformar los valores de la matriz BoW a valores TF-IDF normalizados
        transformador_tfidf = TfidfTransformer()
        atributos.append({'clase': c, 'atributos': transformador_tfidf.fit_transform(X_train_counts)})

        # Persistir el TF-IDF entrenado
        with open('data\\vecTFIDF_' + str(nivel) + '_' + str(etiqueta) + '_' + str(c) + '.pkl', 'wb') as fw:
            pickle.dump(transformador_tfidf, fw)

        # TODO: Poner Progress Bar
        print('Clase ', c, ' vectorizada...')

    # Iterar las clases para crear y entrenar los modelos
    resultados = []
    clases_con_modelo = 0
    clases_sin_modelo = 0

    for i in range(len(clases)):

        print('Predictor para la clase: ', clases[i])

        if len(etiquetas[i]['etiquetas']) > 5:
            # Particiónar del dataset para entrenamiento y testeo
            X_train, X_test, y_train, y_test = train_test_split(atributos[i]['atributos'],
                                                                etiquetas[i]['etiquetas'], test_size=0.3)

            # Definición del clasificador.
            clasificador_RL = LogisticRegression(verbose=0, solver='liblinear', random_state=0, penalty='l2',
                                                max_iter=1000)

            # Entrenamiento del modelo
            clasificador_RL.fit(X_train, y_train)

            # Predicciones del conjunto de testeo
            predicciones_RL = clasificador_RL.predict(X_test)

            # Calculo de accuracy sobre el conjunto de test.
            # print('Accuracy',np.mean(predicciones_RL == y_test)*100, '% sobre conjunto de Test.')
            print('Clase: ', clases[i], 'Muestras(Train): ', len(y_train), 'Accuracy(Test): ',
                np.mean(predicciones_RL == y_test) * 100)
            resultados.append([clases[i], len(y_train), np.mean(predicciones_RL == y_test) * 100])
            clases_con_modelo += 1

            # Guardado del modelo
            with open('data\\modeloRL_' + str(nivel) + '_' + str(etiqueta) + '_' + str(clases[i]) + '.sav', 'wb') as f:
                pickle.dump(clasificador_RL, f)

        else:
            print('No existen muestras suficientes para crear y entrenar un modelo.')
            clases_sin_modelo += 1

    # Guardado de los resultados
    with open('data\\resultados_' + str(nivel) + '_' + str(etiqueta) + '.csv', 'w',
              newline='') as f:
        write = csv.writer(f)
        write.writerows(resultados)

    print('Clases con modelo de predicción:', clases_con_modelo)
    print('Clases sin modelo de predicción:', clases_sin_modelo)
