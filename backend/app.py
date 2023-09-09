from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    id = teacher_collection.insert_one(test_doc).inserted_id
    return "Test document inserted into MongoDB."




# REQUEST -> GET    /teacher/:id
# RESPONSE ->       list of all the courses associated with the teacher id



@app.route('/teacher/<teacher_id>', methods=['GET'])
def get_teacher_courses(teacher_id):

    try:
        # Find the teacher's courses by teacher_id
        teacher_courses = teacher_collection.find_one({"_id": ObjectId(teacher_id)})
        print(teacher_courses)

        # Convert the cursor to a list of dictionaries
        course_list = list(teacher_courses)
        print(course_list)

        return jsonify(course_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# GET request -> /teacher/:id/:course/:date
#           response -> list of key value pair of all the students of that course who were present/absent on the given date

@app.route('/teacher/<teacher_id>/<course>/<date>', methods=['GET'])
def get_teacher_course_attendance(teacher_id, course, date):
    ans = []
    try:
        # Find the teacher's courses by teacher_id
        teacher_courses = teacher_collection.find({"_id": ObjectId(teacher_id)}).next()['course_id']

        all_students = course_collection.find({ "_id": ObjectId(course) }).next()['student_ids']
        for student in all_students:
            attended = attendance_collection.find({ "student_id": ObjectId(student), "date": date, "course_id": ObjectId(course) })
            if not attended:
                ans.append([student, "Absent"])
            else:
                ans.append([student, "Present"])
        
        return jsonify(ans), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





# GET request-> /student/:id/:date
#           response-> list of key value pair of course scheduuled on that date and if he was present or absent

@app.route('/student/<student_id>/<date>', methods=['GET'])
def get_student_course_schedule_and_attendance(student_id, date):
    try:
        
        student = student_collection.find_one({"_id": ObjectId(student_id)})

        if not student:
            return jsonify({"error": "Student not found"}), 404

        # Find the courses associated with the student
        courses = list(course_collection.find())
        course_attendance = []
        for course in courses:
            if ObjectId(student_id) in course['student_ids']:
                course_attendance.append([course['_id'], 'Present'])
            else:
                course_attendance.append([course['_id'], 'Absent'])
        return jsonify(course_attendance), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/teacher/<course_id>/validate', methods=['GET'])
def get_validation_pictures(course_id):
    try:
        course_records = student_collection.find({"course_ids": ObjectId(course_id), "failsafe": {"$ne": None}})

        # Extract pictures from the records
        pictures = [record["photo"] for record in course_records]

        return jsonify(pictures), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()
