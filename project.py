import time
import getpass
from tqdm.auto import tqdm
import sqlite3
import pyzbar.pyzbar as pyzbar
import pyqrcode
import cv2
import png
import os
import numpy
import colorama
from datetime import datetime
from colorama import Back, Style
colorama.init(autoreset=True)


#------ScanningFromWebCamera---------------------
def scan():
	i = 0
	cap = cv2.VideoCapture(0)
	font = cv2.FONT_HERSHEY_PLAIN
	while i<1:
		ret,frame=cap.read()
		decode = pyzbar.decode(frame)
		for obj in decode:
			name=obj.data
			name2= name.decode()
			nn,ii,pp,dd = name2.split(' ')
			now = datetime.now()
			
			db = sqlite3.connect('EmployeeDatabase.db')
			c = db.cursor()
			c.execute(''' Select * from Record where iid=? or TimeofMArk=? ''',(ii,dd)) 
			result=c.fetchone()
			if(result):
				print(Back.MAGENTA+"Attendence is already submitted ") 
				db.commit()
			else:

				c.execute('''CREATE TABLE IF NOT EXISTS Record(name TEXT, iid TEXT,phone_no TEXT, dept TEXT, TimeofMArk TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL )''')
				c.execute("INSERT INTO Record(name, iid, phone_no, dept,TimeofMark) VALUES (?,?,?,?,?)", (nn,ii,pp,dd,now))
				db.commit()
			

#database portions-----------------------------
			i=i+1
		cv2.imshow("QRCode",frame)
		cv2.waitKey(2)
		cv2.destroyAllWindows

