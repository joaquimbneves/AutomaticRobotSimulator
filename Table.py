#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:43:47 2024

@author: Joaquim Botelho Neves 110615 e Filipe Ribeiro Ferreira 110127
"""

from graphics import*

def dist(p1, p2): #define a distancia entre dois pontos arredondada à segunda casa decimal
    xx, yy = p1.getX(), p1.getY()
    x, y = p2.getX(), p2.getY()
    distance = round(( (xx-x)**2+(yy-y)**2)**(1/2) , 2)
    return(distance)

"""esta classe define uma mesa, e capaz de receber o tipo de mesa e as suas dim (todas as dim devem ser preenchidas, independentemente
da relevancia para o tipo de mesa), desenha a mesa, e possui as funções necessatias para interagir com a mesa"""


class Table:

    
    def __init__(self , win , center , Type , radius , height , width):
        self.center = center
        self.win = win
        self.centerX = center.getX()
        self.centerY = center.getY()
        self.Type = str(Type)
        self.radius = radius
        self.height = height
        self.width = width
        X = self.centerX
        Y = self.centerY
        self.dx = self.width/2
        self.dy = self.height/2
        self.P1 = Point((X -self.dx),(Y - self.dy)) #bottom left point
        self.P2 = Point((X + self.dx),(Y + self.dy)) #top right point
        
        #define as coordenadas doa pratos e da comida relativamente ao centro, tipo e dimensoes das mesas
        if self.Type == "circ":
            self.dif_x = self.dif_y = self.radius/2
            self.rad = self.radius/4
        else:
            self.dif_y = self.width/4
            self.dif_x = self.height/4
            self.rad = (self.width+self.height)/16
        self.Plates = [Circle(Point(self.centerX,self.centerY+self.dif_y), self.rad), Circle(Point(self.centerX+self.dif_x,self.centerY), self.rad),
        Circle(Point(self.centerX,self.centerY-self.dif_y), self.rad), Circle(Point(self.centerX-self.dif_x,self.centerY), self.rad)]
        self.Food = [Circle(Point(self.centerX,self.centerY+self.dif_y), self.rad/2), Circle(Point(self.centerX+self.dif_x,self.centerY), self.rad/2),
        Circle(Point(self.centerX,self.centerY-self.dif_y), self.rad/2), Circle(Point(self.centerX-self.dif_x,self.centerY), self.rad/2)]
        
    
        
    def create(self, colour, outline):
        if self.Type == "circ":
            table = Circle( self.center , self.radius )
            table.draw(self.win)
            table.setFill(colour)
            table.setOutline(outline)
        elif self.Type == "rect":
            table = Rectangle(self.P1, self.P2)
            table.draw(self.win)
            table.setFill(colour)
            table.setOutline(outline)
    
    #desenha e da cor aos pratos
    def draw_plates(self):
        for plate in self.Plates:
            plate.setFill("white")
            plate.draw(self.win)
    
    #apaga os pratos
    def undraw_plates(self):
       for plate in self.Plates:
           plate.undraw()
    
    #desenha e da cor a comida
    def draw_food(self):
        for plate in self.Food:
            plate.setFill("salmon")
            plate.draw(self.win)
            
    #apaga a comida
    def undraw_food(self):
        for plate in self.Food:
            plate.undraw()
        
        
    #devolve as coordenadas significativas de cada mesa
    
    def get_coords(self):
        
        #retorna o centro e o raio se cor um circ 
        
        if self.Type == "circ":
            return [self.Type , self.center , self.radius]
        
        #retorna o canto inf esq e sup esq se a mesa for um rect
        
        elif self.Type == "rect":
            return [self.Type , self.P1 , self.P2]
        
        
    #verifica se o click é dentro ou fora de uma mesa e reetorna um bool
    def clicked(self , Point):
        self.click = Point
        self.clickX = Point.getX()
        self.clickY = Point.getY()
        #retorna True se o click esta a uma dist <= ao raio
        if self.Type == "circ":
            X = self.centerX
            Y = self.centerY
            x = self.clickX
            y = self.clickY
            #dx= distancia do click no eixo x 
            dx=abs(x-X)
            #dy= distancia do click no eixo x
            dy=abs(y-Y)
            #dist caldula a distancia do ponto clicado ao centro da circunferencia
            dist=((dx**2)+(dy**2))**(1/2)
            return( dist <= self.radius)
        
        #retorna Trua se o click é no interior da mesa retângular
        elif self.Type == "rect":
            #define as coord x e y dos cantos inf-esq e sup-dir
            p1X = self.P1.getX()
            p1Y = self.P1.getY()
            p2X = self.P2.getX()
            p2Y = self.P2.getY()

            return(p1X <= self.clickX <=p2X and p1Y <= self.clickY <= p2Y)
            
    
    
    def service_point(self): # devolve o ponto onde se vao buscar os pedidos
        
        if self.Type == "rect":
            return Point(self.P1.getX()+self.width/2, self.P1.getY()-3) #ponto encostado a mesa do lado esquerdo no meio
        else:
            return Point(self.centerX, self.centerY-self.radius-3) #ponto encostado a mesa do lado esquerdo no meio
    
    
    def valid_clean_point(self, x, y): #avalia se o ponto introduzido está a uma distancia suficente para ser limpo com o movimento circular
        
        #avalia de um movimento de limpeza vai colidir com a mesa   
        if self.Type == "rect" and self.P1.getX()-6 <= x <= self.P2.getX()+6 and self.P1.getY()-6 <= y <= self.P2.getY()+6:
            return False
        
        #avalia de um movimento de limpeza vai colidir com a mesa 
        if self.Type == "circ" and dist(Point(x,y), Point(self.centerX, self.centerY)) <= self.radius+6:
            return False
        
        #avalia de um movimento de limpeza vai colidir com a janela 
        if x <= 6 or  94<= x or y <= 6 or  94<= y:
            return False
        
        
    def lable(self, lable):
        lable = Text(self.center, str(lable))
        lable.draw(self.win)