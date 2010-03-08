import sys
sys.path.append('C:\Users\Nicholas Palko\Documents\Development\Torque-Extensions')
import torque

schemata = grt.root.wb.doc.physicalModels[0].catalog.schemata[0]

reload(torque)
wbAdaptor = torque.adaptor.MySQLWorkbench()
db = wbAdaptor.toModel(schemata)

xw = torque.adaptor.XML()
xw.write(db)

