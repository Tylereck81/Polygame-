import breakthrough
import minishogi
import othello8
import othello10
import einstein
import connect6
import pygame 
import os 

n = input() 
n = str(n) 
if n == "1": 
    minishogi.run() 
elif n == "2": 
    breakthrough.run() 
elif n == "3": 
    othello8.run() 
elif n == "4": 
    othello10.run() 
elif n == "5": 
    einstein.run() 
elif n == "6": 
    connect6.run()
    
