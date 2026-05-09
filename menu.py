# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 15:55:19 2024

@author: Joaquim Botelho Neves 110615 e Filipe Ribeiro Ferreira 110127
"""

""" 
Este script funciona como o main script. Esta script corre durante todo o 
programa. 
Funciona como um menu que permite escolher a implementação a executar, e armazena
a escolha de sala que pode ser feita na tier3
"""

from graphics import *
from Button import *
from sala import *


if True:
    win = GraphWin("Menu", 200, 400)
    titulo = Text(Point(100, 50), "MENU").draw(win)
    botao1 = Button(win, Point(100, 150), 150, 20, "Limpeza")
    botao2 = Button(win, Point(100, 200), 150, 20, "Entregas")
    botao3 = Button(win, Point(100, 250), 150, 20, "Salas")
    sair = Button(win, Point(100, 350), 100, 20, "Sair")

    botao1.activate()
    botao2.activate()
    botao3.activate()
    sair.activate()

    sala = "SALA01.txt"
    while True:
        e = win.getMouse()
        
        if sair.clicked(e) == True:
            win.close()
            break
        if botao1.clicked(e) == True:
            from tier1 import tier1
            tier1(sala)
        if botao2.clicked(e) == True:
            from tier2 import tier2
            tier2(sala)
        if botao3.clicked(e) == True:
            from tier3 import*
            sala = tier3(sala)