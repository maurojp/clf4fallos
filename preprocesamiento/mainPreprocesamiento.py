import sys
from procesamientoCarpeta import procesarCarpeta
from procesamientoTexto import procesarTexto

"""
Main
"""

if (len(sys.argv) > 1):

    print("Secuencia de preprocesamiento de archivos...")

    # Procesar archivos individuales de fallos
    print("Procesando archivos de la carpeta: ", str(sys.argv[1]))
    sumarios = procesarCarpeta(str(sys.argv[1]))
    print("Todos los fallos fueron procesados...")

    # Preprocesar texto de sumarios
    print("Preprocesando textos de sumarios...")
    sumarios_preprocesados = procesarTexto(sumarios, True)
    print("Todos los sumarios fueron preprocesados...")
    
else:
    print("Falta el argumento Carpeta.")