"""
Torque-Extensions interface to MySQL Workbench

Plugin capabilities:
    Export: 



"""
import grt

from wb import * # required to dump namespace for module to work

DefineModule(name='Torque', author='Nicholas Palko', version='1.0')


# this is just a function used by the plugin, it�s not exported
def printTableLine(fields, filler= ' '):
  print '|',
  for text, size in fields:
    print text.ljust(size, filler), '|',
  print




# @wbplugin defines the name of the plugin to 'wb.catalog.util.dumpColumns', 
# sets the caption to be shown in places like the menu, where to take input 
# arguments from and also that it should be included in the Catalog submenu 
# in Plugins.

# @wbexport makes this function be exported by the module and also describes 
# the return and argument types of the function


@wbplugin('wb.catalog.util.dumpColumns', caption= 'Dump All Table Columns', 
    input= [wbinputs.currentCatalog()], pluginMenu='Catalog')
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
    ("-", typelen)], '-')
  printTableLine([("Schema", schemalen),
    ("Table", tablelen),
    ("Column", columnlen),
    ("Type", typelen)])
  printTableLine([("-", schemalen),
    ("-", tablelen),
    ("-", columnlen),
    ("-", typelen)], '-')

  for s,t,c,dt in lines:
    printTableLine([(s, schemalen), (t, tablelen), (c, columnlen), (dt, typelen)])

  printTableLine([("-", schemalen),
    ("-", tablelen),
    ("-", columnlen),
    ("-", typelen)], '-')

  return 0