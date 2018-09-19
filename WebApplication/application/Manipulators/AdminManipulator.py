# gdb stands for "global database"
from application import databaseObject as gdb
from application.Manipulators import UserManipulator

def exampleAdminManipulatorFunction():
	print("Admin Manipulator")
	gdb.printPath()