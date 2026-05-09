#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 10:32:15 2024

@author: Joaquim Botelho Neves 110615 e Filipe Ribeiro Ferreira 110127
"""

from graphics import*

class Dock:
    def __init__(self, win, p1, p2):
        self.win = win
        self.p1 = p1
        self.p2 = p2
        
    def create(self):
        dock1 = Rectangle(self.p1, self.p2)
        dock1.draw(self.win)
        dock1.setFill("beige")
        dock1.setOutline("khaki")
        
    def get_X(self):
        x1 = self.p1.getX()
        x2 = self.p2.getX()
        X = x1 + ((x2-x1)/2)
        return(X)
    
    def get_Y(self):
        y1 = self.p1.getY()
        y2 = self.p2.getY()
        Y = y1 + ((y2-y1)/2)
        return(Y)