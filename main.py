import cv2
from functions import *
import os
import json
from pymongo import MongoClient 
from pprint import pprint
import inquirer

import pyqrcode 
import png 

def createQRCode(data,name):
    # Generate QR code 
    url = pyqrcode.create(data) 
    # Create and save the png file naming "myqr.png" 
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
    # add new student
    # update student info
    # start attendance
    client = MongoClient("mongodb+srv://rishipardeshi567:666yyNb4CKoGVBd9@cluster0.alwtqt8.mongodb.net/?retryWrites=true&w=majority") 
    mydatabase = client['attendance']
    mycollection = mydatabase['student_data'] 
    student_data = {}
    for value in mycollection.find():
        temp = value
        student_data[value['unique_id']] = temp
    
    answers = selectOptions('command', 'What youu want to do?', ["Get student information","Add new student", "Update student information", "Delete student information", "Start Attendance", "exit"])

    if(answers['command'] == "Add new student"):

        email = input("Email No of student:")
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
        rec = mycollection.insert_one(record)
        createQRCode(unique_id, f'{name}({roll_no})')
        print(f'{record["name"]} added to database')
        print()
        initialize()

    elif(answers['command'] == "Update student information"):
        unique_id = input("Enter unique id of student:")
        update = selectOptions('update', "What you like to update?",["Name", "Roll No","Phone Number", "Email","Department", "Batch", "Div", "Year"], multiple=True)
        for values in update['update']:
            update_value = input(f'Change your {values}:')
            mycollection.find_one_and_update({'unique_id':unique_id}, {"$set":{values.lower():update_value}}, upsert=False)
        print("Updated Succesfully!")
        print()
        initialize()

    elif(answers['command'] == "Get student information"):
        unique_id = input("Enter unique id of student:")
        data = mycollection.find_one({'unique_id':unique_id})
        for key, value in data.items():
            if(key == '_id'):
                continue
            print(f'{key}: {value}')
        print()
        initialize()

    elif(answers['command'] == "Delete student information"):
        unique_id = input("Enter unique id of student:")
        delete = mycollection.find_one_and_delete({"unique_id":unique_id})
        if(delete):
            print("Student information deleted from database successfully...")

    elif(answers['command'] == "Start Attendance"):
        start_attendance(student_data)
    elif(answers['command'] == "exit"):
        exit()

def start_attendance(student_data):
    print("Preparing...")

    # Check weather directory exits
    def checkDir(directory):
        if(not os.path.isdir(directory)):
            os.mkdir(directory)

    checkDir("attendance")

    # Capturing webcam
    cap = cv2.VideoCapture(0)

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
                write_attendance(unique_id, course, batch, student_count,True)
                student_count+=1

        cv2.imshow("QRCODEscanner", img)
        if cv2.waitKey(1) == ord("q"):
            for uniId, record in student_data.items():
                if record['Batch'] == batch.upper() and uniId not in student_entered:
                    write_attendance(uniId, course, batch, student_count, False)
                    student_count+=1
            break

    cap.release() 
    cv2.destroyAllWindows()
    
    print("Attendance Created...")
    print()
    initialize()

initialize()