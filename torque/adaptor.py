from __future__ import print_function

import pickle
import torque.model
import lxml.etree
import urllib

from torque.model import SQLType, KeyAction

    
class MySQLWorkbench(object):
    def __init__(self):
        """initialize bi-directional mapping"""
        
        types = [
            (SQLType.TINYINT, 'TINYINT'),
            (SQLType.SMALLINT, 'SMALLINT'),
            (SQLType.INT, 'INT'),
            (SQLType.BIGINT, 'BIGINT'),
            (SQLType.DECIMAL, 'DECIMAL'),
            (SQLType.BIT, 'BIT'),
            (SQLType.SINGLE, 'SINGLE'),
            (SQLType.DOUBLE, 'FLOAT'),
            (SQLType.TIME, 'TIME'),
            (SQLType.DATE, 'DATE'),
            (SQLType.TIMESTAMP, 'TIMESTAMP'),
            (SQLType.CHAR, 'CHAR'),
            (SQLType.VARCHAR, 'VARCHAR'),
            (SQLType.BINARY, 'BINARY')]
        actions = [
            (KeyAction.CASCADE, 'CASCADE'),
            (KeyAction.SETNULL, 'SET NULL'),
            (KeyAction.RESTRICT, 'RESTRICT'),
            (KeyAction.NONE, 'NO ACTION')]
        
        self._TextToTypeMap = dict((b,a) for (a,b) in types)
        self._ActionToTextMap = dict((a,b) for (a,b) in actions)
        self._TextToActionMap = dict((b,a) for (a,b) in actions)
        
    def getWorkingDir(self, grtRoot):
        """return the working directory of the model, so that we know where
        to save the additional generated files
        
        
        TODO: no idea where this is
        
        """
        pass
    def update(self):
        """
        
        This is tricky. There are API functions for add schema, add table, 
        remove/ change indexes.
        
        Investigate how to pull GUID's of each entity - will need to know 
        we're talking about the same column if it's renamed, etc.
        
        
        """
        pass
    def toModel(self, schemata):
        """return a model.Database representing the database design detailed
        in the MySQL Designer catalog.
        
        schemata = grt.root.wb.doc.physicalModels[0].catalog.schemata[0]"""
        
        dModel = torque.model.Database(name=schemata.name)
        
        # Tables, Columns, Indicies
        
        for t in schemata.tables:
            tModel = torque.model.Table(t.name)
            tModel.description = None if len(t.comment) == 0 else t.comment
            
            # assumes each table has a primary key, and the primary key is 
            # only one column
            
            primaryKeyName = t.primaryKey.columns[0].referencedColumn.name
            
            for c in t.columns:
                cModel = torque.model.Column(c.name)
                cModel.description = None if len(c.comment) == 0 else c.comment
                cModel.length = None if c.length == -1 else c.length
                cModel.scale = None if c.scale == -1 else c.scale
                cModel.precision = None if c.precision == -1 else c.precision
                cModel.nullable = not c.isNotNull
                cModel.autoIncrement = c.autoIncrement
                cModel.defaultIsNull = c.defaultValueIsNull
                cModel.default = None if len(c.defaultValue) == 0 else c.defaultValue
                cModel.primaryKey = (c.name == primaryKeyName)
                                
                datatype = c.formattedType.rsplit('(')[0]
                cModel.datatype = self._TextToTypeMap[datatype]
                                
                tModel.appendColumn(cModel)
                
            for i in t.indices:
                iModel = torque.model.Index(i.name)
                iModel.description = None if len(i.comment) == 0 else i.comment
                iModel.unique = i.unique
                
                for ic in i.columns:
                    modelColumn = [mc for mc in tModel.column
                        if mc.name == ic.referencedColumn.name][0]
                    iModel.column.append(modelColumn)
                    
                tModel.index.append(iModel)
                
            dModel.table.append(tModel)
        
        # Foreign Keys
            
        for t in schemata.tables:
            for k in t.foreignKeys:
                # assumes each foreign key definition only maps 1 column to
                # one column
                
                kModel = torque.model.ForeignKey(k.name)
                kModel.onUpdate = self._TextToActionMap[k.updateRule]
                kModel.onDelete = self._TextToActionMap[k.deleteRule]
                
                restrictedTable = [rt for rt in dModel.table
                    if rt.name == t.name][0]                
                restrictedColumn = [rc for rc in restrictedTable.column
                    if rc.name == k.columns[0].name][0]
                referencedTable = [rt for rt in dModel.table
                    if rt.name == k.referencedTable.name][0]                
                referencedColumn = [rc for rc in referencedTable.column
                    if rc.name == k.referencedColumns[0].name][0]

                kModel.restrictedColumn = restrictedColumn
                kModel.referencedColumn = referencedColumn   
                
                restrictedTable.foreignKey.append(kModel)
                
        return dModel

