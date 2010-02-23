# Complete description of a relational database, expressed as a collection of
# objects.

"""
database = model.Database('Symbology')

currency = model.Table('Currency', column=[
    model.Column('Id', model.INT(), auto=True, unique=True)
    model.Column('Last.Effective.Date', model.DATE())
    ])


precision: number of digits in a number
scale: number of digits to the right of a decimal point

* how to deal with sequences?
* are unique columns another way of specifing an index?

"""

import pickle
from __future__ import print_function

class IndexOrder(object):
    ASC = 0
    DESC = 1
class Action(object):
    CASCADE = 0
    SETNULL = 1
    RESTRICT = 2
    NONE = 3


class DECIMAL(object):
    def __init__(self, precision=18, scale=6):
        self.precision = precision
        self.scale = scale
class NCHAR(object):
    def __init__(self, length=50):
        self.length = length
class NVARCHAR(object):
    def __init__(self, length=50):
        self.length = length
class INT(object):
    pass
class BIGINT(object):
    pass    
class DATE(object):
    pass

class ForeignKey(object):
    def __init__(self, name=None, reference=None, restrict=None, 
                 onUpdate=Action.RESTRICT, onDelete=Action.RESTRICT):
        self.name = name
        self.reference = reference
        self.restrict = restrict
        self.onUpdate = onUpdate
        self.onDelete = onDelete
class Index(object):
    def __init__(self, name=None, datatype=None):
        self.name = name
        self.datatype = datatype
        self.column = []
class Sequence(object):
    def __init__(self):
        pass
class Column(object):
    def __init__(self, name=None, datatype=None, auto=False, 
                 nullable=False, default=None, ordinal=None):
        self.name = name
        self.type = type
        self.autoincrement = autoincrement
        self.nullable = nullable
        self.default = default
        self.ordinal = None
class Table(object):
    def __init__(self, name=None):
        self.name = name
        self.column = dict()
        self.foreignKey = dict()
        self.index = dict()
    def getColumn(self):
        """provide an iteration of columns ordered by column.ordinal"""
        pass
class Database(object):
    def __init__(self, name=None):
        self.name = name
        self.table = dict()
    def getTable(self):
        """provide an iteration of tables such that the tables with foreign
        key dependencies are listed only after the tables the foreign key
        references"""
        pass
        
def writeToPickle(obj, file=None):
    if file is None:
        file = obj.name + '.torque'
    with open(file, 'w') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)        
def loadFromPickle(file):
    with open(file, 'r') as f:
        obj = pickle.load(f)
        return obj
    