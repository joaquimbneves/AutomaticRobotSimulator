#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:47:55 2024

@author: Joaquim Botelho Neves 110615 e Filipe Ribeiro Ferreira 110127
"""
"""a tier 1 define a implemantação 1 e efetua a limpeza da totalidade da sala, 
atravez da lista clean da classe waiter. Este programa irá pedir sequencialmente
ao robo para se mover para o proximo ponto da lista, de porma a precorrer a 
totalidade da sala"""

from graphics import*
from Table import Table
from Waiter import Waiter
from Dock import Dock
from sala import *

"""
Esta função define a primeira implementação do projeto.
É criada uma sala e um robot que irá limpar na totalidade esta sala
"""

def tier1(sala):
    sdim = Sala(0,sala) # é necessário criar um objeto da classe sala para obter as dimensoes
    dim1, dim2 = sdim.getDim()
    win = GraphWin("Pressione 'M' para voltar para o Menu" , dim1 , dim2)
    win.setCoords(0, 0, 100, 100)
    win.setBackground("lightgrey")  
    sala = Sala(win, sala) #definimos a sala
    tables = sala.getMesas() #obtemos uma lista com todas as mesas para dps podermos prevenir colisões
    docks = sala.getDocks() #obtemos uma lista c as docks
    robo = Waiter(win, tables, docks, 1) #criamos o robot
    go = robo.Clean_path()
    recolha = Table(win,Point(10, 95) ,"rect", 0, 10, 20)
    recolha.create("burlywood", "burlywood")
    recolha.lable("BALCÃO")
    sala.createMesas() #desenhamos as mesas
    sala.createDocks()
    robo.create()
    #for i in range(len(go)):
        #Point((go[i])[0], (go[i])[1]).draw(win)
    while len(go) != 0:
        x, y = go[0]
        robo.Move(x,y)
        go.pop(0)
        menu = win.checkKey().upper()
        if menu == "M": #vontar para o menu se "m" ou "M" for clicado
            win.close()
            break
    if len(go) == 0: #quando a caba o movimento mostra mensagem e espera um impit para fechar
        msg = Text(Point(50,50), "Sala limpa")
        msg.setSize(30)
        msg.draw(win)
        menu = win.getKey()
        win.close()