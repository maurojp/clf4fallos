import sys
from procesamientoArchivo import procesarArchivo
from procesamientoArchivo import dividirDataset
from procesamientoNivel import procesarNivel

"""
Main
"""

if (len(sys.argv) > 1):

    print("Secuencia de procesamiento de datasets...")

    # Procesamiento del archivo de sumarios preprocesados
    print("Procesando muestras del archivo: ", str(sys.argv[1]))
    print("Procesando Nivel 1...")
    clases_1 = procesarArchivo(str(sys.argv[1]), 1, 1, 'voz_nivel_1')
    print("Dataset de Nivel 1 creado.")

    # División del dataset según clases de Nivel 1
    print("Procesando Nivel 2...")
    print("Dividiendo Dataset...")
    dividirDataset(str(sys.argv[1]), clases_1, 'voz_nivel_1', 'voz_nivel_2', 2)
    print("Dataset dividido a Nivel 2.")

    # Generación de los datasets finales en nivel 2 dividido
    print("Generando datasets de Nivel 2...")
    procesarNivel(clases_1, 2, 'voz_nivel_2')
    print("Datasets de Nivel 2 generados.")
else:
    print("Falta el argumento Archivo.")