import sys
sys.path.append('C:\Users\Nicholas Palko\Documents\Development\Torque-Extensions')
import torque.adaptor

physicalModel = grt.root.wb.doc.physicalModels[0]

reload(torque.model)
reload(torque.adaptor)
wbAdaptor = torque.adaptor.MySQLWorkbench()
database = wbAdaptor.toModel(schemata)

xw = torque.adaptor.XML()
xw.write(database)

