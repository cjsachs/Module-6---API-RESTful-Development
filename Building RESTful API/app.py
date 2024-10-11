# 1. Create new Flask app with Data Validation using Flask-Marshmallow

# Why Data Validation is important?
# Ensure that the data submitted to the API adheres to predefined formats, preventing errors and ensuring consistency.

# What is Flask-Marshmallow? 
'''
    Marshmallow helps with object serialization/deserialization and data validation.
    Define a schema using Marshmallow to validate API requests.
'''
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)


#2. Defining and Using a Schema
 
# Student Schema: Ensures that only the specified fields (id, name, age) are included in the API's input/output and helps validate that incoming data matches this structure.
class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age')


# Create instance of schema
student_schema = StudentSchema()

# create dummy data of an array of dictionaries
students = [
    {
        'id': 1,
        'name': 'Amilcar',
        'age': 48
    },
    {
        'id': 2,
        'name': 'Rene',
        'age': 38
    }
]


# Create Route "get_students" & Test GET endpoint with Postman
@app.route('/get_students')
def get_students():
    return jsonify(students)

# Create Route "add_student" & Test POST endpoint with Postman
@app.route('/add_student', methods=['POST'])
def add_student():
    # gets our json data
    new_student = request.get_json()
    # validate json with schema
    errors = student_schema.validate(new_student)
    # create conditional based on if errors
    if (errors):
        return jsonify(errors), 404
    else:
        # add student to "students" list
        students.append(new_student)
        return jsonify(f'New Student: {new_student["name"]} was added to your database!'), 200

# create a dynamic route "get_student" to grab specific data
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    # loop through all students in "database"
    for student in students:
        # if the student id matches the end point
        if (student['id'] == student_id):
            # return the jsonified student object
            return jsonify(student), 200      
    # if no match, return a jsonfied response of no student found
    return jsonify({'messgage': 'Student not found.'})

# create a dynamic route "update_student"
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    # get updated json data
    updated_student = request.get_json()
    # loop through all students in "database"
    for student in students:
        # if the student id matches the end point
        if (student['id'] == student_id):
            # use the update method to update information
            student.update(updated_student)
            # return the jsonified student object
            return jsonify(student), 200
    # if no match, return a jsonfied response of no student found
    return jsonify({'message': 'Student not found!'})

# create dynamic route "delete_student"
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    # loop through all students in "database"
    for student in students:
        # if the student id matches the end point
        if (student['id'] == student_id):
            # delete student from students
            students.remove(student)
            # return the jsonified student object
            return jsonify({
                'message': 'Student Deleted!',
                'current_students': students
            }), 200
    # if no match, return a jsonfied response of no student found
    return jsonify({'message': 'Student not found!'})