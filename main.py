import pandas as pd
import os

from collection_service import Config as cf
from file_service import Funciones as fn

def menu():
    """Define el menú al iniciar el programa"""
    print("\n--Mana List--")
    print("1. Buscar una carta en la colección")
    print("2. Comparar una lista de un Deck con la colección")
    print("3. Actualiza la DataBase de la colección")
    print("4. Salir\n")

def main():
    global df

    ruta_coleccion = cf.cargar_o_pedir_coleccion()
    df = ruta_coleccion


    while True:
        menu()
        opcion = input("Seleciona una opción:")
        if opcion == '1':
            nombre_carta= input("Introduzca el nombre de la carta: ")
            fn.buscar_carta(nombre_carta)
        elif opcion == '2':
            try:
                ruta_archivo_mazo = input("Introduzca la ruta del archivo del Deck: ")
                fn.comparar_mazo_con_coleccion(ruta_archivo_mazo)
            except FileNotFoundError:
                print("\n\t**Archivo no encontrado, inténtalo de nuevo**")
            except Exception as e:
                print(f"\n\t**Error inesperado {e}**")
        elif opcion == '3':
            cf.actualizar_coleccion()
            df = cf.cargar_coleccion() # Recargar el Dataframe después de actualizar
        elif opcion == '4':
            print("\n\t**Saliendo del programa**\n")
            break
        else:
            print("\n\t**Opción no disponible, inténtalo de nuevo**")

if __name__ == "__main__":
    main()