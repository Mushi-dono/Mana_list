import pandas as pd

class Config:
    """Establece la configuración general"""
    def cargar_ruta_csv():
        """Carga la ruta almacenada en un archivo"""
        try:
            with open('ruta_csv.txt', 'r') as archivo:
                ruta = archivo.read().strip() # Leer la ruta del archivo
                return ruta
        except FileNotFoundError:
            return None
        
    def guardar_ruta_csv(ruta):
        """Guardar la ruta en un archivo para futuras ejecuciones"""
        with open('ruta_csv.txt', 'w') as archivo:
            archivo.write(ruta)

    def validar_csv(ruta):
        """Verificar si la ruta proporcionada es un archivo CSV válido"""
        try:
            pd.read_csv(ruta) # Intentar cargar el CSV para verificar si es válido
            return True
        except Exception:
            return False
        
    def cargar_o_pedir_ruta_csv():
        """Cargar la ruta del archivo CSV o pedirla si no está almacenada"""
        # 1. Cargar la ruta almacenada en 'ruta_csv.txt'
        ruta_csv = Config.cargar_ruta_csv()

        # 2. Si la ruta existe y el archivo CSV es válido se devuelve la ruta
        if ruta_csv and Config.validar_csv(ruta_csv):
            print(f"\nCargando colección desde {ruta_csv}")
            return ruta_csv
        else:
            # 3. Si no hay ruta guardada o el CSV no es válido se pide una nueva ruta
            while True:
                ruta_csv = input("Introduzca la ruta del archivo CSV de la colección: ")

                # 4. Validar la nueva ruta
                if Config.validar_csv(ruta_csv):
                    Config.guardar_ruta_csv(ruta_csv) # Guardar la ruta en 'ruta_csv.txt'
                    print(f"\nRuta del archivo CSV guardada: {ruta_csv}")
                    return ruta_csv
                else:
                    print("\n\t**El archivo no es válido inténtalo de nuevo.")