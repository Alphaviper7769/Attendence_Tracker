from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient("mongodb://localhost:27017/") 
db = client["Hack24"]  

teacher_collection = db["Teacher"]
student_collection = db["Student"]
course_collection = db["Course"]
attendance_collection = db["Attendance"]


@app.route('/test_db_connection')
def test_db():
    
    test_doc = {"message": "MongoDB connection successful!"}
    teacher_collection.insert_one(test_doc)
    return "Test document inserted into MongoDB."




# REQUEST -> GET    /teacher/:id
# RESPONSE ->       list of all the courses associated with the teacher id

@app.route('/teacher/<teacher_id>', methods=['GET'])
def get_teacher_courses(teacher_id):
    try:
        # Find the teacher's courses by teacher_id
        teacher_courses = teacher_collection.find({"_id": teacher_id})

        # Convert the cursor to a list of dictionaries
        course_list = list(teacher_courses)

        return jsonify(course_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# GET request -> /teacher/:id/:course/:date
#           response -> list of key value pair of all the students of that course who were present/absent on the given date

@app.route('/teacher/<teacher_id>/<course>/<date>', methods=['GET'])
def get_teacher_course_attendance(teacher_id, course, date):
    try:
        # Find the teacher's courses by teacher_id
        teacher_courses = teacher_collection.find({"_id": teacher_id})

        # Check if the requested course exists and is associated with the teacher
        requested_course = None
        for course_doc in teacher_courses:
            if course_doc.get("course_name") == course:
                requested_course = course_doc
                break

        if not requested_course:
            return jsonify({"error": "Course not found or not associated with the teacher"}), 404

        # Find students associated with the course
        course_id = requested_course["_id"]
        course_students = student_collection.find({"course_ids": course_id})

        # Find attendance records for the requested course and date
        attendance_records = attendance_collection.find({"course_id": course_id, "date": date})

        student_attendance = {}

        # Iterate through course students and populate the student_attendance dictionary
        for student in course_students:
            student_id = student["_id"]
            student_name = student["name"]
            attended = any(record["student_id"] == student_id and record["attended"] for record in attendance_records)
            student_attendance[student_name] = "attended" if attended else "absent"

        return jsonify(student_attendance), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





# GET request-> /student/:id/:date
#           response-> list of key value pair of course scheduuled on that date and if he was present or absent

@app.route('/student/<student_id>/<date>', methods=['GET'])
def get_student_course_schedule_and_attendance(student_id, date):
    try:
        
        student = student_collection.find_one({"_id": student_id})

        if not student:
            return jsonify({"error": "Student not found"}), 404

        # Find the courses associated with the student
        student_courses = course_collection.find({"student_ids": student_id})

        # Find attendance records for the student on the specified date
        attendance_records = attendance_collection.find({"student_id": student_id, "date": date})

        
        course_attendance = {}

        
        for course in student_courses:
            course_id = course["_id"]
            course_name = course["course_name"]
            attended = any(record["course_id"] == course_id and record["attended"] for record in attendance_records)
            course_attendance[course_name] = "attended" if attended else "absent"

        return jsonify(course_attendance), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run()
