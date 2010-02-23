import os
import grt

print os.getcwd()

model = grt.root.wb.doc.physicalModels[0]
for tab in model.catalog.schemata[0].tables:
    print "Table: `%s`" % (tab.name)