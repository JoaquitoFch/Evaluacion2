import requests
import random
import json


API_TOKEN = "cisco|aU3uepPB9g5RXiqn5Ms9uIaQKxQ6mLeOG4J5pu5lFt8" 
BASE_URL = "http://library.demo.local/api/v1/books"


headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_TOKEN
}




palabras_titulo = ["Manual", "Guía", "Secretos", "Fundamentos", "Arte", "Ciencia"]
temas = ["Redes", "Python", "Seguridad", "Servidores", "Nube", "Automatización"]
nombres_autor = ["Federico", "Juan", "Sergio", "Leona", "Eduart", "Fernando"]
apellidos_autor = ["Sanchez", "Peñaloza", "Norambuena", "Morales", "Gallegos", "Martinez"]

print("--- Agregando 50 libros aleatorios... ---")


for i in range(8, 58): 
    
    titulo_aleatorio = f"{random.choice(palabras_titulo)} de {random.choice(temas)} Vol. {random.randint(1, 5)}"
    autor_aleatorio = f"{random.choice(nombres_autor)} {random.choice(apellidos_autor)}"
    isbn_aleatorio = str(random.randint(1000000000000, 9999999999999)) 

    
    nuevo_libro = {
        "id": i,
        "title": titulo_aleatorio,
        "author": autor_aleatorio,
        "isbn": isbn_aleatorio
    }

    
    response = requests.post(BASE_URL, headers=headers, data=json.dumps(nuevo_libro))

    
    if response.status_code == 200:
        print(f"Libro con ID {i} creado exitosamente.")
    else:
        print(f"Error al crear libro con ID {i}. Código de estado: {response.status_code}")
        print(f"Respuesta: {response.text}")

print("\n--- Proceso de creación de 50 libros finalizado. ---")




print("\n--- Teniendo la lista completa de libros... ---")

try:
    
    get_response = requests.get(BASE_URL, headers=headers)

    if get_response.status_code == 200:
        todos_los_libros = get_response.json()
        print("--- Lista Total de Libros en la Biblioteca ---")
        
        print(json.dumps(todos_los_libros, indent=4))
        print(f"\nTotal de libros en la biblioteca: {len(todos_los_libros)}")
    else:
        print(f"Error al obtener la lista de libros. Código de estado: {get_response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Ocurrió un error de conexión: {e}")
