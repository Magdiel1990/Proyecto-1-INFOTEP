#Importar el módulo mysql.connector
import mysql.connector

#Importar la libreía matplotlib
import matplotlib.pyplot as plt

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

#Función para obtener las categorías
def categories ():
    # Ejectuar una consulta de todas las categorías
    cursor.execute("SELECT distinct name FROM category")

    # Capturar los resultados
    rows = cursor.fetchall()

    categories = []

    for row in rows:
        categories.append(row[0])

    return categories

#Función para obtener las películas de una categoría
def movies_by_category(category):
    # Ejectuar una consulta
    cursor.execute(f"SELECT count(f.title) as cantidad FROM film as f join film_category as fc on f.film_id = fc.film_id join category as c on c.category_id = fc.category_id where c.name = '{category}'")

    # Capturar los resultados
    rows = cursor.fetchall()

    return rows[0][0]

#Función para obtener las categorías con la cantidad de películas
categorias = categories()

cantidad_peliculas = []

#Cantidad de películas por categoría
for categoria in categorias:
    cantidad_peliculas.append(movies_by_category(categoria))

#Gráfico de barras
plt.bar(categorias, cantidad_peliculas)
#Etiquetas del eje x
plt.xlabel('Categorías')
#Etiquetas del eje y
plt.ylabel('Cantidad de películas')
#Título del gráfico
plt.title('Cantidad de películas por categoría')
#Mostrar el gráfico
plt.show()

# Cerrar el cursor y la conexión
cursor.close()

connection.close()