import pandas as pd

# Cargar archivo CSV
df = pd.read_csv('ManaBox_Collection.csv')

def buscar_carta(nombre_carta):
    # Filtrar por el nombre de la carta
    carta = df[df['Name'].str.contains(nombre_carta, case=False)]

    if not carta.empty:
        # Mostrar los resultados
        for index, row in carta.iterrows():
            print(f"\n---Carta: {row['Name']}--- \n\tCantidad: {row['Quantity']} \n\tCarpeta: {row['Binder Name']}\n")
    else:
        print(f"\n\t---No se encontró la carta '{nombre_carta}' en la base de datos---")

def leer_mazo(ruta_archivo):
    mazo=[]

    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            if linea.strip(): # Ignorar líneas vacías
                # Separar la cantidad del nobmre de la carta
                cantidad, nombre_carta = linea.strip().split(' ', 1)
                mazo.append((int(cantidad), nombre_carta))
    return mazo

def comparar_mazo_con_coleccion(ruta_archivo_mazo):
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
        ruta_salida = input("¿Qué nombre quieres que tenga tu buylist?: ")
        with open(ruta_salida, 'w') as archivo_salida:
            lista_mediollena.insert(0, "\t---Lista cartas a medio completar---")
            lista_faltantes.insert(0, "\n\t---Lista cartas faltantes---")
            for elemento in lista_mediollena:
                archivo_salida.write(elemento + '\n')
            for elemento in lista_faltantes:
                archivo_salida.write(elemento + '\n')
            
            print(f'Buylist: "{ruta_salida}" creada con éxito.')
    else:
        print("\n\t**Opción no disponible, inténtalo de nuevo**")

def crear_buylist(ruta_archivo_mazo, ruta_archivo_salida):
    mazo = leer_mazo(ruta_archivo_mazo)

    cartas_faltantes = []

    for cantidad_mazo, nombre_carta_mazo in mazo:
            # Limpiar y estandarizar el nombre de la carta
            nombre_carta_mazo_limpio = nombre_carta_mazo.strip().lower()
            
            # Buscar todas las coincidencias en el DataFrame
            cartas_en_coleccion = df[df['Name'].str.strip().str.lower().str.contains(nombre_carta_mazo_limpio, na=False)]

            if not cartas_en_coleccion.empty:
                cantidad_total = cartas_en_coleccion['Quantity'].sum()
                if cantidad_total < cantidad_mazo:
                    faltante = cantidad_mazo - cantidad_total
                    cartas_faltantes.append(f"Faltan {faltante} unidades de '{nombre_carta_mazo}'")
            else:
                cartas_faltantes.append(f"La carta'{nombre_carta_mazo}' no está en la colección")

    # Escribir la lista de cartas en un archivo.txt
    with open(ruta_archivo_salida, 'w') as archivo_salida:
        for carta_faltante in cartas_faltantes:
            archivo_salida.write(carta_faltante + '\n')

def menu():
    print("\n--Mana List--")
    print("1. Buscar una carta en la colección")
    print("2. Comparar una lista de un Deck con la colección")
    print("3. Crear una buylist")
    print("4. Salir\n")

def main():
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
            except:
                print("\n\t**Opción no disponible, inténtalo de nuevo**")
        elif opcion == '3':
            ruta_archivo_mazo = input("Introduzca la ruta del archivo del Deck: ")
            ruta_archivo_salida = input("¿Qué nombre tendrá la buylist?: ")
            crear_buylist(ruta_archivo_mazo, ruta_archivo_salida)
        elif opcion == '4':
            print("\n\t**Saliendo del programa**\n")
            break
        else:
            print("\n\t**Opción no disponible, inténtalo de nuevo**")

if __name__ == "__main__":
    main()