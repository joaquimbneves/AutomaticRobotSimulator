
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:05:02 2024

@author: Joaquim Botelho Neves 110615 e Filipe Ribeiro Ferreira 110127
"""

from graphics import*
from Table import Table
from Dock import Dock
import math
import time
from grupografico import Grupo

def dist(p1, p2): #define a distancia entre dois pontos arredondada à segunda casa decimal
    xx, yy = p1.getX(), p1.getY()
    x, y = p2.getX(), p2.getY()
    distance = round(( (xx-x)**2+(yy-y)**2)**(1/2) , 2)
    return(distance)

"""a classe waiter define e cria o robo, todos os seus metodos de movimento e de 
contornaçãode obstaculos"""

class Waiter:
    def __init__(self , win, tables, docks, implemantation):
        self.win = win
        centre = Point(3, 3)
        grupog = Grupo(Point(3,3))
        grupog.addObj(Circle(centre , 3))
        self.robot = grupog #cria a parte grafica do robo como um grupo grafico
        self.robot.setFill("cadetblue")
        self.robot.setOutline("cadetblue")
        self.centre = self.robot.getCenter()
        self.battery = 6500#valor inicial da bateria; equivalente a varrer a sala duas vezes 
        self.tables = tables
        self.docks = docks
        self.implemantation = implemantation
        self.go = []
        self.battery_indicator = Text(Point(3,3), "100%")#indicação do valor inicial da beteria
        self.battery_indicator.draw(self.win)
        
    def getCenter(self):
        return(self.robot.getCenter())

    
    def addObj(self, obj):
        self.robot.addObj(obj)
        self.robot.undraw()
        self.robot.draw(self.win)
        
    def remObj(self, obj, win):

        self.robot.remObj(obj, self.win)
        self.robot.undraw()
        self.robot.draw(win)
    
    def create(self): #desenha o robo
        self.robot.draw(self.win)
        self.robot.setFill("cadetblue")
        self.robot.setOutline("cadetblue")
        
        
    def change_colour(self, colour): #muda a cor do robo; tendo 4 possives cpres associadas a numeros
        if colour == 0:
            self.robot.setFill("cadetblue")
            self.robot.setOutline("cadetblue")
        elif colour == 1:
            self.robot.setFill("green")
            self.robot.setOutline("gold")
        elif colour == 2:
            self.robot.setFill("red")
            self.robot.setOutline("red")
        elif colour == 3:
            self.robot.setFill("orange")
            self.robot.setOutline("orange")
            
        
    #recebe a lista de mesas e o movimento que vai fazer 
    #avalia se o proximo movimento vai ser uma colisao
    #se for colisao devolve verdadeiro e a mesa com que colide
    def colision(self, x, y): 
        cntr = self.robot.getCenter()
        next_x = cntr.getX()+x #coord x/y do proximo ponto
        next_y = cntr.getY()+y
        for table in self.tables: #ciclo para avaliar a lista de mesas
            coords = table.get_coords()
            
            if coords[0] == "rect":
                p1, p2 = coords[1], coords[2]
                if (next_x+3 > p1.getX()  and next_x-3 < p2.getX() and next_y+3 > p1.getY() and next_y-3 < p2.getY() ) : # se o proximo movimento colide com a mesa retangular
                    return [True,table]
                    
            if table.Type == "circ":
                if dist(coords[1], Point(next_x, next_y)) < coords[2]+3:
                    return [True, table]
        return [False, 0]
            
        
    def Move(self ,x ,y): #funcao para mover o robo para o ponto introduzido; e que avalia e evita colisao com as mesas com auxilio da func avoid e MOVE_avoid
            araival = False
            bat_perc = self.battery_percentage()
            while araival == False: #enquanto nao chega ao ponto pedido move se na direção dele atravez do vetor normalizado
                
                #avalia se o valor da percentagem se altera de forma a evitar redesenhar desnecessariamente
                #redesanha o valor da perçentagem da bateria
                if bat_perc != self.battery_percentage():
                    self.battery_indicator.undraw()
                    self.battery_indicator = Text(Point(3,3), (str(self.battery_percentage()),"%"))
                    self.battery_indicator.draw(self.win)
                
                bat_perc = self.battery_percentage()
                
                
                if self.implemantation == 2: #no caso da implementação 2 o adiciona os pontos clicados a uma lista de pontos para ir
                    click = self.win.checkMouse()
                    if click !=None:
                        self.go.append(click)
                        
                        
                if self.battery < 300: #se a bateria é inferior a 300 (valor suficiente para retornar à dock); recarrega
                    self.recharge()
                    
                #variaveis usadas para o movimento
                cent = self.robot.getCenter()
                dx = x-cent.getX()
                dy = y-cent.getY()
                distance = dist(Point(x, y), cent)
                
                #calcula o vetor diretor se dist!=0 para nao divitir por 0
                if distance != 0:
                    X = dx/(2*distance) # x/y do vetor normalizado
                    Y = dy/(2*distance) # 2*distance para os incrementos serem mais pequenos e o movimento sem mais suave
                    
                if self.colision(X, Y)[0] == False: #se nao há colisao move-se
                    self.robot.move(X, Y) #move-se um incremento (X,Y) na direçao do ponto pretendido
                    self.battery -= dist(Point(0,0), Point(X, Y)) #subtrai a bateria o valor da distancia percorrida
                    
                    if distance <= 1: #avalia se o robo ja chegou
                        araival = True
                        
                elif self.colision(X, Y)[0] == True: #no caso de haver colisao; chama a func avoid
                    table = self.colision (X, Y)[1]
                    self.Avoid(table)
                    
                update(60)
                
    #funcao que auxilia movimento para contornar a mesa
    #muito parecida com o Move; mas nao avalia a colisao 
    #uma vez que so é utilizada para pontos que nao colidem
        
    def MOVE_avoid(self ,x ,y): #funcao que auxilia movimento para contornar a mesa
        araival = False
        while araival == False: #enquanto nao chega ao ponto pedido move se na direção dele atravez do vetor normalizado
            cent = self.robot.getCenter()
            dx = x-cent.getX()
            dy = y-cent.getY()
            distance = dist(Point(x, y), cent)
            if distance != 0:
                X = dx/(2*distance)  # x/y do vetor normalizado
                Y = dy/(2*distance)  #2*distance para os incrementos serem mais pequenos e o movimento sem mais suave
                self.robot.move(X, Y)
                self.battery -= dist(Point(0,0), Point(X, Y)) #subtrai a bateria o valor da distancia percorrida)
            if distance <= 1: #avalia se o robo ja chegou
                araival = True
            update(60)
    
    #returns the betery in percentege
    def battery_percentage(self):
        return round(self.battery/65)
    
    # recarrega o robo 
    def recharge(self):
        msg = Text(Point(50,97), "A carregar...")
        self.battery = 6500
        self.change_colour(2)
        self.dock()
        msg.draw(self.win)
        self.change_colour(1)
        time.sleep(2)
        self.change_colour(0)
        msg.undraw()
        
   
   #contornar mesas quando esta em colisao
   #avalia o tipo de colisao e faz um movimento para contornar essa colisao
   #se para chegar ao ponto pretendido continuar em colisao, a função move chama o avoid outra vez
    def Avoid(self, table): #reçebe a mesa que tem que contornar
        x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()
        coords = table.get_coords()
        
        
        #contornar uma mesa retangular
        #com "redundância" nos cantos para evitar erros 
        if coords[0] == "rect":
            P1, P2 = coords[1], coords[2] #canto inf esq, canto sup dir
            P1_ = Point(P1.getX(), P2.getY()) #canto sup esq
            P2_ = Point(P2.getX(), P1.getY()) #canto inf dir
            if (y >= P2.getY()+3) or (y == P2.getY()+3 and x == P1.getX()-3): # se está na face superior ou no canto sup esq; vai para o canto sup dir 
                self.MOVE_avoid(P2.getX()+3, P2.getY()+3)
            if (y <= P1.getY()-3) or (y == P1.getY()-3 and x == P2.getX()+3): # se está na face inferior ou no canto inf dir; vai para o canto inf esq
                self.MOVE_avoid(P1.getX()-3, P1.getY()-3)
            if (x > P2.getX() and y > P1.getY()-3 and y < P2.getY()+3) or (y == P2.getY()+3 and x == P2.getX()+3): # se está na face direita ou no canto sup dir;, vai para o canto inf dir
                self.MOVE_avoid(P2_.getX()+3, P2_.getY()-3)
            if (x < P1.getX() and y > P1.getY()-3 and y < P2.getY()+3) or (y == P1.getY()-3 and x == P1.getX()-3): # se está na face esquerda ou no canto inf esq vai para o canto sup esq
                self.MOVE_avoid(P1_.getX()-3, P1_.getY()+3)
                
                
        #contornar uma mesa circular
        #atravez do centro da mesa e do robo, calcula um vetor normalizado que une os centros
        #efetua o movimento de um vetor perpendicular a esse vetor, de vorma a contornar a mesa circular
        else:
            table_center = coords[1]
            tab_center_x = table_center.getX()
            tab_center_y = table_center.getY()
            dist = coords[2]+3
            self.MOVE_avoid(x+(y-tab_center_y)/dist, y-(x-tab_center_x)/dist) # movimento para o ponto onde o robo se enconta mais o incremento na direção perpendicular
            
    # move o robo num movimento circular de limpeza
    def Clean(self, x, y):
        clean_area = Circle(Point(x,y), 6)
        clean_area.draw(self.win)
        for i in range(7):
            self.Move(x+3*math.cos(i),y+3*math.sin(i))
        clean_area.undraw()
        
        
        
    #Precorre o perimetro da mesa
    def clean_table(self, table):
        coords = table.get_coords()
        
        #move o robo para os quatro cantos da mesa sucesivamente 
        if coords[0] == "rect":
            P1, P2 = coords[1], coords[2] #canto inf esq, canto sup dir
            P1_ = Point(P1.getX(), P2.getY()) #canto sup esq
            P2_ = Point(P2.getX(), P1.getY()) #canto inf dir
            self.MOVE_avoid(P1.getX()-3, P1.getY()-3)
            self.MOVE_avoid(P1_.getX()-3, P1_.getY()+3)
            self.MOVE_avoid(P2.getX()+3, P2.getY()+3)
            self.MOVE_avoid(P2_.getX()+3, P2_.getY()-3)
            
        
        #move o bobo para dois lados opostos da mesa circular
        #devido a forma como a função move esta definida estes dois pontos asseguram uma volta completa
        else:
            self.Move(coords[1].getX(), coords[1].getY()+coords[2]+3)
            self.Move(coords[1].getX()+coords[2]+3, coords[1].getY())
            
        
            

    #cria um caminho de zige-zage que precorre a totalidade do restaurante, numa lista
    #avalia as mesas e remove os pontos que colidiriam com uma mesa
    def Clean_path(self):
        
        """fazer um caminho de limpeza sem considerar as mesas"""
        
        clean = []
        for row in range(32): #uma vez que o raio co robo é 3 e a largura é 100; logo haverá um terço das colunas precorridas
            if row % 2 == 0: #para as colunas pares adiciona pontos de baixo para cima
                for colum in range(32):
                    clean.append([3*row+3,3*colum+3])
            else:
                for colum in range(colum, -1, -1): #para colunas impares adiciona pontos de cima para baixo
                    clean.append([3*row+3, 3*colum+3])
                    
        if [self.centre.getX(),self.centre.getY()] in clean: #remove o ponto se for igual a pocição do robo
            clean.remove([self.centre.getX(),self.centre.getY()])#falta adicionar o ponto da dock final para acabar na dock
            
        tabls = [] #lista com as coordenadas das mesas
        for i in self.tables:
            tabls.append(i.get_coords())

        """fazer uma lista com os pontos onde o robo nao pode passar para depois eliminar ao clean"""

        avoid = [] #lista com as coordenadas a evitar
        #corre a lista de mesas e cria uma lista avoid com todos os pontos a evitar
        for i in range(len(tabls)):
            
            if (tabls[0])[0] == "rect": #no casso de ser uma mesa retangular
                xmin = (tabls[0])[1].getX()-3
                xmax = (tabls[0])[2].getX()+3
                ymin = (tabls[0])[1].getY()-3
                ymax = (tabls[0])[2].getY()+3
                for x in range(int(xmax-xmin+1)):  #loop que aliciona todos os pontos a evitar
                    for y in range(int(ymax-ymin+1)):
                        avoid.append([xmin+x,ymin+y])#tem um problema que so soma 3 no min e nao no max
                tabls.pop(0)
            
            else: #no caso de ser uma mesa circular
                X = (tabls[0])[1].getX()
                Y = (tabls[0])[1].getY()
                
                for point in clean: #se um ponto da lista clean colide com a mesa circular, adiciona se à lista avoid
                    x, y = point
                    if dist(Point(X,Y), Point(x,y)) <= ((tabls[0])[2]+3): #se a distancia entre o ponto e o centro é menor ao rio do robo + da mesa
                        avoid.append(point)
                tabls.pop(0)
                
        """loop para remover os pontos da lista avoid à lista clean"""
        
        for i in range(len(clean)+len(avoid)):
            if len(avoid) != 0:
                if avoid[0] in clean:
                    clean.remove(avoid[0])
                else:
                    avoid.pop(0)
            else:
                break
        clean.append([self.docks[1].get_X(),self.docks[1].get_Y()])#para adicionar o ponto da ultima dock
            
        return clean #devolve a lista clean que é uma lista com um padrao de limpeza de zige-zage sem os pontos que colidem com as mesas
    
    def dock(self): #funçao que volta para a dock mais proxima
        cent = self.robot.getCenter()
        x1 = self.docks[0].get_X() #coordenada x da dock 1
        y1 = self.docks[0].get_Y()#coordenada y da dock 1
        x2 = self.docks[1].get_X()#coordenada x da dock 2
        y2 = self.docks[1].get_Y()#coordenada y da dock 2
        X = cent.getX()#coordenada x do centro do robo em cada instante
        Y = cent.getY()#coordenada y do centro do robo em cada instante
        dist1 = dist(Point(X,Y), Point(x1,y1))#distancia do robo a dock 1
        dist2 = dist(Point(X,Y), Point(x2,y2))#distancia do robo a dock 2
        if dist1 <= dist2 and dist1>0.5 and dist2>0.5:
            self.Move(x1,y1)
        if dist1 > dist2 and dist1>0.5 and dist2>0.5:#arranjar uma forma melhor de parar a oscilaçao,(melhor que este 0,5)
            self.Move(x2,y2)