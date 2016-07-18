
import os
import csv

import singleImport

javapath = "../out/artifacts/CBLP_jar/CBLP.jar"
os.environ['CLASSPATH'] = javapath

from jnius import autoclass

count = 0
for rt, dirs, files in os.walk('../TrajData/Geolife'):
    for fname in files:
        count += 1
        print "file" + str(count) + "importing"
        singleImport.loadtrace(open(rt+'/'+fname))

        print "predicting"
        precisions = []
        PyInterface = autoclass('markov.analysis.PyInterface')
        precision = PyInterface.getPrecision(0, 0)
        precisions.append(tuple(precision))
        singleImport.refresh()
        precision = PyInterface.getPrecision(1, 0)
        precisions.append(tuple(precision))
        singleImport.refresh()
        precision = PyInterface.getPrecision(1, 1)
        precisions.append(tuple(precision))
        singleImport.refresh()
        precision = PyInterface.getPrecision(2, 0)
        precisions.append(tuple(precision))
        singleImport.refresh()
        precision = PyInterface.getPrecision(2, 1)
        precisions.append(tuple(precision))
        singleImport.refresh()
        precision = PyInterface.getPrecision(2, 2)
        precisions.append(tuple(precision))
        singleImport.refresh()
        precision = PyInterface.getPrecision(3, 0)
        precisions.append(tuple(precision))
        singleImport.refresh()
        precision = PyInterface.getPrecision(3, 1)
        precisions.append(tuple(precision))
        singleImport.refresh()
        precision = PyInterface.getPrecision(3, 2)
        precisions.append(tuple(precision))

        out = open('../Precisions/'+fname, mode="wb")
        writer = csv.writer(out)
        writer.writerows(precisions)
        out.close()