from model.model import Model

myModel = Model()
myModel.buildGraph(2010, "circle")
n=myModel.getNumNodi()
a=myModel.getNumArchi()
print(n,a)