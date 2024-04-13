# importing modules
import json
import csv
import datetime
import os
    
def write_attendance(unique_id, course, batch, student_count, attendance,data):
    if(attendance):
        print(f'{data["Name"]} Entered')
    data['sr'] = student_count
    data['Attendance_Time'] = f'{datetime.datetime.now().time().hour}:{datetime.datetime.now().time().minute}' if attendance else "NuLL"
    data['Attendance'] = "P" if attendance else "A"
    data['Course'] = course
    temp = []
    temp.append(data['sr'])
    temp.append(unique_id)
    temp.append(data['Name'])
    temp.append(data['Roll_No'])
    temp.append(data['DIV'])
    temp.append(data['Batch'])
    temp.append(data['Course'])
    temp.append(data['Department'])
    temp.append(data['Year'])
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