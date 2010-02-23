
"""
MySQL Workbench -> Internal Structure
    Internal Structure -> SQLAlchemy
    Internal Structure -> SQLLite
    Internal Structure <-> pickle
    Internal Sturcutre <-> Torque XML file

"""

		
	
def loadFromXML(file):
	pass
def writeToXML(database, file=None):
	pass	
	
def loadFromPickle(file):
	pass
def writeToPickle(database, file=None):
	pass
	
def writeToSQLLite(database, file=None):
	pass
def writeToSQLAlchemy(database, file=None);
	pass
	

	
"""
Designer data structure -> Torque XML

Torque XML -> SQLAlchemy
Torque XML -> SQLLite class



def importMySQLStudio(grt):


import xml.dom.minidom
import xml.etree.ElementTree


doc = xml.dom.minidom.Document()

database = doc.createElement('database')
database.setAttribute('name', '')
doc.appendChild(database)

table = doc.createElement('table')
table.setAttribute('name', 'security')
database.appendChild(table)



doc.print

"""