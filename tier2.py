#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:55:55 2024

@author: Joaquim Botelho Neves 110615 e Filipe Ribeiro Ferreira 110127
"""

""" a tier 2 define a segunda implementação em que o robo é capaz 
de receber clicks, armazenalos e corrrelos por ordem de forma a 
efetuar uma limpeza ou um serviço à mesa comforme o click é foora
ou dentro da mesa (respectivamente)"""

from graphics import*
from Table import Table
from Waiter import Waiter
from Dock import Dock
import time
from sala import*


def tier2(sala):
    sdim = Sala(0,sala) # é necessário criar um objeto da classe sala para obter as dimensoes
    dim1, dim2 = sdim.getDim()
    win = GraphWin("Pressione 'M' para voltar para o Menu" , dim1 , dim2)
    win.setCoords(0, 0, 100, 100)
    win.setBackground("lightgrey") 
    sala = Sala(win, sala)
    tables = sala.getMesas()
    docks = sala.getDocks()
    robo = Waiter(win, tables, docks, 2)
    recolha = Table(win,Point(10, 95) ,"rect", 0, 10, 20)
    recolha.create("burlywood", "burlywood")
    recolha.lable("BALCÃO")
    sala.createMesas() #desenhamos as mesas
    sala.createDocks()
    robo.create()
    robo
    while True:
        go_clean = True
        if len(robo.go) != 0:
            click = robo.go[0]
        else:
            click = win.checkMouse()
            if click != None:
                robo.go.append(click)
        pedido = [False, "a"]
        menu = win.checkKey().upper()
        if menu == "M": #vontar para o menu se "m" ou "M" for clicado
            win.close()
            break
        if click != None: #avalia se tem bateria para cumprir a funçao; uma ves que esta sempre a menos de 300 de uma dock
            click_x = click.getX()
            click_y = click.getY()
            for i in range(len(tables)): #avalia se o click e dentro de uma mesa; se for é um pedido e devolve True e a mesa do pedido
                if tables[i].clicked(click):
                    pedido = [True,i]
            for i in range(len(tables)):
                if tables[i].valid_clean_point(click_x, click_y) == False:
                    go_clean = False
                    break
            if pedido[0] == False and go_clean == True : # o click nao é numa; é valido mesa move-se para o ponto a limpar e efetua a limpeza
                msg = Text(Point(50,99), "A limpar...")
                msg.draw(win)
                robo.Move(click_x, click_y)
                robo.Clean(click_x, click_y)
                msg.undraw()
                
            if pedido[0] == False and go_clean == False : # o click nao é numa mesa; e nao é valido,mostra diz que nao é capaz de limpar o ponto
                msg = Text(Point(50,50), "Não é possível limpar esse ponto")
                msg.setSize(20)
                msg.draw(win)
                time.sleep(2)
                msg.undraw()
                
        
            if pedido[0] == True:            #o click é numa mesa logo o robo move se para o ponte definido como ponto de serviço e espera 2 seg para receber o pedido
                menu = Rectangle(robo.getCenter(), Point(robo.getCenter().getX()+2,robo.getCenter().getY()-2)) #cria a imagem gráfica do menu  
                menu.setFill("White")
                robo.addObj(menu) # adiciona o menu ao grupo do robo para que seja visivel e que se movam ao msm tempo
                #chegada de clientes
                marcador_clientes = Circle(tables[pedido[1]].center, 2)
                marcador_clientes.draw(win)
                marcador_clientes.setFill("green")
                marcador_clientes.setOutline("gold")
             
                #Dirigir ate à mesa e receber o pedido
                x = tables[pedido[1]].service_point().getX() #coord x/y do ponto de serviço
                y = tables[pedido[1]].service_point().getY()
                robo.Move(x, y)
                msg_1 = Text(Point(50,99), "A receber pedido...")
                msg_1.draw(win)
                time.sleep(2)
                msg_1.undraw()
                robo.remObj(menu, win) #após receber o pedido apaga-se o menu
            
                #Voltar para a Dock e confeciofar o pedido
                robo.dock()
                msg_2 = Text(Point(50,99), "A confecionar pedido...")
                msg_2.draw(win)
                time.sleep(5)
                msg_2.undraw()
                
                #Levar o pedido deste a zona de confeção à mesa, e voltar à dock
                msg_3 = Text(Point(50,99), "A entregar pedido...")
                msg_3.draw(win)
                robo.Move(3, 97)
                time.sleep(2)
                robo.Move(x, y)
                time.sleep(2)
                marcador_clientes.setFill("orange")
                tables[pedido[1]].draw_plates()
                tables[pedido[1]].draw_food()
                msg_3.undraw()
                robo.dock()
                time.sleep(3)
                tables[pedido[1]].undraw_food()
                marcador_clientes.undraw() #saida dos clientes
                
                
                #limpar a mesa apos os clientes sairem
                marcador_clientes.undraw() #saida dos clientes
                msg_4 = Text(Point(50,99), "Clientes acabaram; a limpar mesa... ")
                msg_4.draw(win)
                robo.Move(x, y)
                robo.clean_table(tables[pedido[1]])
                tables[pedido[1]].undraw_plates()
                robo.Move(x, y)
                msg_4.undraw()
                robo.dock()
                
                
            
            robo.go.pop(0)

        else:
            robo.dock()