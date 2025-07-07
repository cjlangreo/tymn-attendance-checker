# TYMN, A Facial Recognition Student Attendance Checker

## Introduction

Developed as a school project. Tymn uses a pre-trained AI to recognize students' faces recorded in a database to take their attendance if previous records are found, if not, uses their facial data to register them as a new student. Also has the ability to use your Android phone's camera for the facial recognition.

## Development

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

- This project was developed using
  [Python](https://www.python.org),
  [SQLite](https://www.sqlite.org/),
  [Pillow](https://pypi.org/project/pillow/),
  and [CustomTkinter](https://customtkinter.tomschimansky.com/).

- [Scrcpy](https://github.com/Genymobile/scrcpy) was also used to create a custom script that allows users to use their Android phone as a camera to use with the application.

## Face Recognition

TYMN uses [Adam Geitgey's face_recognition API](https://github.com/ageitgey/face_recognition) under the hood for its face recognition feature.
- Adding new student to the database
- Attendance check by facial recognition
<p>
  <img src="./thumbnails/sample.gif" alt="add-student.gif" style="width: 48%">
  <img src="./thumbnails/sample2.gif" alt="attendance-student.gif" style="width: 48%">
</p>

## User Interface

Interface developed with CustomTkinter library.

<p>
  <img src="./thumbnails/about-us.png" style="width: 48%">
  <img src="./thumbnails/add-student.png" style="width: 48%">
</p>
<p>
  <img src="./thumbnails/student-records.png" style="width: 48%">
  <img src="./thumbnails/attendance.png" style="width: 48%">
</p>
<p>
  <img src="./thumbnails/scan-1.png" style="width: 48%">
  <img src="./thumbnails/scan-2.png" style="width: 48%">
</p>