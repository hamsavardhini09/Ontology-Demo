"""
Created on Wed Jan 20 10:14:43 2016
@author: Hamsavardhini
"""
#File to get search keywords those that are present in ontology from the JSON result
#Invoked by retrieveStatements.py
#Invokes JSON result

import json

def filter():
    json_file = open("static/result.json")
    json_data = json.loads(json_file.read())
    nodeList = []
    for i in json_data:
        if i == 'nodes':
            valueList = json_data[i]
            for item in valueList:
                nodeList.append(item['name'].encode('ascii'))
    return nodeList

