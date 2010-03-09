from __future__ import print_function

import hashlib

# Complete description of a relational database, expressed as a collection of
# objects.



class KeyAction(object):
    CASCADE = 0
    SETNULL = 1
    RESTRICT = 2
    NONE = 3
    
class SQLType(object):
    TINYINT = 0       # 0 to 255
    SMALLINT = 1      # -2^15 to 2^15-1 
    INT = 2           # -2^31 to 2^31-1 
    BIGINT = 3        # -2^63 to 2^63-1 
    DECIMAL = 4       # we don't use NUMERIC
    BIT = 5           # 0,1,NULL
    SINGLE = 6        # REAL, FLOAT(1-24)
    DOUBLE = 7        # 
    TIME = 8
    DATE = 9
    TIMESTAMP = 10
    CHAR = 11
    VARCHAR = 12
    BINARY = 13
    
class ForeignKey(object):
    def __init__(self, name=None, referencedColumn=None, 
                 restrictedColumn=None, onUpdate=KeyAction.RESTRICT, 
                 onDelete=KeyAction.RESTRICT):	
        """RestrictedColumn is the column that has its allowed values 
        restricted by the foreign key contstraint; the ReferencedColumn is
        the column providing the constraint"""
        
        self.name = name
        self.referencedColumn = referencedColumn
        self.restrictedColumn = restrictedColumn
        self.onUpdate = onUpdate
        self.onDelete = onDelete
    def getAutomaticName(self):
        """return an auto-generated name for the constraint"""
        return 'FK_(%s)%s_(%s)%s' % (self.restrictedColumn.parentTable.name,
            self.restrictedColumn.name,
            self.referencedColumn.parentTable.name,
            self.referencedColumn.name)

class Index(object):
    def __init__(self, name=None, unique=True, ascendingOrder=True,
                 description=None):
        self.name = name
        self.unique = unique
        self.ascendingOrder = ascendingOrder
        self.description = description
        self.column = []
    def isPrimary(self):
        """return true if it this is the primary key index"""
        return (len(self.column) == 1) and (self.column[0].primaryKey)
    def getAutomaticName(self):
        """return an auto-generated name for the index"""
        if self.isPrimary():
            name = '(%s)' % self.column[0].parentTable.name
        else:
            m = hashlib.sha1()
            m.update(str(self.unique))
            m.update(str(self.ascendingOrder))
            m.update(str(self.description))
            for c in self.column:
                m.update(c.parentTable.name + c.name)
            name = m.hexdigest()[:16]
        return 'IDX_%s' % name
        
class Column(object):
    def __init__(self, name=None, interfaceName=None, datatype=None, 
                 description=None, autoIncrement=False, primaryKey=False, 
                 unique=False, nullable=False, default=None, 
                 defaultIsNull=False, length=None, precision=None, 
                 scale=None, parentTable=None):
        self.name = name
        self.interfaceName = interfaceName
        self.datatype = datatype
        self.description = description
        self.autoIncrement = autoIncrement
        self.primaryKey = primaryKey
        self.unique = unique
        self.nullable = nullable
        self.default = default # None == no default specified
        self.defaultIsNull = defaultIsNull # true if default is NULL
        self.length = length
        self.precision = precision
        self.scale = scale
        self.parentTable = parentTable
        
class Table(object):
    def __init__(self, name=None, interfaceName=None, description=None):
        self.name = name
        self.interfaceName = interfaceName
        self.description = description
        self.column = []
        self.foreignKey = []
        self.index = []
    def appendColumn(self, column):
        """embed a reference to the parent table for each column appended"""
        column.parentTable = self
        self.column.append(column)
        
class Database(object):
    def __init__(self, name=None, interfaceName=None, description=None):
        self.name = name
        self.interfaceName = interfaceName
        self.description = description
        self.table = []
    def getTableDependencyIteration(self):
        """provide an iteration of tables such that the tables with foreign
        key dependencies are listed only after the tables the foreign key
        references"""
        
        """
        for (i,table) in self.table:
            
            for fk in table.foreignKey:
                parentTable = fk.referencedColumn.parentTable
                
                if parentTable not in self.table[:i]:
                    # problem: dependent not listed before
                    
                    
                
        """
            
            
        
        # sort [] by @name
        # for t in table
        #   for t in table.foreignKey.referencedColumn.parentTable
        
        
        return (t for t in self.table)
        
        
def test():
    
    database = Database('Symbology')
    
    currency = Table('Currency')
    id = Column('Id', SQLType.INT, autoIncrement=True, primaryKey=True)
    lastDate = Column('Last.Effective.Date', SQLType.DATE)

    currency.appendColumn(id)
    currency.appendColumn(lastDate)
    database.table.append(currency)
    
    
    return database

