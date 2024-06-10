# -*- coding: utf-8 -*-
"""
GRUPO: TFG

Lider del proyecto: Francisco Coronel

Integrantes: Tomas Aragusuku          
             Gabriel Tarquini

Este archivo y analisisOscar1 generan gráficos que analizan los datos del dataset premiosOscar.csv
Ese dataset contiene todas las nominaciones y premiaciones de los Oscars desde su comienzo hasta la actualidad
Sin embargo, este programa toma los datos desde el año 1990 (y las 4 ceremonias anteriores) para acotar un poco la cantidad de posiblidades

analisisOscar1 requiere que el usuario ingrese un año y una opción (validadas con expresiones regulares) para diagramar en nodos
los nominados y ganadores de distintas categorías. El nodo ganador está coloreado de manera tal que resalte a la vista.
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import re

df = pd.read_csv('premiosOscar.csv')
# Con esta línea se corrigen los nombres de las categorías para que comiencen con mayúscula en vez de estar MAYUSCULIZADOS
df["category"] = df["category"].str.capitalize()
# Esto equipara el nombre del premio para poder consultar por cualquier año
df["category"].replace("Actor", "Actor in a leading role", inplace=True)
df["category"].replace("Writing (screenplay based on material previously produced or published)", "Writing (adapted screenplay)", inplace=True)
df["category"].replace("Writing (screenplay adapted from other material)", "Writing (adapted screenplay)", inplace=True)
df["category"].replace("Writing (screenplay written directly for the screen)", "Writing (original screenplay)", inplace=True)
df["category"].replace("Actress", "Actress in a leading role", inplace=True)  # Idem
df["name"] = df["name"].str.replace(" ", "\n")
df["film"] = df["film"].str.replace(" ", "\n")

#Funcion para que chequee que el año ingresado es correcto con uso de expresiones regulares

def buscar(anio):
    if re.search(r'\b(19[9]\d|20[012]{2}|200[0-9]|2023)\b', anio) is None:
        return True
    else:
        return False

    
anio = input("INGRESE EL AÑO QUE DESEA CONSULTAR (VISUALIZARÁ LAS ANTERIORES CUATRO EDICIONES)\n"
                 "DEBE SELECCIONAR UN AÑO ENTRE 1990 Y EL AÑO CORRIENTE:  \n")

while buscar(anio):
    anio = input("DEBE SELECCIONAR UN AÑO ENTRE 1990 Y EL AÑO CORRIENTE: \n")
    
def opcionesMenu ():
    print("\nEL SIGUIENTE PROGRAMA LE MOSTRARÁ LA CATEGORÍA DEL OSCAR QUE SELECCIONE\n"
          "EN LAS ULTIMAS 5 EDICIONES, CON SUS RESPECTIVOS NOMINADOS Y DESTACANDO QUIEN\n"
          "FUE EL GANADOR.\n"
          "Presione 1 para ver la categoría: Actor in a leading role\n"
          "Presione 2 para ver la categoría: Actress in a leading role\n"
          "Presione 3 para ver la categoría: Actress in a supporting role\n"
          "Presione 4 para ver la categoría: Actor in a supporting role\n"
          "Presione 5 para ver la categoría: Directing\n"
          "Presione 6 para ver la categoría: Best picture\n"
          "Presione 7 para ver la categoría: Writing (original screenplay)\n"
          "Presione 8 para ver la categoría: Visual effects\n"
          "Presione 9 para ver la categoría: Film editing\n"
          "Presione 10 para ver la categoría: Animated feature film\n"
          "Presione 0 para finalizar\n")

def menu():
    opcionesMenu()
    opcion = input("Por favor seleccione que categoría desea visualizar o ingrese 0 para finalizar el programa: ")
    while(not re.search(r'^(10|[0-9])$',opcion)):       #(opcion < 0) or (opcion > 10) 
        opcion = input("Por favor ingrese una opcion válida: ")
    opcion = int(opcion)
    if opcion == 1:
        grafos("Actor in a leading role", opcion)
    if opcion == 2:
        grafos("Actress in a leading role", opcion)
    if opcion == 3:
        grafos("Actress in a supporting role", opcion)
    if opcion == 4:
        grafos("Actor in a supporting role", opcion)
    if opcion == 5:
        grafos("Directing", opcion)
    if opcion == 6:
        grafos("Best picture", opcion)
    if opcion == 7:
        grafos("Writing (original screenplay)", opcion)
    if opcion == 8:
        grafos("Visual effects", opcion)
    if opcion == 9:
        grafos("Film editing", opcion)
    if opcion == 10:
        grafos("Animated feature film", opcion)
    if opcion == 0:
        return

def restaAnios(anio):
    """
    Parametros
    ----------
    anio : Es un string y se lo convierte a int para poder operar 
        
    Return
    -------
    anios_analizados : Es una lista de los años anteriores al ingresado por el usuario

    """
    anio=int(anio)
    anios_analizados = []
        
    for i in range(5):
            anios_analizados.append(anio-i)
    return anios_analizados

def removerCategorias(dataframe, aniosAnalizados):
    """
    Parametros
    ----------
    dataframe : DataFrame
        Puede ser cualquier DataFrame, aunque debería tener una columna "category".
    listaCategorias : Lista
        Es una lista de categorías a graficar, puede tener cualquier categoría mientras que coincida con las del DataFrame.

    Return
    -------
    DataFrame
        Ya que devuelve un DataFrame, se puede crear uno nuevo con este filtro o asignar al original para "limpiarlo".

    """
    return dataframe[dataframe["year_ceremony"].isin(aniosAnalizados)]

def tuplas_categoria(dataframe, anio, opcion):
    """
    Parametros
    ----------
    dataframe : DataFrame
        Puede ser cualquier DataFrame aunque siempre se trabaja con PG.
    categoria : String
        Es una de las categorías de la lista categorias_deseadas.
        Por el momento se ingresan manualmente aunque también se podría automatizar.
    opcion : Int
        Dependera el dato que tendran los nodos mas externos, ya que si se trata de una premios individuales
    devolverá el nombre del nominado/ganados. En cambio en premios colectivos, devolverá el nombre del film

    Return
    -------
    tuplas : Tupla
        Ya que las aristas se crean en base a tuplas,
        esta función extrae la categoría y el nombre del premiadx
        en base a la categoría ingresada al llamar a la función.
        Se transforma a lista para que la función add_edges_from cree todas las aristas.
    """
    if (opcion > 0) and (opcion < 6):
        tuplas = list(zip(dataframe[dataframe["year_ceremony"] == anio]["year_ceremony"], dataframe[dataframe["year_ceremony"] == anio]["name"]))
    else:
        tuplas = list(zip(dataframe[dataframe["year_ceremony"] == anio]["year_ceremony"], dataframe[dataframe["year_ceremony"] == anio]["film"]))

    return tuplas

def grafos(categoria, opcion):
    
    # Esta es la función llamada por el menú, y utiliza todas las funciones definidas previamente
    # para crear el grafo acorde a la opción ingresada
    
    PG = df[df["category"] == categoria]
    PG = PG.drop(columns=["year_film"])

    aniosAnalizados = restaAnios(anio)    


    #Se limpia el dataframe y también se crea una pequeña lista que contiene solamente a los ganadores
    #Esta lista es necesaria para colorear los nodos al momento de graficar
    PG = removerCategorias(PG, aniosAnalizados)

    if (opcion > 0) and (opcion < 6):
        ganadores = PG[PG["winner"] == True]["name"]
        ganadores = list(ganadores)
    else:
        ganadores = PG[PG["winner"] == True]["film"]
        ganadores = list(ganadores)

    # Crear una figura y ejes para el gráfico
    fig, ax = plt.subplots(figsize=(18, 18))
    plt.title(f"PREMIOS OSCAR - CATEGORIA: {categoria}")

    # Crear un grafo
    G = nx.Graph()
        
    # Agregar nodos
    G.add_node(categoria)
    G.add_nodes_from(restaAnios(anio))
    if (opcion > 0) and (opcion < 6):
        G.add_nodes_from(list(PG["name"]))
    else:
        G.add_nodes_from(list(PG["film"]))

    
    # Agregar bordes.
    #Podría ser una función.
    #Básicamente, recorre la lista de categorías y conecta cada una con el nodo central del año de la ceremonia
    for i in range(len(aniosAnalizados)):
        G.add_edge(aniosAnalizados[i], categoria)
        

    # Listas de bordes para diferentes categorias
    for i in range(len(aniosAnalizados)):
        i = tuplas_categoria(PG, aniosAnalizados[i], opcion)
        G.add_edges_from(i)

    # Lista de colores
    # Esta lista de colores hace que nx.draw() sea más legible, ya que si no todas estas condiciones estaban a la derecha de node_color=
    colores = ['#B0C4DE' if node == categoria else '#87CEFA' if node in aniosAnalizados else '#FFA500' if node in ganadores else '#FFD700' for node in G.nodes()]
    
    pos = nx.spring_layout(G, k=0.25, iterations=50)
    
    # Dibujar el grafo
    nx.draw(G, pos, node_color=colores, edge_color="grey", font_size=10,
            width=2, with_labels=True, node_size=2000, ax=ax)

    # Configurar los ejes para que no se muestren
    plt.axis('off')

    # Mostrar el gráfico
    plt.show()
    menu()

menu()