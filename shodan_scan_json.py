import argparse
import shodan
import sys
import json
import pymongo

# Coloca aquí tu clave de API de Shodan
API_KEY = ''

def obtener_servicios_en_ip(ip):
    api = shodan.Shodan(API_KEY)

    try:
        # Buscar información sobre la dirección IP
        result = api.host(ip)

        # Imprimir información sobre los servicios o "none" si no hay información
        servicios = result['data'] if 'data' in result else [{'port': 'none', 'data': 'none'}]
        insertar_mongo_json(result['data'])
        for servicio in servicios:
            print(f"{ip} | {servicio['port']} ")

    except shodan.APIError as e:
        # Si hay un error de Shodan, mostrar "none" para el servicio
        print(f"{ip} | none | none (Error: {e})")
#colocar aqui tu cadena de conexion con mongodb
def insertar_mongo_json(json_data): 
    client = pymongo.MongoClient("mongodb://")

    # Seleccionar la base de datos en MongoDB
    db = client["ESCANEOS"]
    collection = db["IP"]
    try:
        for item in json_data:
            item.pop('_id', None)  # Elimina el campo Id si existe

        # Insertar los datos en la colección
        inserted_data = collection.insert_many(json_data)

        # Imprimir los IDs de los documentos insertados
        print("Documentos insertados con los siguientes IDs:")
        for id in inserted_data.inserted_ids:
            print(id)

    except Exception as e:
        print("Error en MongoDB:", e)

def procesar_archivo(archivo):
    try:
        with open(archivo, 'r') as file:
            # Leer cada línea del archivo
            for line in file:
                ip = line.strip()  # Eliminar espacios en blanco
                obtener_servicios_en_ip(ip)

    except FileNotFoundError:
        print(f"No se encontró el archivo: {archivo}")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

def main():
    parser = argparse.ArgumentParser(description="Script para obtener información de servicios en IPs utilizando Shodan y almacenar en MongoDB.")
    parser.add_argument("nombre_del_archivo", metavar="archivo", type=str, help="Nombre del archivo que contiene las direcciones IP.")

    args = parser.parse_args()

    # Obtener el nombre del archivo desde los argumentos de línea de comandos
    archivo_ips = args.nombre_del_archivo

    procesar_archivo(archivo_ips)

if __name__ == "__main__":
    main()
                              
