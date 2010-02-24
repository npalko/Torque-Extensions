from __future__ import print_function

import cPickle as pickle
from torque.model import SQLType, KeyAction

try:
    from lxml import etree
except ImportError:
    print('Couldn''t load lxml. XML IO not available')

	
class MySQLAdaptor(object):
	def __init__(self):
		pass
	def toModel(self, physicalModel):
		"""
			physicalModel = grt.root.wb.doc.physicalModels[0]
			database = torque.mysqlwb.adaptor(physicalModel)
		
		"""
		pass

class XML(object):
    def __init__(self, dtd='torque-extensions.dtd'):
    
        # create bi-directional mapping between types in torque.model and text
        # expected in XML file
        
        types = [(SQLType.INT, 'INT'),
            (SQLType.NVARCHAR,'NVARCHAR'),
            (SQLType.DECIMAL, 'DECIMAL'),
            (SQLType.DATE, 'DATE')]
        actions = [(KeyAction.CASCADE, 'CASCADE'),
            (KeyAction.SETNULL, 'SETNULL'),
            (KeyAction.RESTRICT, 'RESTRICT'),
            (KeyAction.NONE, 'NONE')]
        bools = [(True, 'True'),
            (False, 'False')]
            
        self._TypeToTextMap = dict((a,b) for (a,b) in types)
        self._TextToTypeMap = dict((b,a) for (a,b) in types)
        self._ActionToTextMap = dict((a,b) for (a,b) in actions)
        self._TextToActionMap = dict((b,a) for (a,b) in actions)
        self._BoolToTextMap = dict((a,b) for (a,b) in bools)
        self._TextToBoolMap = dcit((b,a) for (a,b) in bools)
        
        self.dtd = dtd
        self.extension = 'xml'
                 
    def load(self, file):
        with open(file, 'r') as f:
            xmlDatabase = etree.parse(f)
    
        return xmlDatabase
    def write(self, database, file=None):
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
                a['type'] = self._TypeToTextMap[column.datatype]
                if column.description is not None:
                    a['description'] = column.description
                if column.primaryKey is not None:	
                    a['primaryKey'] = self._BoolToTextMap[column.primaryKey] 
                if column.autoIncrement is not None:
                    a['autoIncrement'] = self._BoolToTextMap[column.autoIncrement]
                    
                ##required='',
                ##precision='',
                ##scale='',
                ##length='',
                ##default='',
                
            for index in table.getIndex():
                xmlIndex = etree.SubElement(xmlTable, 'index')
                a = xmlIndex.attrib
                a['name'] = index.getName()
                if index.description is not None:
                    a['description'] = index.description 
                for indexColumn in index.getColumn():
                    xmlIndexColumn = etree.SubElement(xmlIndex, 'column')
                    a = xmlIndexColumn.attrib
                    a['name'] = indexColumn.name
                    
            for foreignKey in table.getForeignKey():
                xmlForeignKey = etree.SubElement(xmlTable, 'foreignKey')
                a = xmlForeignKey.attrib
                a['name'] = foreignKey.getName()
                
                ##'foreignTable', )
                ##'onUpdate', )
                ##'onDelete', )
                for foreignKeyColumn in foreignKey.getColumn():
                    xmlForeignKeyColumn = etree.SubElement(foreignKey, 'column')
                    a = foreignKeyColumn.attrib
                    a['name'] = foreignKeyColumn.name

        # I can't believe we have to do this. Fragile. Insert the <!DOCTYPE>
        # when we write the XML to file.
        
        doctype = '\n<!DOCTYPE database SYSTEM "%s">' % dtd    
        xmlString = etree.tostring(xmlDatabase, encoding='utf-8', 
            pretty_print=True, xml_declaration=True)
        endCarrot = xmlString.find('>') + 1

        if file is None:
            file = database.name + '.' + self.extension 
        with open(file, 'w') as f:
            f.write(xmlString[:endCarrot])
            f.write(doctype)
            f.write(xmlString[endCarrot:])
        
    
class Pickle(object):
    def load(self, file):
        with open(file, 'r') as f:
            return pickle.load(f) 
    def write(self, obj, file=None):
        if file is None:
            file = obj.name + '.torque'
        with open(file, 'w') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)        

class LiteSQL(object):
    def write(self, database, file=None):
        pass
        

class SQLAlchemy(object):
    def write(self, database, file=None):
        pass
        
	