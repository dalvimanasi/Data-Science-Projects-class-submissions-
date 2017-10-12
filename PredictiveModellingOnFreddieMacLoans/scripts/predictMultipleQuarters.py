# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 23:33:54 2017

@author: visha
"""
from downloadPrediction import performregressionandclassification
import sys

def main():
    
    #config_file=loadConfig()
    #username=config_file['username']
    #password=config_file['password']
    
    args = sys.argv[1:]
    
    if len(args) != 4:
        print("Not enough arguments")
        exit(0)
        
    username=str(args[0])
    password=str(args[1])
    fromquarter=str(args[2])
    toquarter=str(args[3])
    
    startquarter = int(fromquarter[1])
    endquarter = int(toquarter[1])
    startyear=int(fromquarter[2:6])
    endyear=int(toquarter[2:6])
    
    currentquarter=startquarter
    currentyear=startyear
    
    breakloop=False
    breakloopprev=False
    while breakloop==False:
        
        analyzequarter="Q"+str(currentquarter)+str(currentyear)
        performregressionandclassification(username,password,analyzequarter)
        print(analyzequarter)
        if currentquarter < 4:
            currentquarter+=1
        elif currentquarter ==4:
            currentquarter=1
            currentyear = currentyear + 1
        if breakloopprev==True:
            break
        if ((currentyear==endyear) & (endquarter==currentquarter)):
            breakloopprev=True


if __name__ == '__main__':
    main()