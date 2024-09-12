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

buscar_carta('clement, the worrywort')

mazo = leer_mazo('Grixis Affinity.txt')
print(mazo)