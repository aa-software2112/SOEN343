# gdb stands for "global database"
from application import databaseObject as gdb

def exampleUserManipulatorFunction():
	print("User Manipulator")
	gdb.printPath()