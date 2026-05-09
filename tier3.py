# -*- coding: utf-8 -*-
"""
Created on Wed May 15 22:41:32 2024

@author: Joaquim Botelho Neves 110615 e Filipe Ribeiro Ferreira 110127
"""
"""a tier 3 define a terceira implementação, apenas devolve a sala escolhida para ser 
desenhada nas outras implementações"""

from graphics import *
from Button import *
from sala import *
from customize import*
#MenuCall faz com q se crie uma nova janela em que surge o menu, pensei em criar uma classe mas so há este menu, que é sempre igual

def tier3(sala):
    win = GraphWin("Salas", 200, 400)
    titulo = Text(Point(100, 50), "Escolha uma sala").draw(win)
    botao1 = Button(win, Point(100, 120), 150, 20, "Sala 1")
    botao2 = Button(win, Point(100, 170), 150, 20, "Sala 2")
    botao3 = Button(win, Point(100, 220), 150, 20, "Sala 3")
    costumizar = Button(win, Point(100, 270), 150, 20, "Customizar")
    sair = Button(win, Point(100, 350), 100, 20, "Sair")

    botao1.activate()
    botao2.activate()
    botao3.activate()
    costumizar.activate()
    sair.activate()


    while True:
        e = win.getMouse()
        
        if sair.clicked(e) == True:
            win.close()
            return sala
            
        if botao1.clicked(e) == True:
            win.close()
            return("SALA01.txt")
            
        if botao2.clicked(e) == True:
            win.close()
            return("SALA02.txt")
        
        if botao3.clicked(e) == True:
            win.close()
            return("SALA03.txt")
        
        if costumizar.clicked(e) == True:
            customize()
            win.close()
            return("SALA_CUST.txt")