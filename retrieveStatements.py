# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:14:43 2016
@author: Hamsavardhini
"""
#Get search keywords from 'getKeywords' function and 
#prepares a statments_list containing those filtered search keywords
#Invoked by neo4j.py
import os
import test

def find_term():
    nodeList=getKeywords.filter()
    stList=[]
    for term in nodeList:
        pathname = "Statements/"
        termlower = term.lower()

        for file in os.listdir("Statements/"):
            if file.endswith(".csv"):
                fname = pathname + file
                #print(fname)

                textfile=open(fname,"r")
                tempnewfile = textfile.readlines()

                for line in tempnewfile:
                    lineTest = line.lower()
                    answer = lineTest.find(termlower)
                    if answer != -1:
                        stList.append(line.decode("ascii",errors="ignore"));
    return stList

if __name__ == '__main__':
    find_term()