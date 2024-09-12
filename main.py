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

buscar_carta('clement, the worrywort')