#EN ESTE PROYECTO VAMOS A REALIZAR UNA EJEMPLO DE BUSQUEDA DE DATOS EN UNA BASE DE DATOS SQL
#UTILIZANDO EXPRESIONES REGULARES EN PYTHON PARA SELECCIONAR LOS DATOS QUE CUMPLAN CON UN PATRON ESPECIFICO

#Conexión a la base de datos sakila
#Importar el módulo mysql.connector
import mysql.connector

#importar el módulo re
import re

#Recibir las letras inicial y final del usuario
input1 = input("Inserte la primera letra de la película que desea: ")
input2 = input("Inserte la última letra de la película que desea: ")

#Validar que el usuario haya insertado alguna letra o una letra válida
if len(input1) == 0 or len(input2) == 0 or not input1.isalpha() or not input2.isalpha():
    print("Debe insertar una letra válida")
    exit()

#Función para conectar a la base de datos
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="sakila"
        )
        #Conexión exitosa
        if connection.is_connected():
            #print("Conexión exitosa a la base de datos")
            return connection
        #Conexión fallida
        else:
            print("Error al conectar a la base de datos")
    except Exception as e:
        print("Error al conectar a la base de datos", e)

#Conectar a la base de datos
connection = connect_to_database()

# Crear un cursor
cursor = connection.cursor()

# Ejectuar una consulta
cursor.execute("SELECT * FROM film")

# Capturar los resultados
rows = cursor.fetchall()

#Nombres de las columnas van en esta lista
movies_names = []

#Agregar los nombres de las películas a la lista
for film in rows:
    movies_names.append(film[1])

#Función para filtrar las películas 
def filter_movies(movies_names, input1, input2):     
    selected_movies = []
    #Reemplazar los espacios por guiones bajos
    for movie in movies_names:
        selected_movies.append(re.sub(' ', '_', movie))
        
    #Patrón para seleccionar las películas 
    patron = r'\b' + input1 + r'\w*' + input2 + r'\b'

    #Lista de películas seleccionadas que cumplen con el patrón
    selected_movies = [movie for movie in selected_movies if re.match(patron, movie)]
    
    #Retornar las películas seleccionadas
    return selected_movies

#Llamada a la función filter_movies
selected_movies = filter_movies(movies_names, input1, input2)

#Función para reemplazar los guiones bajos por espacios
def replace_space(selected_movies):
    final_selected_movies = []
    for(movie) in selected_movies:
        final_selected_movies.append(re.sub('_', ' ', movie))
    return final_selected_movies

#Llamada a la función replace_space
final_selected_movies = replace_space(selected_movies)

#Imprimir las películas seleccionadas
if(len(final_selected_movies) == 0):
    print("No hay películas que comiencen con la letra " + input1 + " y terminen con la letra " + input2)
else:
    print("Las películas disponibles son: ")
    index = 1
    for movie in final_selected_movies:        
        print(str(index) + ") " + movie)
        index += 1

# Cerrar el cursor y la conexión
cursor.close()

connection.close()