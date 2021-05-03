from os import path
import pickle
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

def clasificar(nivel, division, clase, texto):
    """
        Clasifica el texto con el modelo de ese nivel, division y clase
        @params:
            nivel           - Required  : nivel al que se quiere clasificar (Int)
            division        - Required  : division del nivel que se quiere clasificar (Int)
            clase           - Required  : clase que se quiere clasificar (Int)
            texto           - Required  : Texto preprocesado que se quiere clasificar (Lst)
        """

    # Lectura del vocabulario - carga del vectorizador y transformada TFIDF
    loaded_vec = CountVectorizer(analyzer='word', tokenizer=dummy_tokenizer, lowercase=False, token_pattern=None,
                                 decode_error="replace", vocabulary=pickle.load(open('..\\modelos\\data\\vecVocabulario_' + str(nivel)
                                                               + '_' + str(division) + '_' + str(clase)
                                                               + '.pkl', "rb")))

    transformador_tfidf = pickle.load(open('..\\modelos\\data\\vecTFIDF_'
                                                               + str(nivel) + '_' + str(division) + '_'
                                                               + str(clase) + '.pkl', "rb"))

    # Vectorizado y transformado del texto
    texto_vectorizado = transformador_tfidf.transform(loaded_vec.transform([texto]))

    # Lectura del modelo si existe (Pudo no hacerse por falta de muestras)
    if path.exists('..\\modelos\\data\\modeloRL_'+ str(nivel) + '_' + str(division)
                  + '_'+ str(clase) + '.sav'):

        modelo_leido = pickle.load(open('..\\modelos\\data\\modeloRL_'
                                                                   + str(nivel) + '_' + str(division) + '_'
                                                                   + str(clase) + '.sav', 'rb'))
        # clasificación
        result = modelo_leido.predict(texto_vectorizado)

    else:

        print('Falta un modelo para nivel '+ str(nivel) + '_' + str(division) + '_'+ str(clase))
        result = '-1'

    return result