class XML(object):
    def __init__(self, dtd='http://github.com/npalko/Torque-Extensions' \
                 '/raw/master/torque-extensions.dtd'):
        """create bi-directional mapping between torque.model and text labels
        used in the XML file"""
            
        # TODO: is there a better way to create this bidirectional map?
            
        types = [
            (SQLType.TINYINT, 'TINYINT'),
            (SQLType.SMALLINT, 'SMALLINT'),
            (SQLType.INT, 'INT'),
            (SQLType.BIGINT, 'BIGINT'),
            (SQLType.DECIMAL, 'DECIMAL'),
            (SQLType.BIT, 'BIT'),
            (SQLType.SINGLE, 'SINGLE'),
            (SQLType.DOUBLE, 'DOUBLE'),
            (SQLType.TIME, 'TIME'),
            (SQLType.DATE, 'DATE'),
            (SQLType.TIMESTAMP, 'TIMESTAMP'),
            (SQLType.CHAR, 'CHAR'),
            (SQLType.VARCHAR, 'VARCHAR'),
            (SQLType.BINARY, 'BINARY')]
        actions = [
            (KeyAction.CASCADE, 'Cascade'),
            (KeyAction.SETNULL, 'SetNull'),
            (KeyAction.RESTRICT, 'Restrict'),
            (KeyAction.NONE, 'None')]
        bools = [
            (True, 'True'),
            (False, 'False')]
            
        self._TypeToTextMap = dict((a,b) for (a,b) in types)
        self._TextToTypeMap = dict((b,a) for (a,b) in types)
        self._ActionToTextMap = dict((a,b) for (a,b) in actions)
        self._TextToActionMap = dict((b,a) for (a,b) in actions)
        self._BoolToTextMap = dict((a,b) for (a,b) in bools)
        self._TextToBoolMap = dict((b,a) for (a,b) in bools)
        
        self.dtd = dtd
        self.extension = 'xml'
    def load(self, file, validate=True):
        """return a model.Database based on the provided XML file"""
        
        def generateTryAssign(xmlElement):
            attrib = xmlElement.attrib
            def tryAssign(key, default=None):
                try:
                    if default is not None:
                        if attrib[key] is None:
                            return default
                        else:
                            return self._TextToBoolMap[attrib[key]]
                    else:
                        return attrib[key]
                except KeyError:
                    return default
            return tryAssign
            
            
        with open(file, 'r') as f:
            tree = lxml.etree.parse(f)
        xmlDatabase = tree.getroot()    
            
        if validate:
            dtd = lxml.etree.DTD(urllib.urlopen(self.dtd))
            if not dtd.validate(xmlDatabase):
                raise ValueError, dtd.error_log.filter_from_errors()
            
        tryAssign = generateTryAssign(xmlDatabase)
        
        database = torque.model.Database()
        database.name = tryAssign('name')
        database.interfaceName = tryAssign('interfaceName')
        database.description = tryAssign('description')
        
        # Tables, Columns, Indicies
        
        for xmlTable in xmlDatabase.iterchildren('table'):
            tryAssign = generateTryAssign(xmlTable)
            
            table = torque.model.Table()
            database.table.append(table)
            table.name = tryAssign('name')
            table.interfaceName = tryAssign('interfaceName')
            table.description = tryAssign('description')
            
            for xmlColumn in xmlTable.iterchildren('column'):
                tryAssign = generateTryAssign(xmlColumn)
                
                column = torque.model.Column()
                table.appendColumn(column)
                column.name = tryAssign('name')
                column.interfaceName = tryAssign('interfaceName')
                column.description = tryAssign('description')
                column.default = tryAssign('default')
                column.length = tryAssign('length')
                column.precision = tryAssign('precision')
                column.scale = tryAssign('scale')
                column.autoIncrement = tryAssign('autoIncrement', False)
                column.primaryKey = tryAssign('primaryKey', False)
                column.unique = tryAssign('unique', False)
                column.nullable = tryAssign('nullable', False)
                column.defaultIsNull = tryAssign('defaultIsNull', False)
                datatype = tryAssign('type')
                column.datatype = self._TextToTypeMap[datatype]
                
            for xmlIndex in xmlTable.iterchildren('index'):
                tryAssign = generateTryAssign(xmlIndex)
                
                index = torque.model.Index()
                table.index.append(index)
                index.name = tryAssign('name')
                index.description = tryAssign('description')
                index.unique = tryAssign('unique', False)
                index.ascendingOrder = tryAssign('ascendingOrder', False)
                
                for xmlIndexColumn in xmlIndex.iterchildren('index-column'):
                    a = xmlIndexColumn.attrib
                    indexColumn = [c for c in table.column 
                        if c.name == a['name']][0]
                    index.column.append(indexColumn)
                    
        # Foreign Keys
        
        for xmlTable in xmlDatabase.iterchildren('table'):
            restrictedTable = [i for i in database.table 
                if i.name == xmlTable.attrib['name']][0]
            
            for xmlKey in xmlTable.iterchildren('foreign-key'):
                a = xmlKey.attrib
                
                referencedTable = [i for i in database.table
                    if i.name == a['referencedTable']][0]
                
                foreignKey = torque.model.ForeignKey()
                restrictedTable.foreignKey.append(foreignKey)
                foreignKey.name = a['name']
                foreignKey.onDelete = self._TextToActionMap[a['onDelete']]
                foreignKey.onUpdate = self._TextToActionMap[a['onUpdate']]
                
                foreignKey.restrictedColumn = [i for i in restrictedTable.column
                    if i.name == a['restrictedColumn']][0]
                foreignKey.referencedColumn = [i for i in referencedTable.column
                    if i.name == a['referencedColumn']][0]
                    
        return database
    def write(self, database, file=None, useAutoNames=True):
        """write model.database to a Torque Database Schema XML file"""
        
        xmlDatabase = etree.Element('database', name=database.name)
        
        for table in database.getTableDependencyIteration():
            xmlTable = etree.SubElement(xmlDatabase, 'table')
            a = xmlTable.attrib
            a['name'] = table.name
            if table.description is not None:
                a['description'] = table.description
                
            for column in table.column:
                xmlColumn = etree.SubElement(xmlTable, 'column')
                a = xmlColumn.attrib
                a['name'] = column.name
                a['type'] = self._TypeToTextMap[column.datatype]
                if column.description is not None:
                    a['description'] = column.description
                if column.default is not None:
                    a['default'] = str(column.default)
                if column.length is not None:
                    a['length'] = str(column.length)
                if column.precision is not None:
                    a['precision'] = str(column.precision)
                if column.scale is not None:
                    a['scale'] = str(column.scale)
                if column.primaryKey:	
                    a['primaryKey'] = self._BoolToTextMap[column.primaryKey] 
                if column.autoIncrement:
                    a['autoIncrement'] = self._BoolToTextMap[column.autoIncrement]
                if column.nullable:
                    a['nullable'] = self._BoolToTextMap[column.nullable]
                if column.defaultIsNull:
                    a['defaultIsNull'] = self._BoolToTextMap[column.defaultIsNull]

            for index in table.index:
                xmlIndex = etree.SubElement(xmlTable, 'index')
                a = xmlIndex.attrib
                if useAutoNames:
                    a['name'] = index.getAutomaticName()
                else:
                    a['name'] = index.name
                if index.description is not None:
                    a['description'] = index.description 
                a['unique'] = self._BoolToTextMap[index.unique]
                a['ascendingOrder'] = self._BoolToTextMap[index.ascendingOrder]
                
                for indexColumn in index.column:
                    xmlIndexColumn = etree.SubElement(xmlIndex, 'index-column')
                    a = xmlIndexColumn.attrib
                    a['name'] = indexColumn.name

            for foreignKey in table.foreignKey:
                xmlForeignKey = etree.SubElement(xmlTable, 'foreign-key')
                a = xmlForeignKey.attrib
                if useAutoNames:
                    a['name'] = foreignKey.getAutomaticName()
                else:
                    a['name'] = foreignKey.name
                a['restrictedColumn'] = foreignKey.restrictedColumn.name
                a['referencedTable'] = foreignKey.referencedColumn.parentTable.name
                a['referencedColumn'] = foreignKey.referencedColumn.name
                a['onUpdate'] = self._ActionToTextMap[foreignKey.onUpdate]
                a['onDelete'] = self._ActionToTextMap[foreignKey.onDelete]

        # I can't believe we have to do this. Fragile. (requires pretty_print
        # and xml_declaration). Insert the <!DOCTYPE> when we write the XML 
        # to file. Perhaps submit a patch to lxml?
        
        doctype = '\n<!DOCTYPE %s SYSTEM "%s">' % ('database', self.dtd)
        xmlString = etree.tostring(xmlDatabase, encoding='utf-8', 
            pretty_print=True, xml_declaration=True)
        endCarrot = xmlString.find('>') + 1

        if file is None:
            file = database.name + '.' + self.extension 
        with open(file, 'wb') as f:
            f.write(xmlString[:endCarrot])
            f.write(doctype)
            f.write(xmlString[endCarrot:])
        
    
class Pickle(object):
    def __init__(self):
        self.extension = 'torque'
    def load(self, file):
        with open(file, 'rb') as f:
            return pickle.load(f) 
    def write(self, obj, file=None):
        if file is None:
            file = obj.name + '.' + self.extension 
        with open(file, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)        

class LiteSQL(object):
    def write(self, database, file=None):
        pass
        

class SQLAlchemyORM(object):
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
        

        
