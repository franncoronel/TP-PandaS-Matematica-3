# -*- coding: utf-8 -*-
"""
GRUPO: TFG
Integrantes: Tomas Aragusuku
             Francisco Coronel   
             Gabriel Tarquini

analisisOscar2 genera un gráfico de barras que muestra el éxito (o fracaso) en los Oscars de una selección de directores.
El usuario debe ingresar qué director quiere analizar, y este ingreso está validado con una expresión regular.
Cada director pertenece a la clase Director, y también se utilizan expresiones regulares para extraer datos del dataset.
En base a una lista de películas, las compara con el dataset premiosOscar.csv para mostrar cuantos premios ganó y a cuantos fue nominada cada una de las películas.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

# DEFINIMOS LA CLASE DIRECTOR E INSTANCIAMOS LOS DIRECTORES DE LA LISTA CON SU NOMBRE Y SU LISTA DE PELICULAS

class Director:
    def __init__(self, nombreCompleto, peliculas):
        self.nombre = nombreCompleto
        self.peliculas = peliculas
        
    def nombre (self):
        return self.nombre
    
    def peliculas (self):
        return self.peliculas

martinScorsese = Director("MARTIN SCORSESE", ["Goodfellas", "The Departed", "Taxi Driver", "Raging Bull", "The Wolf of Wall Street"])
quentinTarantino = Director("QUENTIN TARANTINO", ["Pulp Fiction", "Kill Bill: Vol. 1", "Django Unchained", "Inglourious Basterds", "Reservoir Dogs"])
jamesCameron = Director("JAMES CAMERON", ["Avatar: The way of water", "Titanic", "Terminator 2: Judgment Day", "Aliens", "Avatar"])
christopherNolan = Director("CHRISTOPHER NOLAN", ["The Dark Knight", "Inception", "Interstellar", "Dunkirk", "Memento"])
timBurton = Director("TIM BURTON", ["Edward Scissorhands", "Batman", "The Nightmare Before Christmas", "Beetlejuice", "Alice in Wonderland"])
stanleyKubrick = Director("STANLEY KUBRICK", ["2001: A Space Odyssey", "Barry Lyndon", "A Clockwork Orange", "Full Metal Jacket", "A Clockwork Orange"])
peterJackson = Director("PETER JACKSON", ["The Lord of the Rings: The Return of the King", "The Lord of the Rings: The Fellowship of the Ring", "The Hobbit: An Unexpected Journey", "King Kong", "The Lovely Bones"])
stevenSpielberg = Director("STEVEN SPIELBERG", ["Jurassic Park", "E.T. the Extra-Terrestrial", "Schindler's List", "Saving Private Ryan", "Jaws"])

textoDirectores = "- MARTIN SCORSESE\n- QUENTIN TARANTINO\n- JAMES CAMERON\n- CHRISTOPHER NOLAN\n- TIM BURTON\n- STANLEY KUBRICK\n- PETER JACKSON\n- STEVEN SPIELBERG\n"
      

# INTERACCION CON EL USUARIO: SOLICITAMOS AL USUARIO EL NOMBRE COMPLETO DE UN DIRECTOR Y VALIDAMOS CON EXPRESIONES REGULARES

              
director = input(f"De la siguiente lista de directores:\n{textoDirectores}Ingrese el nombre completo "
                  "del director por el cual desea conocer las estadisticas de sus peliculas nominadas a los Oscar: ")
directores_regex = re.compile((r'^- ' + director + '\n'), re.MULTILINE | re.IGNORECASE)
hayCoincidencia = directores_regex.search(textoDirectores)

while hayCoincidencia is None:
    director = input("Nombre no encontrado. Por favor asegurese de que el director este en la lista y que su nombre este escrito correctamente: ")
    directores_regex = re.compile((r'^- ' + director + '\n'), re.MULTILINE | re.IGNORECASE)
    hayCoincidencia = directores_regex.search(textoDirectores)

directorElegido = director.upper()
print(f"\nHa seleccionado al director: {directorElegido}")


# COMPARAMOS LA ELECCION CON TODAS LAS OPCIONES PARA TRABAJAR UNICAMENTE CON LA VARIABLE "directorSeleccionado"
# Y TENER UN CODIGO GENERICO QUE SE PUEDA USAR PARA CUALQUIER DIRECTOR/OPCION QUE DECIDA EL USUARIO

if directorElegido == "MARTIN SCORSESE":
    directorSeleccionado = martinScorsese
elif directorElegido == "QUENTIN TARANTINO":
    directorSeleccionado = quentinTarantino
elif directorElegido == "JAMES CAMERON":
    directorSeleccionado = jamesCameron
elif directorElegido == "CHRISTOPHER NOLAN":
    directorSeleccionado = christopherNolan
elif directorElegido == "TIM BURTON":
    directorSeleccionado = timBurton
elif directorElegido == "STANLEY KUBRICK":
    directorSeleccionado = stanleyKubrick
elif directorElegido == "PETER JACKSON":
    directorSeleccionado = peterJackson
elif directorElegido == "STEVEN SPIELBERG":
    directorSeleccionado = stevenSpielberg
    
# INCIAMOS EL TRABAJO CON EL DATA SET

#Esta funcion recibe una dataframe y retorna la cantidad de veces que una pelicula fue nominada mediante expresiones regulares
def cuentaNominaciones(dataframe, pelicula):
    nominaciones = len(dataframe[dataframe['film'].str.contains((pelicula +'$'), case=False, na=False)])
    return nominaciones
    
df = pd.read_csv('premiosOscar.csv')
# Con esta línea se corrigen los nombres de las categorías para que comiencen con mayúscula en vez de estar MAYUSCULIZADOS
df["category"] = df["category"].str.capitalize()
# Esto equipara el nombre del premio para poder consultar por cualquier año

ganadores = df[df["winner"] == True]
perdedores = df[df["winner"] == False]

ganadores_lista = []
perdedores_lista = []

listaPeliculas = directorSeleccionado.peliculas

for i in range(len(listaPeliculas)):
    ganadores_lista.append(cuentaNominaciones(ganadores, listaPeliculas[i]))
    perdedores_lista.append(cuentaNominaciones(perdedores, listaPeliculas[i]))
   
# PREPARAMOS EL GRAFICO 
   
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False) # Borra linea superior del grafico para mejor visualizacion de los datos
ax.set_title("PELICULAS DIRIGIDAS POR " + directorSeleccionado.nombre + "\nNOMINADAS AL OSCAR\n")
ax.set_ylabel("Nominaciones")
ax.set_xlabel("Peliculas")

datos_ganadores = np.array(ganadores_lista)
datos_perdedores = np.array(perdedores_lista)
xvals = np.arange(len(listaPeliculas))
ancho = 0.3

for i,j in zip(xvals, datos_ganadores):
    plt.annotate(j, xy=(i - 0.2, j + 0.2)) # Valores de cada barra por encima de cada una
    
for i,j in zip(xvals, datos_perdedores):
    plt.annotate(j, xy=(i + 0.1, j + 0.2)) # Valores de cada barra por encima de cada una

plt.bar(xvals - ancho/2, datos_ganadores, width=ancho, color='green', label="Ganaron el premio")
plt.bar(xvals + ancho/2, datos_perdedores, width=ancho, color='red', label="Solo fueron nominadas")
plt.xticks(xvals, listaPeliculas, rotation=45)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1)) # Agregamos leyenda con las referencias del grafico
plt.show()





