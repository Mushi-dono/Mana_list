import pandas as pd

# Cargar archivo CSV
df = pd.read_csv('ManaBox_Collection.csv')

def buscar_carta(nombre_carta):
    # Filtrar por el nombre de la carta
    carta = df[df['Name'].str.contains(nombre_carta, case=False)]

    if not carta.empty:
        # Mostrar los resultados
        for index, row in carta.iterrows():
            print(f"---Carta: {row['Name']}--- \n\tCantidad: {row['Quantity']} \n\tCarpeta: {row['Binder Name']}\n")
    else:
        print(f"No se encontró la carta '{nombre_carta}' en la base de datos.")

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
    
    for cantidad_mazo, nombre_carta_mazo in mazo:
        # Limpiar y estandarizar el nombre de la carta
        nombre_carta_mazo_limpio = nombre_carta_mazo.strip().lower()
        
        # Buscar todas las coincidencias en el DataFrame
        cartas_en_coleccion = df[df['Name'].str.strip().str.lower().str.contains(nombre_carta_mazo_limpio, na=False)]
        
        if not cartas_en_coleccion.empty:
            cantidad_total = cartas_en_coleccion['Quantity'].sum()
            if cantidad_total >= cantidad_mazo:
                print(f"La carta '{nombre_carta_mazo}' está en la colección con suficiente cantidad ({cantidad_total} unidades).")
            else:
                print(f"Faltan {cantidad_mazo - cantidad_total} unidades de '{nombre_carta_mazo}' en la colección. Solo hay {cantidad_total} unidades.")
        else:
            print(f"La carta '{nombre_carta_mazo}' no está en la colección.")

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
                


# Llamar a la función con las rutas de los archivos
crear_buylist('Grixis Affinity.txt', 'cartas_faltantes.txt')