#------CreateDatabaseForeEmployee------------------
def database():
	conn = sqlite3.connect('EmployeeDatabase.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS all_record(employee_name TEXT, employee_id TEXT, employee_contact, employee_department TEXT)")
	conn.commit()
	conn.close()
database()

#------AddingNewUsers/Employee---------------------
def add_User():
	Li = []
	E_name=str(input("Please Enter Employee Name\n"))
	E_id=str(input("Please Enter Employee Id\n"))
	E_contac= input("Please enter Employee Contact No\n")
	E_dept= input("Please enter Employee Department\n")
	Li.extend((E_name,E_id,E_contac,E_dept))
#-----using List Compression to convert a list to str--------------
	listToStr = ' '.join([str(elem) for elem in Li])
	#print(listToStr)
	print(Back.MAGENTA + "Please Verify the Information")
	print("Employee Name       = "+ E_name)
	print("Employee ID         = "+ E_id)
	print("Employee Contact    = "+ E_contac)
	print("Employee Department = "+ E_dept)
	input("Press Enter to continue or ### ENTER ### to Break Operation")
	conn = sqlite3.connect('EmployeeDatabase.db')
	c = conn.cursor()
	c.execute("INSERT INTO all_record(employee_name, employee_id, employee_contact, employee_department) VALUES (?,?,?,?)", (E_name,E_id,E_contac,E_dept))
	conn.commit()
	conn.close()
	qr= pyqrcode.create(listToStr)
	if not os.path.exists('./QrCodes'):
		os.makedirs('./QRCodes')
	qr.png("./QRCodes/" +E_name+ ".png",scale=8)
#--------------ViewDatabase------------------------

def viewdata():
	conn = sqlite3.connect('EmployeeDatabase.db')
	c = conn.cursor()
	c.execute("SELECT * FROM Record")
	rows = c.fetchall()
	for row in rows:
		print(row)
	conn.close()

#----------------Salary Giving Work ------------------

def countSalaries():
	conn=sqlite3.connect('EmployeeDatabase.db')
	inputName=input()
	daysalary=500
	c=conn.cursor()
	# c.execute("Select * from Record where name='inputName'")
	c.execute("Select * from Record where name=?",(inputName,))
	rows=c.fetchall()
	print("No of days he comes in "+str(len(rows)))
	tsalary=len(rows)*daysalary
	print("Salary "+str(tsalary))

	
	conn.close()



#------------------Deleting a Record-------------------------------------
#----it will delete a record from the attendence taken section------------


def deleteRecord():	

	conn = sqlite3.connect('EmployeeDatabase.db')
	c = conn.cursor()
	d = str(input('Please enter name: '))
	mydata = c.execute('DELETE FROM Record WHERE Name=?', (d,))
	conn.commit()
	print("Record deleted sucessfully!")
	c.close()





#---------------Display all Records which are present in the database ------------------------

#-------------which we have added till in our database-------------

def displayAllDetails():
    conn = sqlite3.connect('EmployeeDatabase.db')
    print("Opened database successfully")

    cursor = conn.execute("SELECT * FROM all_record")
    data = cursor.fetchall()

    for lst in data:
        print(lst)

    print()
    conn.close()

#------------------update date in the database-------------
#####-----------update data------------------------
# update the record form the database form the total records in the database and display the records of the whose attendence is taken  
def updateRecord():
    conn = sqlite3.connect('EmployeeDatabase.db')
    print("Opened database successfully")
    nId = int(input("id: "))

    colN = int(input("1)name\n2)department \nwhich value you want to update: "))
    if colN == 1:
        column = "employee_name"
        value = input("enter the name you want to update: ")
        value = "\'" + value + "\'"
    elif colN == 2:
        column = "employee_department"
        value = input("enter the department you want to update: ")
        value = "\'" + value + "\'"
   
    else:
        print("Enter valid number")
        return

    conn.execute("UPDATE all_record set {} = {} where employee_id = {}".format(column, value, nId))
    conn.commit()
    print("Total number of rows updated :", conn.total_changes, "\n")

    conn.close()

    viewdata()


# ******************display some records by our choice************

#---------------show specific records-------------

def displaySpecificRecord():
    conn = sqlite3.connect('EmployeeDatabase.db')
    print("Opened database successfully")

    colN = int(input("1)iid\n2)name\n3)department\nwhich value you want to sort by: "))
    if colN == 1:
        column = "employee_id"
        value = int(input("enter id: "))
        condition = "{} = {}".format(column, value)
    elif colN == 2:
        column = "employee_name"
        value = input("enter the name: ")
        value = "\'" + value + "\'"
        condition = "{} = {}".format(column, value)
    elif colN == 3:
        column = "employee_department"
        value = input("enter the department: ")
        value = "\'" + value + "\'"
        condition = "{} = {}".format(column, value)
    
    
    else:
        print("Enter valid number")
        return

    cursor = conn.execute(("SELECT * FROM all_record where " + condition))
    data = cursor.fetchall()

    for lst in data:
        print(lst)

    print()
    conn.close()



#--------------own Query-----------------
# select name from Record 

def writeQuery():
    conn = sqlite3.connect('EmployeeDatabase.db')
    print("Opened database successfully")
    query = input("Enter your Query: ")

    cursor = conn.execute(query)

    words = query.split()
    if words.pop(0).lower() == "select":
        data = cursor.fetchall()
        for lst in data:
            print(lst)
        return
    else:
        conn.commit()
        print("Total number of rows updated :", conn.total_changes, "\n")
        print()
        conn.close()
        return



#----------AdminScreen-----------------------
def afterlogin():
	print( "           \n \n")


	print("+------------------------------------+")
	print(Back.MAGENTA+"                Menu Bar             ")
	print("|          1- Add New Employee       |")
	print("|          2- View Records           |")
	print("|          3- Salary                 |")
	print("|          4- Delete Records         |")
	print("|          5- Update Records         |")
	print("|          6-displayAllDetails       |")
	print("|          7- displaySpecificRecord  |")
	print("|          8--Write our own query    |")
	print("|          9- Exit                   |")
	print("+------------------------------------+")
	user_input = input("")
	if user_input == '1':
		add_User()
	if user_input == '2':
		viewdata()
	if user_input == '3':
		countSalaries()
	if user_input == '4':
		deleteRecord()
	if user_input == '5':
		updateRecord()
	if user_input == '6':
		displayAllDetails()
	if user_input == '7':
		displaySpecificRecord()
	if user_input == '8':
		writeQuery()
	if user_input == '9':

		bol = False

	print("\n\n ___________ Thank You ___________\n\n\n")


#Login--------------------------------------
def login():
	print(Back.CYAN+ 'Please Enter Password :')
	print(Back.MAGENTA+"QR Code Attendace System")
	password = getpass.getpass()
	if password =='aka':
		for i in tqdm(range(4000)):
			print("",end='\r')
		print("------------------------------------------------------------------------------------------------------------------------")
		print(Back.BLUE+"QR Code Attendace System")
		afterlogin()
	if password != 'aka':
		print("Invalid Password")
		login()



#-------MainPage----------------------------
def Intro():
	print("\n\n\n\n\n")
	print("\t\t\t===================================================")
	print("\t\t\t===================================================")
	print(Back.RED+"\t\t\t\t Employee Attendence Management System ")
	# cout << "\n\n\n\t\t\t\t\tVersion : 1.1"
	print("\t\t\t===================================================")
	print("\t\t\t===================================================")
	print("\n\n\n\n\n")
	os.system("pause")

def Student():
	print("\n\n\n\n\n")
	print("\t\t\t===================================================")
	print("\t\t\t===================================================")
	# print("\n\n\t\t\t\t Student Details")
	print("\t\t\t\t\t Student Details ")
	print("\t\t\t===================================================")
	print("\t\t\t===================================================")
	# print(Back.RED+"\n\n\t\t\t\t Student Details")
	print("\n\t\t\t\t  Name : Vishal Singh ")
	print("\n\t\t\t \t Class : SY-IT-A ")
	print("\n\t\t\t \t Roll no : 65 ")
	print("\n\t\t\t \t Subject : SPD Project ")
	print("\n\t\t\t \t Email: vishal.singh20@vit.edu ")
	print("\n\t\t\t \t Prn no: 12010382")
	# cout << "\n\n\n\t\t\t\t\tVersion : 1.1"
	print("\t\t\t===================================================")
	print("\t\t\t===================================================")
	print("\n\n\n\n\n")
	os.system("pause")
def Guide():
	print("\n\n\n\n\n")
	print("\t\t\t===================================================")
	print("\t\t\t===================================================")
	print("\n\n\t\t\t\t  Teacher : Prof.Ranjana Yadhav ")
	print("\n\n\t\t\t \t Institute : Vishwakarma University ")
	# cout << "\n\n\n\t\t\t\t\tVersion : 1.1"
	print("\n\t\t\t===================================================")
	print("\n\t\t\t===================================================")
	print("\n\n\n\n\n")
	os.system("pause")
	

# Intro()
# Student()
# Guide()


def markattendance():
	print("+------------------------------+")
	print("|  1- Mark Attendance          |")
	print("|  2- Admin Login              |")
	print("+------------------------------+")
	user_input2 = input("")
	if user_input2== '1':
		scan()
	if user_input2 == '2':
		login()

markattendance()

