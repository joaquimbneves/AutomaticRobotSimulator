#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:22:32 2024

@author: Joaquim Botelho Neves 110615 e Filipe Ribeiro Ferreira 110127
"""

from graphics import*
from Button import*
from Dock import*
from Table import*


#função para criar um ficheiro SALANN.txt costumizado
def customize():
    Tables = []
    win = GraphWin("Customize a sua sala" , 600 , 600)
    win.setCoords(0, 0, 100, 100)
    win.setBackground("lightgrey")
    Tables = []
    Sair= Button(win, Point(30, 10), 30, 7, "Sair")
    Enter = Button(win, Point(70, 10), 30, 7, "Enter")
    Sair.activate()
    Enter.activate()
    
    
    Msg = Text(Point(50,98), "Indiique as cordenadas das mesas que quere. (min-1; max-6)")
    Msg.setSize(15)
    Msg.draw(win)
    Msg1 = Text(Point(50,94), """Clique no fundo para continuar e em Enter quando acabar
    Se a mesa estiver demasiado perto de uma parede não será desenhada""")
    Msg1.draw(win)
    
    
    #um loop que no maximo rorre seis vezes para receber as coordenadas das mesas
    for i in range(6):
        Enter.deactivate()
        
        #desena a mensagem na promeira linha da mesa e do numero
        mesa = Text(Point(10, 100-(i*7+12)), f"Mesa{i+1}")
        mesa.draw(win)
        
        #desena na linha as caixas de texto para as coord do ponto P1
        P1_msg = Text(Point(45, 100-(i*7+12)), "P1")
        P1_msg.draw(win)
        P1_X = Entry(Point(50,100-(i*7+12)), 3)
        P1_X.draw(win)
        virgula = Text(Point(54, 100-(i*7+12)), ",")
        virgula.draw(win)
        P1_Y = Entry(Point(57,100-(i*7+12)), 3)
        P1_Y.draw(win)
        
        #desena na linha as caixas de texto para as coord do ponto P2
        P2_msg = Text(Point(67, 100-(i*7+12)), "P2")
        P2_msg.draw(win)
        P2_X = Entry(Point(72,100-(i*7+12)), 3)
        P2_X.draw(win)
        virgula = Text(Point(76, 100-(i*7+12)), ",")
        virgula.draw(win)
        P2_Y = Entry(Point(79,100-(i*7+12)), 3)
        P2_Y.draw(win)
        
        #desena na linha as caixas de texto para receber o tipo de mesa
        Type_msg = Text(Point(25, 100-(i*7+12)), '"circ" ou "rect"')
        Type_msg.draw(win)
        Type = Entry(Point(35, 100-(i*7+12)), 4)
        Type.draw(win)
        
        #avalia se o utilizador quere sair e faz uma pausa para poder guardar os dados
        c = win.getMouse()
        if Sair.clicked(c):
            win.close()
            return
        
        #guarda os dados dos pontos
        P1x,P1y = int(P1_X.getText()), int(P1_Y.getText())
        P2x,P2y = int(P2_X.getText()), int(P2_Y.getText())
        Type = str(Type.getText())
        
            
        Enter.activate()
        click = win.getMouse()
      
        
      
        if Type == "circ": #falta verificar se é valida
            Tables.append(f"Table{i+1} Circle(Point({P1x},{P1y}),Point({P2x},{P2y}))")
        
        #se a mesa é um rect e nao esta demadiado perto de uma parede, adciona à lista Tables o formato correto de uma mesa rect, para depos adicionar ao ficheiro
        if Type == "rect" and 6 < P1x < 94 and 6 < P1y < 94 and 6 < P2x < 94 and 6 < P2y < 94 :
            Tables.append(f"Table{i+1} Rectangle(Point({P1x},{P1y}),Point({P2x},{P2y}))")
        
        if Sair.clicked(click):
            win.close()
            return
        
        if Enter.clicked(click):
            break
    
        
    #ativa dois botoes para o utilizador indicar onde quere a segunda dock
    #guarda o formado adequado para depois adicionar ao ficheiro
    Msg = Text(Point(50,40), "Escolha onde quere a Segunda Dock")
    Msg.setSize(15)
    Msg.draw(win)
    botao1 = Button(win, Point(25, 30), 30, 7, "Canto Inf-Dir")
    botao2 = Button(win, Point(75, 30), 30, 7, "Canto Sup-Dir")
    botao1.activate()
    botao2.activate()
    Enter.deactivate()
    click = win.getMouse()
    if click != None:
           if botao1.clicked(click):
               Dock = "Dock2 Rectangle(Point(94,0), Point(100,6))"
           if botao2.clicked(click):
               Dock = "Dock2 Rectangle(Point(94,94), Point(100,100))"
           if Sair.clicked(click):
               win.close()
               return
           
    #adiciona linha a linha ao ficheiro o formato correto da sala costumizada
    with open('SALA_CUST.txt', 'w') as file:
        file.write('#Sala 2\n')
        file.write('#Autoria de Filipe Ribeiro e Joaquim Neves\n')
        file.write('Dimensões (900,700)\n')
        file.write('Dock1 Rectangle(Point(0,0), Point(6,6))\n')
        file.write(f'{Dock}\n')
        for table in Tables:
            file.write(f'{table}\n')
        
        
    win.close()
    return