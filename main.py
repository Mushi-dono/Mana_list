import pandas as pd
import os

from config import Config as cf

def buscar_carta(nombre_carta):
    """Busca una carta en la colección"""
    # Filtrar por el nombre de la carta
    carta = df[df['Name'].str.contains(nombre_carta, case=False)]

    if not carta.empty:
        # Mostrar los resultados
        for index, row in carta.iterrows():
            print(f"\n---Carta: {row['Name']}--- \n\tCantidad: {row['Quantity']} \n\tCarpeta: {row['Binder Name']}\n")
    else:
        print(f"\n\t---No se encontró la carta '{nombre_carta}' en la base de datos---")


def leer_mazo(ruta_archivo):
    """Revisa el mazo importado"""
    mazo=[]

    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            if linea.strip(): # Ignorar líneas vacías
                # Separar la cantidad del nobmre de la carta
                cantidad, nombre_carta = linea.strip().split(' ', 1)
                mazo.append((int(cantidad), nombre_carta))
    return mazo

def guardar_en_escritorio(nombre_archivo):
    """Devuelve la ruta completa para guardar el archivo en el escritorio"""
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop") # Obtiene la ruta del escritorio
    return os.path.join(escritorio, nombre_archivo) # Devuelve la ruta completa del archivo

def comparar_mazo_con_coleccion(ruta_archivo_mazo):
    """Compara el mazo importado con el CSV de la colección"""
    mazo = leer_mazo(ruta_archivo_mazo)
    
    # Listas vacías
    lista_suficientes = []
    lista_mediollena = []
    lista_faltantes = []

    for cantidad_mazo, nombre_carta_mazo in mazo:
        # Limpiar y estandarizar el nombre de la carta
        nombre_carta_mazo_limpio = nombre_carta_mazo.strip().lower()
        
        # Buscar todas las coincidencias en el DataFrame
        cartas_en_coleccion = df[df['Name'].str.strip().str.lower().str.contains(nombre_carta_mazo_limpio, na=False)]

        # Completar listas con mazo
        if not cartas_en_coleccion.empty:
            cantidad_total = cartas_en_coleccion['Quantity'].sum()
            if cantidad_total >= cantidad_mazo:
                lista_suficientes.append(f"{nombre_carta_mazo} [{cantidad_total}]")
            else:
                lista_mediollena.append(f"{nombre_carta_mazo}: \n\tDisponibles [{cantidad_total}] \n\tUnidades faltantes [{cantidad_mazo - cantidad_total}]")
        else:
            lista_faltantes.append(f"{nombre_carta_mazo} [4]")

    # Imprimir listas completas
    print("\t---Lista cartas disponibles---")
    for elemento in lista_suficientes:
        print(elemento)
    print("\n")
    print("\t---Lista cartas a medio completar---")
    for elemento in lista_mediollena:
        print(elemento)
    print("\n")
    print("\t---Lista cartas faltantes---")
    for elemento in lista_faltantes:
        print(elemento)
    print("\n")

    # Crear una buylist
    pregunta = input(f"\n\t¿Quieres crear una buylist? (y/n): ")
    if pregunta.lower() == 'y':
        nombre_archivo = input("¿Qué nombre quieres que tenga tu buylist?: ") + ".txt" # Añadida extensión del archivo
        ruta_salida = guardar_en_escritorio(nombre_archivo)

        with open(ruta_salida, 'w') as archivo_salida:
            # Añadir título para diferenciar
            lista_mediollena.insert(0, "\t---Lista cartas a medio completar---")
            lista_faltantes.insert(0, "\n\t---Lista cartas faltantes---")

            # Añadir lista de cartas
            for elemento in lista_mediollena:
                archivo_salida.write(elemento + '\n')
            for elemento in lista_faltantes:
                archivo_salida.write(elemento + '\n')
            
            print(f'Buylist: "{ruta_salida}" creada con éxito.')
    else:
        print("\n\t**Opción no disponible, inténtalo de nuevo**")


def menu():
    """Define el menú al iniciar el programa"""
    print("\n--Mana List--")
    print("1. Buscar una carta en la colección")
    print("2. Comparar una lista de un Deck con la colección")
    print("3. Salir\n")

def main():
    global df

    # Cargar la ruta del CSV o pedir una nueva si no existe
    ruta_csv = cf.cargar_o_pedir_ruta_csv()

    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv(ruta_csv)


    while True:
        menu()
        opcion = input("Seleciona una opción:")
        if opcion == '1':
            nombre_carta= input("Introduzca el nombre de la carta: ")
            buscar_carta(nombre_carta)
        elif opcion == '2':
            try:
                ruta_archivo_mazo = input("Introduzca la ruta del archivo del Deck: ")
                comparar_mazo_con_coleccion(ruta_archivo_mazo)
            except FileNotFoundError:
                print("\n\t**Archivo no encontrado, inténtalo de nuevo**")
            except Exception as e:
                print(f"\n\t**Error inesperado {e}**")
        elif opcion == '3':
            print("\n\t**Saliendo del programa**\n")
            break
        else:
            print("\n\t**Opción no disponible, inténtalo de nuevo**")

if __name__ == "__main__":
    main()