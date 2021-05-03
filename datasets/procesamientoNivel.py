import os
from procesamientoArchivo import procesarArchivo


def procesarNivel(clases, nivel, campo):
    """
        A partir del dataset dividido genera los problemas binomiales de cada etiqueta
        @params:
            clases          - Required  : clases del nivel dividido (Lst)
            nivel           - Required  : nivel que se procesa (Int)
            campo           - Required  : nombre del campo cuyas clases dividen el problema (Str)
        """

    for c in clases:
        procesarArchivo(os.getcwd() + '\data\dataset_preprocesado_' + str(nivel) + '_' + str(c)
                        + '.json', nivel, c, 'voz_nivel_2')
