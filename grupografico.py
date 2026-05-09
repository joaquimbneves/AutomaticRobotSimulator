# -*- coding: utf-8 -*-

"""
Created on Mon May 20 12:23:12 2024

@author: Joaquim Botelho Neves 110615 e Filipe Ribeiro Ferreira 110127
"""

from graphics import *

"""
Esta classe define um grupo gráfico, permitindo o movimento sincrono de multiplos
objetos. Utilizamos esta classe no projeto para que seja graficamente visivel o 
movimento do robo com um menu quando o robô vai receber um pedido
"""
class Grupo:
    def __init__(self,ancora):
        self.ancora = ancora
        self.objetos = [] #cria lista onde se vai guardar os objetos do grupo

    def addObj(self, objeto):
        self.objetos.append(objeto) #adiciona um objeto á lista
        
    def move(self, dx, dy): #movimento sincrono de todos os objetos
        for object in self.objetos:
            object.move(dx,dy)
        self.ancora.move(dx,dy)
    def draw(self, win): #desenha todos o grupo
        for object in self.objetos:
            object.draw(win)
    def undraw(self): #apaga todo o grupo
        for object in self.objetos:
            object.undraw()
                
    def remObj(self, obj, win): #remove um objeto especifico do grupo
        n = 0
        self.undraw() #apaga o grupo
        for i in self.objetos:
            if self.objetos[n] == obj:
                print(obj)
                self.objetos.pop(n) #remove o objeto
            n = n+1
        self.draw(win) #desenha o grupo, agora sem objeto   
                
    def getCenter(self):
        center = self.objetos[0].getCenter()
        return(center)
    def setFill(self, color):
        self.objetos[0].setFill(color)
    def setOutline(self, color):
        self.objetos[0].setOutline(color)