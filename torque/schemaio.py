from __future__ import print_function

import cPickle as pickle
import torque.model

from torque.model import SQLType, KeyAction

try:
    from lxml import etree
except ImportError:
    print('Couldn''t load lxml. XML IO not available')
    
try:
    import sqlalchemy
except ImportError:
    print('Couldn''t load sqlalchemy. SQLAlchemy ORM not available')
    

	
class MySQLAdaptor(object):
    def __init__(self):
        """ """

        self._TextToTypeMap = {'INT': SQLType.INT,
            }
        
        self._TypesWithLength = [SQLType.CHAR, SQLType.NCHAR, SQLType.NVARCHAR]
    def getWorkingDir(self, grtRoot):
        """return the working directory of the model, so that we know where
        to save the additional generated files"""
        pass
    def toModel(self, physicalModel):
        """Usage:

        physicalModel = grt.root.wb.doc.physicalModels[0]
        database = torque.mysqlwb.adaptor(physicalModel)
        """
        
        schemata = physicalModel.catalog.schemata[0]
        dModel = torque.model.Database(name=schemata.name)
        
        for t in schemata.tables:
            tModel = torque.model.Table(t.name, comment=t.comment)
            
            # TODO: only works for one column as primary key
            primaryKeyName = t.primaryKey.columns[0].referencedColumn.name
            
            for c in t.columns:
                cModel = torque.model.Column(c.name, comment=c.comment)
                
                cModel.autoIncrement = c.autoIncrement
                cModel.primaryKey = (c.name is primaryKeyName)
                cModel.default = c.defaultValue
                cModel.defaultIsNull = c.defaultValueIsNull
                cModel.nullable = not c.isNotNull
                cModel.datatype = self._TextToTypeMap[c.formattedType]
                
                if cModel.datatype in self._TypesWithLength:
                    cModel.length = c.length
                if cModel.datatype is SQLType.DECIMAL:
                    cModel.precision = c.precision
                    cModel.scale = c.scale
                
                tModel.column.append(cModel)
            
            for k in t.foreignKeys:
                kModel = torque.model.ForeignKey(k.name)
                
                k.referencedTable.name
                
                for kc in k.columns:
                    # create reference to column object already existing in
                    # the model data structure rather than creating new 
                    # objects
                    kc.name
                    
                tModel.foreignKey.append(kModel)
                    
            for i in t.indicies:
                iModel = torque.model.Index(i.name)
                
                tModel.index.append(iModel)
                
            
            dModel.table.append(tModel)
            
        return dModel

class XML(object):
    def __init__(self, dtd='http://github.com/npalko/Torque-Extensions' \
                 '/raw/master/torque-extensions.dtd'):
    
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
                if column.default is not None:
                    a['default'] = column.default
                if column.length is not None:
                    a['length'] = column.length
                if column.precision is not None:
                    a['precision'] = column.precision
                if column.scale is not None:
                    a['scale'] = column.scale
                if column.primaryKey:	
                    a['primaryKey'] = self._BoolToTextMap[column.primaryKey] 
                if column.autoIncrement:
                    a['autoIncrement'] = self._BoolToTextMap[column.autoIncrement]
                if column.requried:
                    a['required'] = self._BoolToTextMap[column.requried]
                if column.defaultIsNull:
                    a['defaultIsNull'] = self._BoolToTextMap[column.defaultIsNull]
                
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
        

class SQLAlchemyAdaptor(object):
    """
        lib/sqlalchemy/schema.py
        class MetaData(SchemaItem)
        
        line 1698
        
        use reflection interface MetaData.reflect() as a way of populating
        MetaData from torque.model
    
    """
    def __init__(self):
        pass
    def toMetaData(self, database):
        """return sqlalchemy.metadata for the given torque.model.Database"""
        pass
    def toModel(self, metaData):
        """return torque.model.Database for the given sqlalchemy.metadata"""
        pass
        

        
