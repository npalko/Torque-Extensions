from __future__ import print_function

# Complete description of a relational database, expressed as a collection of
# objects.

"""



* how to deal with sequences?
* are unique columns another way of specifing an index?
* should we use lists instead of a dict()?
"""


class IndexOrder(object):
    ASC = 0
    DESC = 1
class KeyAction(object):
    CASCADE = 0
    SETNULL = 1
    RESTRICT = 2
    NONE = 3
class SQLType(object):
    DECIMAL = 0	# don't support NUMERIC, it's redundant
    CHAR = 1
    VARCHAR = 2
    NCHAR = 3
    NVARCHAR = 4
    INT = 5
    BIGINT = 6
    DATE = 7
    DATETIME = 8
    TIMESTAMP = 9
    BIT = 10

class ForeignKey(object):
    def __init__(self, name=None, reference=None, restrict=None, 
                 onUpdate=KeyAction.RESTRICT, onDelete=KeyAction.RESTRICT):	
        self.name = name
        self.reference = reference
        self.restrict = restrict
        self.onUpdate = onUpdate
        self.onDelete = onDelete
    def getName(self):
        """return an auto-generated name for the constraint if one hasn't 
        been explictly provided"""
        pass
class Index(object):
    def __init__(self, name=None, datatype=None):
        self.name = name
        self.datatype = datatype
        self.column = []
    def getName(self):
        """return an auto-generated name for the index if one hasn't been
        explicitly provided"""
        pass
class Column(object):
    def __init__(self, name=None, datatype=None, description=None, 
                 autoIncrement=False, primaryKey=False, unique=False, 
                 nullable=False, default=None, ordinal=None):
        self.name = name
        self.datatype = datatype
        self.description = description
        self.autoIncrement = autoIncrement
        self.primaryKey = primaryKey
        self.unique = unique
        self.nullable = nullable
        self.default = default
        self.ordinal = ordinal
class Table(object):
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
        self.column = dict()
        self.foreignKey = dict()
        self.index = dict()
    def getColumn(self):
        """provide an iteration of columns ordered by column.ordinal"""
        return self.column.values()
class Database(object):
    def __init__(self, name=None):
        self.name = name
        self.table = dict()
    def getTable(self):
        """provide an iteration of tables such that the tables with foreign
        key dependencies are listed only after the tables the foreign key
        references"""
        return self.table.values()
        
        
def test():
    
    database = Database('Symbology')
    currency = Table('Currency')
    id = Column('Id', SQLType.INT, autoIncrement=True, unique=True)
    lastDate = Column('Last.Effective.Date', SQLType.DATE)


    database.table[currency.name] = currency
    currency.column[id.name] = id
    currency.column[lastDate.name] = lastDate
    
    return database

