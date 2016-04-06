"""
@author: Hamsavardhini, Dheepan
"""

#Main file 
	# --Which renders all the HTML
	# --Queries Neo4j to retrieve the result in JSON
	# --Prepares graph from JSON
	# --Invoke R prediction model
	# --Invoke 2 summarizers

#!/usr/bin/env python

import flask
from flask import request
from flask import render_template
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
import json
from retrieveStatements import *
from pprint import pprint
from summarizer1 import *
from summarizer3 import *
from prepareInputList import *
from predictionModel.callR import func


# Create the application.
APP = flask.Flask(__name__)

class graph:
    term = None
    ss=[]
    sum1= None
    sum2 = None
    pred = ''

@APP.route('/',methods=['POST','GET'])
def index():
    if(request.method == 'POST'):
        stmnts=[]
        input = request.form['term']
        data = None

        fromUser = input.split()
        inputList = prepare(fromUser)

        db = GraphDatabase("http://localhost:7474", username="neo4j", password="admin")

        query1 = "Match (n)-[r*1]-(c) where n.name IN ["
        query2 = "] return n,r,c"
        b=''
        for term in inputList:
            a = ''.join("\'" + term + "\'")
            if inputList[-1] != term:
                 b = b + a + ','
            else:
                 b = b + a
        print b
        #graph.term = True
        if True:
            q1 = query1 + b + query2
            results = db.query(q1, data_contents=True)
            data = results._get_graph()

            # # to create neo4j graph data
            # with open('ontodemoresult.json', 'w') as fp:
            #     json.dump(data, fp)

            if data:
                class nodes:
                    id = None
                    label = None
                    title = None
                    type = None

                class links:
                    source = None
                    target = None
                    type = None

                nodeslist=[nodes]
                linkslist=[links]

                def idIndex(a,id):
                    if a is not None:
                        for i,j in enumerate(a):
                            if j.id == id:
                                return i
                    return None

                for y in data:
                    z = y['nodes']
                    for x in z:
                        fnvalue = idIndex(nodeslist,x['id'])
                        if(fnvalue == None):
                            nodeobj = nodes()
                            nodeobj.id = x['id']
                            nodeobj.label = x['labels'] if x['labels'] else "NA"
                            nodeobj.title = x['properties'].values()[0] if bool(x['properties']) else "NA"
                            nodeobj.type = x['properties'].keys()[0] if bool(x['properties']) else "NA"

                            nodeslist.append(nodeobj)


                del[nodeslist[0]]# zeroth instance with None values as entries

                for y in data:
                    z = y['relationships']
                    for x in z:
                        linkobj = links()
                        linkobj.source = idIndex(nodeslist,x['startNode'])
                        linkobj.target = idIndex(nodeslist,x['endNode'])
                        linkobj.type = x['type']

                        if not (any((x.source == linkobj.source and x.target == linkobj.target and x.type == linkobj.type) for x in linkslist)):
                            linkslist.append(linkobj)

                del[linkslist[0]] # zeroth instance with None values as entries


                # print len(nodeslist)
                # print len(linkslist)

                with open('static/legalrelationtopics.json') as data_file:
                    jsontemplate = json.load(data_file)

                for key, value in jsontemplate.iteritems() :
                    if(key == "nodes"):
                        for x in nodeslist:
                            if x.title == graph.term:
                                groupvalue = 25
                            elif x.type == "Statement":
                                groupvalue = 10
                            elif x.type == "Parent":
                                groupvalue = 5
                            elif x.type == "Term":
                                groupvalue = 15
                            elif (x.type == "Child" or x.type == "Children"):
                                groupvalue = 20
                            else:
                                groupvalue = 10
                            value.append({"name":x.title,"type":x.type,"id":x.id,"group":groupvalue},)

                    if(key == "links"):
                        for x in linkslist:
                            value.append({"source":x.source,"target":x.target,"value":1},)

                #to generate json from dict object
                with open('static/result.json', 'w') as fp:
                    json.dump(jsontemplate, fp)

                graph.ss = []
                graph.ss = find_term()
                print len(graph.ss)

                '''for x in nodeslist:
                    if x.type == "Statement":
                        graph.ss.append(x.title)'''
                return flask.render_template('index.html',keyword=graph)
            else:
                data = []
        return flask.render_template('index.html')
    else:
        return flask.render_template('index.html')


@APP.route('/graphview', methods=['POST','GET'])
def graphview():
    #calls Summarizers -> summarizer1 and summarizer3
	graph.sum1 = ''.join(FrequencySummarizer().summarize(''.join(graph.ss).encode('ascii', 'ignore'), 5))
    graph.sum2 = ''.join(FrequencySummarizer().final())
    #calls prediction model
	f = open( 'predictionModel/Rinput.txt', 'r+')
    f.write( graph.sum2 )
    f.close()
    graph.pred = func()
    #graph.sum2 = statementsummarizer(''.join(graph.ss).encode('ascii', 'ignore'))
    return render_template('/statements.html',keyword=graph)

#Main is to run this framework standalone without any server
if __name__ == '__main__':
    APP.debug = True
    APP.run(port=5000)
