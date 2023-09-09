import pymongo
from pymongo import MongoClient

# Create a MongoDB client and connect to your MongoDB server
client = MongoClient("mongodb+srv://Alphaviper-7769:uDCmxnyyLkkPOCit@dev.nmr3n9v.mongodb.net/")  # Replace with your MongoDB connection URI

# Select the database you want to use
db = client["Hack24"]  # Replace with your database name

# Create the collections (if they don't already exist)
teacher_collection = db["Teacher"]
student_collection = db["Student"]
course_collection = db["Course"]
attendance_collection = db["Attendance"]

# Sample data for insertion (replace with your actual data)
sample_teacher = {
    "course_id": "course_id_1"
}

sample_student = {
    "name": "Student Name",
    "face": "Facial Recognition Data",
    "failsafe": "Failsafe Data"
}

sample_course = {
    "student_ids": []  # Add student ObjectId values here
}

sample_attendance = {
    "date": "2023-09-10",  # Date of attendance
    "course_id": "course_id_1",  # ObjectId of the course
    "student_id": "student_id_1",  # ObjectId of the student
    "attended": True
}

# Insert documents into their respective collections
teacher_id = teacher_collection.insert_one(sample_teacher).inserted_id
student_id = student_collection.insert_one(sample_student).inserted_id
course_id = course_collection.insert_one(sample_course).inserted_id
attendance_id = attendance_collection.insert_one(sample_attendance).inserted_id

# Print the inserted IDs
print(f"Teacher ID: {teacher_id}")
print(f"Student ID: {student_id}")
print(f"Course ID: {course_id}")
print(f"Attendance ID: {attendance_id}")

# Close the MongoDB client connection when done
client.close()
