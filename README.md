# Student Management System with Attendance Tracking

## Overview

This project aims to create a comprehensive Student Management System with an integrated attendance tracking feature. Developed using Python programming language and MongoDB database, the system facilitates the management of student records, including adding, updating, and deleting student data. Additionally, it provides functionality for tracking student attendance through QR code scanning, with attendance records being exported to a CSV file for easy monitoring and analysis.

## Features

- **Student Data Management**: The system allows users to add, update, and delete student records. Each record typically includes information such as student name, ID, contact details, and other relevant data.

- **Attendance Tracking**: Utilizing QR codes, the system enables efficient tracking of student attendance during classes or events. By scanning the QR code associated with each student, their attendance status is recorded in real-time.

- **CSV Export**: Attendance data is exported to a CSV (Comma-Separated Values) file, providing a structured format for further analysis or integration with other tools. This feature enhances accessibility and simplifies the process of generating attendance reports.

## Technologies Used

- **Python**: The primary programming language used for developing the project logic and functionality. Python offers versatility and ease of integration with various libraries and frameworks.

- **MongoDB**: A NoSQL database used to store and manage student data efficiently. MongoDB's flexible document-based model is well-suited for handling diverse types of data associated with student records.

- **QR Code Generation and Scanning**: Python libraries such as `qrcode` and `opencv-python` are utilized for generating QR codes and scanning them respectively. QR codes serve as unique identifiers for students and are crucial for recording attendance.

- **CSV File Handling**: Python's built-in `csv` module is employed for handling CSV file operations, including writing attendance records in a structured format.

## Usage Instructions

1. **Installation**: Download or clone the project repository from GitHub.
2. **Dependencies Installation**: Ensure Python is installed on your system. Install required Python packages using `pip install -r requirements.txt`.
3. **Database Configuration**: Configure MongoDB connection settings in the project configuration file (`config.py`).
4. **Running the Application**: Execute the compiled `.exe` file to launch the Student Management System.
5. **Adding Student Data**: Use the provided interface to add student records, including necessary information such as name, ID, etc.
6. **Attendance Tracking**: Scan the QR codes provided to students during classes or events using the integrated scanner feature.
7. **Exporting Attendance**: Access the exported CSV file containing attendance records for further analysis or reporting.

## Contributing

Contributions to the project are welcome! If you encounter any issues or have suggestions for improvements, please submit them via GitHub issues or consider creating a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
-----
Feel free to customize and expand upon this template to provide more specific details about your project as needed.
