from __future__ import print_function

# Complete description of a relational database, expressed as a collection of
# objects.

"""

* unique constrants -> translated to an index
* autoincrement -> only specified as sequence behind the scense
* ordinal not writtent to xml file - assumed by position


<table>
    col
    col
    <index unique="True">
        <index-column name=""/>
    </index>
    <foreign-key name="" table="" column="" localColumn="" onDelete="" onUpdate=""/>
</table>
        
        

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
        been explictly provided
        
        FK_[Source Table]_[Source Column]_[Restricted Table]_Restricted_Column
        
        
        """
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
    def __init__(self, name=None, datatype=None, comment=None, 
                 autoIncrement=False, primaryKey=False, unique=False, 
                 nullable=False, default=None, defaultIsNull=False):
        self.name = name
        self.datatype = datatype
        self.comment = comment
        self.autoIncrement = autoIncrement
        self.primaryKey = primaryKey
        self.unique = unique
        self.nullable = nullable
        self.default = default # None == no default specified
        self.defaultIsNull = defaultIsNull # true if default is NULL
    def getIndex(self):
        """If a column requires an index (in the case of a unique constraint or
        autoincrement, return an Index object here"""
        if (self.autoIncrement is not None) or self.unique or self.primaryKey:
            return Index(datatype='', column=self)
        
class Table(object):
    def __init__(self, name=None, comment=None):
        self.name = name
        self.comment = comment
        self.column = []
        self.foreignKey = []
        self.index = []
    def getColumn(self):
        """provide an iteration of columns ordered by column.ordinal"""
        return self.column.values()
class Database(object):
    def __init__(self, name=None):
        self.name = name
        self.table = []
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

