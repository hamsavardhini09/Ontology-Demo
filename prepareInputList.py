"""
@author: Hamsavardhini
"""
#prepares a list of keywords present in both 'search query' and 'ontology'
#Invoked by neo4j.py

from neo4jrestclient.client import GraphDatabase

def prepare(fromUser):
    db = GraphDatabase("http://localhost:7474", username="neo4j", password="admin")
    nodesQuery = "MATCH (n) RETURN n.name"
    nodeValues = db.query(nodesQuery, data_contents=True)
    inputList = []
    input = []

    for i in range(0,len(nodeValues)):
        inputList.append(nodeValues[i][0])
        #print inputList[i]

    for item in fromUser:
        if item in inputList:
            input.append(item)

    return input
