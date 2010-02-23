
class ForeignKey(object):
    def __init__(self, name=None, referencedColumn=None, restrictedColumn=None):
        self.name = name
        self.referencedColumn = referencedColumn
        self.restrictedColumn = restrictedColumn
    def __repr__(self):
        pass

class Index(object):
    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type
        self.column = []
    def __repr__(self):
        pass

class Column(object):
    def __init__(self, name=None, type=None, autoincrement=None, nullable=False, default=None):
        self.name = name
        self.type = type
        self.autoincrement = autoincrement
        self.nullable = nullable
        self.default = default
    def __repr__(self):
        pass

class Table(object):
    def __init__(self, name=None, column=None, foreignKey=None, index=None):
        self.name = name
		
		if column is None
			self.column = []
        self.column = column
        self.foreignKey = foreignKey
        self.index = index
    def __repr__(self):
        pass

class Database(object):
    def __init__(self, name=None):
        self.name = name
        self.table = []
    def __repr__(self):
        pass
	