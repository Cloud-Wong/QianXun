from flask import Flask, jsonify, render_template , url_for , redirect
from py2neo import Graph, NodeMatcher,RelationshipMatcher,Node,walk,Relationship,Cursor
from datetime import timedelta

app = Flask(__name__) #flask框架必备
app.config ['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


graph = Graph("http://127.0.0.1:7474", username="neo4j", password="123456")
node_matcher = NodeMatcher(graph)
r_matcher = RelationshipMatcher(graph)

#start_sue = node_matcher.match(state='未完成',event='审理起诉').first()
#caseShall = node_matcher.match(state='未完成',event='受理').first()


def buildNodes(nodeRecord): #构建web显示节点
    data = {"id": nodeRecord.__name__, "label": list(nodeRecord._labels)[0]} #将集合元素变为list，然后取出值
    data.update(dict(nodeRecord))
    return {"data": data}


def buildEdges(relationRecord): #构建web显示边
    x = ''
    for i in relationRecord.types():
        x = i
    data = {"source": relationRecord.start_node.__name__,
            "target":relationRecord.end_node.__name__,
            "relationship": x,
            "desc":relationRecord['describe']
            }
    return {"data": data}


@app.route('/')
def index():


    return render_template('index.html')





@app.route('/graph')
def graph():
    node = node_matcher.match()  # 显示所有节点
    relation = r_matcher.match()  # 显示所有关系

    nodeList = list(node)
    edgeList = list(relation)

    nodes = list(map(buildNodes, nodeList))
    edges = list(map(buildEdges, edgeList))
    print({"nodes": nodes, "edges": edges})
    #print(jsonify(elements = {"nodes": nodes, "edges": edges}))
    return jsonify(elements = {"nodes": nodes, "edges": edges})


if __name__ == '__main__':
    app.run(debug = True)
#a=  map(dict,node
#print(list(a))