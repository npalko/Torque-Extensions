from __future__ import print_function

"""
Methods to translate a torque.model.database object
    * Torque XML 
and generate
    * LiteSQL C++ *.hpp files (http://sourceforge.net/apps/trac/litesql)
    * SQLAlchemy Schema *.py file
    
        
TODO
* write own DTD

http://stackoverflow.com/questions/15798/how-do-i-validate-xml-against-a-dtd-file-in-python


"""
import StringIO

from lxml import etree
from torque.model import SQLType, KeyAction

DTD = 'http://db.apache.org/torque/dtd/database.dtd'

TypeMap = {
	SQLType.INT:		'INT',
	SQLType.NVARCHAR:	'NVARCHAR',
	SQLType.DECIMAL:	'DECIMAL',
    SQLType.DATE:       'DATE'}
KeyActionMap = {
    KeyAction.CASCADE:  'CASCADE',
    KeyAction.SETNULL:  'SETNULL',
    KeyAction.RESTRICT: 'RESTRICT',
    KeyAction.NONE:     'NONE'}
BoolMap = {
    True:               'True',
    False:              'False'}


def loadFromXML(file):
    """load a Torque Database Schema XML file, verify it agains the DTD, and 
    return a model.database"""

    with open(file, 'r') as f:
        xmlDatabase = etree.parse(f)
    
    
    
    
    return xmlDatabase
def writeToXML(database, file=None, dtd=DTD):
    """write model.database to a Torque Database Schema XML file"""
    
    
    xmlDatabase = etree.Element('database', name=database.name)
        
    for table in database.getTable():
        xmlTable = etree.SubElement(xmlDatabase, 'table')
        a = xmlTable.attrib
        a['name'] = table.name
        if table.description is not None:
            a['description'] = table.description
            
        for column in table.getColumn():
            xmlColumn = etree.SubElement(xmlTable, 'column')
            a = xmlColumn.attrib
            a['name'] = column.name
            a['type'] = TypeMap[column.datatype]
            if column.description is not None:
                a['description'] = column.description
            if column.primaryKey:
                a['primaryKey'] = BoolMap[column.primaryKey]
            if column.autoIncrement:
                a['autoIncrement'] = BoolMap[column.autoIncrement]
            ##interfaceName='',
            ##required='',
            ##type='',
            ##interfaceType='',
            ##precision='',
            ##scale='',
            ##length='',
            ##default='',
            
        for index in table.getIndex():
            xmlIndex = etree.SubElement(xmlTable, 'index')
            a = xmlIndex.attrib
            ##'name', index.name)
            ##'type', )
            ##'description', )
            for indexColumn in index.getColumn():
                xmlIndexColumn = etree.SubElement(xmlIndex, 'column')
                a = xmlIndexColumn.attrib
                a['name'] = indexColumn.name
                
        for foreignKey in table.getForeignKey():
            xmlForeignKey = etree.SubElement(xmlTable, 'foreignKey')
            a = xmlForeignKey.attrib
            ##'name', foreignKey.name)
            ##'foreignTable', )
            ##'onUpdate', )
            ##'onDelete', )
            for foreignKeyColumn in foreignKey.getColumn():
                xmlForeignKeyColumn = etree.SubElement(foreignKey, 'column')
                a = foreignKeyColumn.attrib
                a['name'] = foreignKeyColumn.name

    # I can't believe we have to do this. Insert the DOCTYPE
    # make a function instead - insertDoctype
    
    doctype = '\n<!DOCTYPE database SYSTEM "%s">' % dtd    
    xmlString = etree.tostring(xmlDatabase, encoding='utf-8', 
        pretty_print=True, xml_declaration=True)
    endCarrot = xmlString.find('>') + 1

    if file is None:
        file = database.name + '.xml'    
    with open(file, 'w') as f:
        f.write(xmlString[:endCarrot])
        f.write(doctype)
        f.write(xmlString[endCarrot:])



