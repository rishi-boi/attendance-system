import cv2
import os
import csv
from pymongo import MongoClient 
from pprint import pprint
import inquirer
import datetime
import pyqrcode 
import png 

def write_attendance(unique_id, course, batch, student_count, attendance,data):
    # Getting which student entered class
    if(attendance):
        print(f'{data["name"]} Entered')

    # Getting all information and storing it in structured format
    data['sr'] = student_count
    data['Attendance_Time'] = f'{datetime.datetime.now().time().hour}:{datetime.datetime.now().time().minute}' if attendance else "NuLL"
    data['Attendance'] = "P" if attendance else "A"
    data['Course'] = course
    temp = []
    temp.append(data['sr'])
    temp.append(unique_id)
    temp.append(data['name'])
    temp.append(data['roll_no'])
    temp.append(data['div'])
    temp.append(data['batch'])
    temp.append(data['Course'])
    temp.append(data['department'])
    temp.append(data['year'])
    temp.append(data['Attendance_Time'])
    temp.append(data['Attendance'])
    field = ['sr','id','Name','Roll_No','DIV','Batch','Course','Department','Year','Attendance_Time','Attendance']
    
    # Specify the path to your existing CSV file
    csv_file_path = f'attendance/{course}/{batch.upper()}.csv'

    # Check if the file exists and is not empty
    if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
        write_header = False
    else:
        write_header = True

    # Open the CSV file in append mode
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(field)
        writer.writerow(temp)

def createQRCode(data,name):
    # Generate QR code 
    url = pyqrcode.create(data) 
    # Create and save the png file naming "myqr.png" 
    checkDir("QRCodes")
    url.png(f'QRCodes/{name}.png', scale = 6) 

def selectOptions(name, message, choices, multiple=False):
    if(multiple):
        questions = [
            inquirer.Checkbox(
                name, message, choices
            ),
        ]
    else:
        questions = [
            inquirer.List(
                name, message, choices
            ),
        ]

    return inquirer.prompt(questions)

def initialize():
    # connecting to mongodb
    client = MongoClient("mongodb+srv://rishipardeshi567:666yyNb4CKoGVBd9@cluster0.alwtqt8.mongodb.net/?retryWrites=true&w=majority") 
    # selecting database
    mydatabase = client['attendance']
    # selecting collection
    mycollection = mydatabase['student_data']
    
    # commands for users
    answers = selectOptions('command', 'What youu want to do?', ["Get student information","Add new student", "Update student information", "Delete student information", "Start Attendance", "exit"])

    # Adding new student
    if(answers['command'] == "Add new student"):

        # asking for basic information
        email = input("Email No of student:")
        # checking if user already exists
        isAlready = mycollection.find_one({"email":email})
        if(isAlready):
            print("Student Already present with same email ID")
            print()
            initialize()
        name = input("Enter full name of student:")
        roll_no = input("Enter Roll No of student:")
        phone = input("Phone No of student:")
        department = input("Department No of student:")
        batch = input("batch No of student:") 
        div = input("Div of student:")
        year = input("year of student:")
        # generating unique ID based on their email
        unique_id = str(hash(email))[1:13]

        record = {
            'unique_id': unique_id,
            'name': name,
            'roll_no': roll_no,
            'phone': phone,
            'email': email,
            'department': department,
            'batch': batch,
            'div': div,
            'year':year
        }

        # Inserting given information into database
        rec = mycollection.insert_one(record)
        # Generating QR code of newly inserted student
        createQRCode(unique_id, f'{name}({roll_no})')
        print(f'{record["name"]} added to database')
        print()
        initialize()

    # Updating student information
    elif(answers['command'] == "Update student information"):
        # Asking for student unique ID
        unique_id = input("Enter unique id of student:")
        # asking for which information to update
        update = selectOptions('update', "What you like to update?",["Name", "Roll No","Phone Number", "Email","Department", "Batch", "Div", "Year"], multiple=True)
        # Looping and updating values
        for values in update['update']:
            update_value = input(f'Change your {values}:')
            mycollection.find_one_and_update({'unique_id':unique_id}, {"$set":{values.lower():update_value}}, upsert=False)
        print("Updated Succesfully!")
        print()
        initialize()

    # Getting specific student information
    elif(answers['command'] == "Get student information"):
        # Asking for unique student ID
        unique_id = input("Enter unique id of student:")
        # Getting all student information based on given unique ID
        data = mycollection.find_one({'unique_id':unique_id})
        # Showing student inforamtion in structured format
        for key, value in data.items():
            if(key == '_id'):
                continue
            print(f'{key}: {value}')
        print()
        initialize()

    # Deleting specific student information
    elif(answers['command'] == "Delete student information"):
        # Asking for unique student ID
        unique_id = input("Enter unique id of student:")
        # Finding and deleting student based in unique ID
        delete = mycollection.find_one_and_delete({"unique_id":unique_id})
        if(delete):
            print("Student information deleted from database successfully...")

    # Starting Attendance
    elif(answers['command'] == "Start Attendance"):
        start_attendance(mycollection)

    # Exiting program
    elif(answers['command'] == "exit"):
        exit()

# Check weather directory exits
def checkDir(directory):
    if(not os.path.isdir(directory)):
        os.mkdir(directory)

def start_attendance(mycollection):
    print("Preparing...")


    checkDir("attendance")

    # Capturing webcam
    cap = cv2.VideoCapture(0) # put 1 for external camera

    # Initializing QR code detector
    detector = cv2.QRCodeDetector()

    # Taking values from user
    course = input("Enter the name of subject:")
    batch = input("Enter batch:")

    checkDir(os.path.join('attendance',course))

    student_count = 1
    student_entered = []

    while True:
        # Reading images from webcam
        _, img = cap.read()

        # Getting data from QR code shown
        data, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image 
        if data:
            unique_id=data

            # Checking if student already marked their attendance
            if(unique_id not in student_entered):

                # storing student
                student_entered.append(unique_id)

                # Writing attendance in CSV file
                write_attendance(unique_id, course, batch, student_count,True,mycollection.find_one({'unique_id':unique_id}))
                student_count+=1

        cv2.imshow("QRCODEscanner", img)
        if cv2.waitKey(1) == ord("q"):
            # Getting all students from database and marking them Absent 
            students_absent = mycollection.find({"batch":batch.upper()})
            for student in students_absent:
                    if student['unique_id'] not in student_entered:
                        write_attendance(student['unique_id'], course, batch, student_count, False,student)
                        student_count+=1
            break

    cap.release() 
    cv2.destroyAllWindows()
    
    print("Attendance Created...")
    print()
    initialize()

initialize()