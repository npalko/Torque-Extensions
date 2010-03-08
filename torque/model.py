from __future__ import print_function

# Complete description of a relational database, expressed as a collection of
# objects.

"""

* unique constrants -> translated to an index
* autoincrement -> only specified as sequence behind the scense
* ordinal not writtent to xml file - assumed by position

        
Tables organized as a collection of 
    columns
    indexes
    foreign-key



Need to fix foreign key automatic name        

"""

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
        return self.name
    
class Index(object):
    def __init__(self, name=None, unique=True, ascendingOrder=True,
                 description=None):
        self.name = name
        self.unique = unique
        self.ascendingOrder = ascendingOrder
        self.column = []
        self.description = description
    def getAutomaticName(self):
        """return an auto-generated name for the index"""
        return self.name
    
class Column(object):
    def __init__(self, name=None, datatype=None, description=None, 
                 autoIncrement=False, primaryKey=False, unique=False, 
                 nullable=False, default=None, defaultIsNull=False,
                 length=None, precision=None, scale=None, parentTable=None):
        self.name = name
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
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
        self.column = []
        self.foreignKey = []
        self.index = []
    def appendColumn(self, column):
        """embed a reference to the parent table for each column appended"""
        column.parentTable = self
        self.column.append(column)
        
class Database(object):
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
        self.table = []
    def getTableDependencyIteration(self):
        """provide an iteration of tables such that the tables with foreign
        key dependencies are listed only after the tables the foreign key
        references"""
        
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

