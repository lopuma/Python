#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

def opciones():
    print('''
    MENU DE APLICACIONES:
    1- APP Compliance
    2- Recortar
    3- Salir
    ''')
    while True:
        centinela = input("Elige una OPCION ?: ")
        if centinela in ["1", "2", "3"]:
            return centinela
        print("[!] Opcion no valida, reintente\n")

def solve(s):
    words = s.split()
    if len(words) <= 1:
        full_name = [w.capitalize() if '/' not in w and w[1:-1].upper() not in w else w[0].upper()+w[1:] for w in words]
    elif len(words) >= 2:
        full_name = words
    return ' '.join(full_name)

def acciones(centinela):
    if centinela == "1":
        s = input()
        result = solve(s)
        print(result)
        os.popen('/home/esy9f47u/Compliance/Compliance')
    elif centinela == "2":
        os.popen('gtk-launch myScream.desktop')
    elif centinela == "3":
        print("Adios") 

opt = opciones()
acciones(opt)
