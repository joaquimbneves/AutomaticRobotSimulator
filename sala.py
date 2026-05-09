# -*- coding: utf-8 -*-
"""
Created on Tue May 14 19:47:54 2024

@author: Joaquim Botelho Neves 110615 e Filipe Ribeiro Ferreira 110127
"""
from graphics import *
from Table import Table
from Dock import Dock

def dist(p1, p2): #define a distancia entre dois pontos arredondada à segunda casa decimal
    xx, yy = p1.getX(), p1.getY()
    x, y = p2.getX(), p2.getY()
    distance = round(( (xx-x)**2+(yy-y)**2)**(1/2) , 2)
    return(distance)

""" esta classe é recponsavel por converter e devolver ficheiros de texto
 em listas de mesas e de docks com o formato que o programa reconhece"""

class Sala:
    def __init__(self, win, ficheiro):
        self.file = ficheiro
        self.win = win

    def getFile(self):#retorna o ficheiro que está a ser usado
        file = self.file
        return(file)
    

    def getMesas(self):
        sala = open(self.file)
        mesas = [] #cria a lista onde vamos guardar as mesas
        for line in sala: # para cada linha
            if line[0] == "T": # se começar com espaço ou comentario ignoramos
                if "table" in line or "Table" in line:
                    x1,y1 = map(int, line.split('(')[2].split(')')[0].split(','))#coordenadas ponto1
                    x2,y2 = map(int, line.split('(')[3].split(')')[0].split(','))#coordenadas ponto2
                    center = Point((x1+x2)/2, (y1+y2)/2) #ponto médio/centro
                    raio = dist(Point(x1,y1), Point(x2,y2))/2
                    height = abs((y2-y1))
                    width = abs((x2-x1))
                    print(center)
                    print(height,width)
                    
                    if "Circle" in line: tipo = "circ" # se mesa for circular 
                    if "Rectangle" in line: tipo = "rect"  # se for retangular
                        
                    mesa = Table(self.win, center, tipo, raio, height, width)
                    mesas.append(mesa)
                            
        return(mesas)
    
    def getDocks(self):
        sala = open(self.file)
        docks = []
        for line in sala: 
            if "Dock" in line:
                x1,y1 = map(int, line.split('(')[2].split(')')[0].split(',')) 
                x2,y2 = map(int, line.split('(')[3].split(')')[0].split(','))
                p1,p2 = Point(x1,y1), Point(x2,y2)
                dock = Dock(self.win, p1, p2)
                docks.append(dock)
                
        return(docks)
    
    def getDim(self):
        sala = open(self.file)
        for line in sala:
            if "Dim" in line:
                x,y = map(int, line.split("(")[1].split(")")[0].split(","))
        return(x,y)
    
    def createMesas(self):
        for table in self.getMesas():
            table.create("goldenrod", "darkgoldenrod")
            
    def createDocks(self):
        for dock in self.getDocks():
            dock.create()