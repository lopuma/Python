"""
  ____          _____               _ _           _       
 |  _ \        |  __ \             (_) |         | |      
 | |_) |_   _  | |__) |_ _ _ __ _____| |__  _   _| |_ ___ 
 |  _ <| | | | |  ___/ _` | '__|_  / | '_ \| | | | __/ _ \
 | |_) | |_| | | |  | (_| | |   / /| | |_) | |_| | ||  __/
 |____/ \__, | |_|   \__,_|_|  /___|_|_.__/ \__, |\__\___|
         __/ |                               __/ |        
        |___/                               |___/         
    
    Blog:       https://parzibyte.me/blog
    Ayuda:      https://parzibyte.me/blog/contrataciones-ayuda/
    Contacto:   https://parzibyte.me/blog/contacto/
    
    Copyright (c) 2020 Luis Cabrera Benito
    Licenciado bajo la licencia MIT
    
    El texto de arriba debe ser incluido en cualquier redistribución
"""
archivo = "/home/esy9d7l1/Compliance/extracion/FT/Linux/pp"
salida = "result.txt"
busqueda = input("Ingresa búsqueda: ")
lineas_escribir = []
with open(archivo, "r") as archivo_lectura:
    numero_linea = 0
    print(busqueda)
    for linea in archivo_lectura:
        numero_linea += 1
        linea = linea.rstrip()
        separado = linea
        if busqueda in separado:
            lineas_escribir.append(str(numero_linea) + " - " + linea)

with open(salida, "w") as archivo_salida:
    for linea in lineas_escribir:
        archivo_salida.write(linea + "\n")