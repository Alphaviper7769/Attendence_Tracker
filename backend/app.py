from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://Alphaviper-7769:uDCmxnyyLkkPOCit@dev.nmr3n9v.mongodb.net") 
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
        
        
        courses= teacher_courses['course_id']
        print(courses)
        courses_final = []
        for course in courses:
            print(course) 
            course_name=course_collection.find_one({"_id":ObjectId(course)})['name']
            print(course_name)
            courses_final.append(course_name)



        # Convert the cursor to a list of dictionaries

        return jsonify({"data": courses_final}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# GET request -> /teacher/:id/:course/:date
#           response -> list of key value pair of all the students of that course who were present/absent on the given date

@app.route('/teacher/<teacher_id>/<course>/<date>', methods=['GET'])
def get_teacher_course_attendance(teacher_id, course, date):
    ans = []
    print(1)
    try:
        # Find the teacher's courses by teacher_id
        teacher_courses = teacher_collection.find({"_id": ObjectId(teacher_id)}).next()['course_id']
        print(2)
        print(teacher_courses)

        all_students = course_collection.find({ "_id": ObjectId(course) }).next()['student_ids']
        print(all_students)
        print(3)
        for student in all_students:
            attended = attendance_collection.find({ "student_id": ObjectId(student), "date": date, "course_id": ObjectId(course) })
            print(4)
            print(attended)
            if not attended:
                ans.append([student, "Absent"])
            else:
                ans.append([student, "Present"])
        print(ans)
        
        ans = json.loads(json_util.dumps(ans))
        
        return jsonify({"data": ans}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





# GET request-> /student/:id/:date
#           response-> list of key value pair of course scheduuled on that date and if he was present or absent

@app.route('/student/<student_id>/<date>', methods=['GET'])
def get_student_course_schedule_and_attendance(student_id, date):
    print(1)
    try:
        
        student = student_collection.find_one({"_id": ObjectId(student_id)})
        print(2)

        if not student:
            return jsonify({"error": "Student not found"}), 404

        # Find the courses associated with the student
        courses = list(course_collection.find())
        print(3)
        course_attendance = []
        for course in courses:
            if ObjectId(student_id) in course['student_ids']:
                course_attendance.append([course['_id'], 'Present'])
            else:
                course_attendance.append([course['_id'], 'Absent'])
        print(4)
        print(course_attendance)
        course_attendance = json.loads(json_util.dumps(course_attendance))
        return jsonify({"data": course_attendance}), 200
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
    




@app.route('/teacher/<course_id>/validate', methods=['POST'])
def validate_and_update_student_info(course_id):
    try:
        
        student_id = request.form.get('student_id')
        student_name = request.form.get('student_name')
        failsafe_id = request.form.get('failsafe_id')

        # Check if the student ID exists
        existing_student = student_collection.find_one({"_id": ObjectId(student_id)})

        if existing_student:
            print("Student Exist")
            failsafe_data = student_collection.find_one({"_id": ObjectId(failsafe_id)})
            
            if failsafe_data and "date" in failsafe_data:
                date = failsafe_data["date"]

                attendance_collection.update_one(
                    {"student_id": ObjectId(student_id)},
                    {"$push": {"dates": date}}
                )

                student_collection.delete_one(
                    {"_id":ObjectId(failsafe_id)}
                )

                return jsonify({"message":"Attendence Updated"}),200
            else:
                return jsonify({"error":"failsafe data missing"}),402

        else:
            print("Student doesnt exist")
            failsafe_data = student_collection.find_one({"_id": ObjectId(failsafe_id)})
            if failsafe_data and "face" in failsafe_data:
                face = failsafe_data["face"]
                new_student={
                    '_id':ObjectId(student_id),
                    'face':face,
                }
                student_collection.insert_one(new_student)

                course_collection.update_one
                (
                    {'_id':ObjectId(course_id)},
                    {"$push": {"student_id":ObjectId(student_id)}}
                )
                return jsonify({"message":"New User Added"}),200
            else:
                return jsonify({"error":"failsafe data missing"}),402



    except Exception as e:
        return jsonify({"error":str(e)}),500



if __name__ == '__main__':
    app.run()
