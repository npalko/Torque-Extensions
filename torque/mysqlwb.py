"""
Torque-Extensions interface to MySQL Workbench

Plugin capabilities:
    Export: 


physicalModel = grt.root.wb.doc.physicalModels[0]
database = torque.mysqlwb.adaptor(physicalModel)


"""
import grt
import torque.model

from wb import * # import the wb module, must be imported this way for the automatic module setup to work


DefineModule(name='PyWbUtils', author='Sun Microsystems Inc.', version='1.0')



def adaptor(physicalModel):
    """given a physicalModel from MySQL Workbench, return a 
    torque.model.database"""







# this is just a function used by the plugin, it’s not exported
def printTableLine(fields, filler= ' '):
  print '|',
  for text, size in fields:
    print text.ljust(size, filler), '|',
  print


# @wbexport makes this function be exported by the module and also describes the return and
# argument types of the function
# @wbplugin defines the name of the plugin to “wb.catalog.util.dumpColumns”, sets the caption to be
# shown in places like the menu, where to take input arguments from and also that it should be included
# in the Catalog submenu in Plugins.
@wbplugin(“wb.catalog.util.dumpColumns”, caption= “Dump All Table Columns”, input= [wbinputs.currentCatalog()], pluginMenu= “Catalog”)
@wbexport(grt.INT, grt.classes.db_Catalog)
def printAllColumns(catalog):
  lines= []
  schemalen= 0
  tablelen= 0
  columnlen= 0
  typelen= 0
  for schema in catalog.schemata:
    schemalen= max(schemalen, len(schema.name))
    for table in schema.tables:
      tablelen= max(tablelen, len(table.name))
      for column in table.columns:
        columnlen= max(columnlen, len(column.name))
        typelen= max(typelen, len(column.formattedType(1)))
        lines.append((schema.name, table.name, column.name, column.formattedType(1)))
  printTableLine([("-", schemalen),
    ("-", tablelen),
    ("-", columnlen),
    ("-", typelen)], “-”)
  printTableLine([("Schema", schemalen),
    ("Table", tablelen),
    ("Column", columnlen),
    ("Type", typelen)])
  printTableLine([("-", schemalen),
    ("-", tablelen),
    ("-", columnlen),
    ("-", typelen)], “-”)

  for s,t,c,dt in lines:
    printTableLine([(s, schemalen), (t, tablelen), (c, columnlen), (dt, typelen)])

  printTableLine([("-", schemalen),
    ("-", tablelen),
    ("-", columnlen),
    ("-", typelen)], “-”)
  span style=”color: #cdbe70?>print len(lines), “columns printed”

  return 0