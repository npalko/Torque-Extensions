"""
Methods to translate a torque.model.database object
    * Python Pickle
    * Torque XML 
and generate
    * LiteSQL C++ *.hpp files (http://sourceforge.net/apps/trac/litesql)
    * SQLAlchemy Schema *.py file
    
    
    
TODO
* how to convert between enums in model and enums used in XML doc
* convert to lxml, etree
* write own DTD
"""

import xml.dom.minidom

from __future__ import print_function
from torque import model



def loadFromXML(file):
    """load a Torque Database Schema XML file and return a model.database"""
    with open(file, 'r') as f:
        doc = xml.dom.minidom.parse(f)
    
    xmlDatabase = doc.getElementsByTagName('database')[0]
    database = model.Database(xmlDatabase.getAttribute('name'))
    return database
def writeToXML(database, file=None):
    """write model.database to a Torque Database Schema XML file"""
    
    doc = xml.dom.minidom.Document()
    # <!DOCTYPE database SYSTEM "http://db.apache.org/torque/dtd/database.dtd">
    
    xmlDatabase = doc.createElement('database')
    xmlDatabase.setAttribute('name', database.name)
    
    for table in database.getTable():
        xmlTable = doc.createElement('table')
        xmlTable.setAttribute('name', table.name)
        xmlTable.setAttribute('interfaceName', )
        xmlTable.setAttribute('description', )
            
        for column in table.getColumn():
            xmlColumn = doc.createElement('column')
            xmlColumn.setAttribute('name', column.name)
            xmlColumn.setAttribute('interfaceName', )
            xmlColumn.setAttribute('primaryKey', )
            xmlColumn.setAttribute('required', )
            xmlColumn.setAttribute('type', )
            xmlColumn.setAttribute('interfaceType', )
            xmlColumn.setAttribute('precision', )
            xmlColumn.setAttribute('scale', )
            xmlColumn.setAttribute('length', )
            xmlColumn.setAttribute('default', )
            xmlColumn.setAttribute('autoIncrement', )
            xmlColumn.setAttribute('description', )
            xmlTable.appendChild(xmlColumn)
            
        for index in table.getIndex():
            xmlIndex = doc.createElement('index')
            xmlIndex.setAttribute('name', index.name)
            xmlIndex.setAttribute('type', )
            xmlIndex.setAttribute('description', )
            for indexColumn in index.getColumn():
                xmlIndexColumn = doc.createElement('column')
                xmlIndexColumn.setAttribute('name', indexColumn.name)
                xmlIndex.appendChild(xmlIndexColumn)
            xmlTable.appendChild(xmlIndex)
            
        for foreignKey in table.getForeignKey():
            xmlForeignKey = doc.createElement('foreignKey')
            xmlForeignKey.setAttribute('name', foreignKey.name)
            xmlForeignKey.setAttribute('foreignTable', )
            xmlForeignKey.setAttribute('onUpdate', )
            xmlForeignKey.setAttribute('onDelete', )
                # column reference here
            xmlTable.appendChild(xmlForeignKey)       
            
        xmlDatabase.appendChild(xmlTable)
        
    doc.appendChild(xmlDatabase)
    
    if file is None:
        file = database.name + '.xml'    
    with open(file, 'w') as f:
        doc.writexml(f)



def writeToLiteSQL(database, file=None):
	pass
def writeToSQLAlchemy(database, file=None):
	pass
	

