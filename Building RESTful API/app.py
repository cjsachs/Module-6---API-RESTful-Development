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
# Part 3: from db_connection import db_connection
from db_connection import db_connection
# Part 3: from marshmallow import fields, ValidationError
from marshmallow import fields, ValidationError

app = Flask(__name__)
ma = Marshmallow(app)

# Part 3: Modify our current Schema to match our MySQL database

# Student Schema: Ensures that only the specified fields ('id', 'first_name', 'last_name', 'email', 'phone_num', 'start_date') are included in the API's input/output and helps validate that incoming data matches this structure.
class StudentSchema(ma.Schema):
    # Part 3: Create all field definitions for Student
    id = fields.Int(dump_only=True) # dump_only means we dont input data for this field
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    phone_num = fields.String(required=True)
    start_date = fields.Date()
    
    class Meta:
        # update fields to match database fields
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_num', 'start_date')

# Create instance of schema
student_schema = StudentSchema()
# Part 3: Create instance to handle multiple records
students_schema = StudentSchema(many=True)

# Part 3: modify and comment out dummy data
# students = [
#     {
#         'id': 1,
#         'first_name': 'Amilcar',
#         'last_name': 'Cornier',
#         'email': 'acornier@ct.com',
#         'phone_num': '111-111-1111',
#         'start_date': '2024-05-01'
#     }
# ]

# Part 3: Modify all routes to include database

# Create Route "get_students" & Test GET endpoint with Postman
@app.route('/get_students')
def get_students():
    #Connect to database
    db = db_connection()
    if (db):
        # create "cursor" object to control database, dictionary=True will return objects as dictionaries rather than tuples.
        cursor = db.cursor(dictionary=True)
        
        # write query to get all students
        query = '''
            SELECT *
            FROM students;
        '''
        
        # execute query with cursor
        cursor.execute(query)
        # fetch all objects and store into "students" variable
        students = cursor.fetchall()
        
        # close cursor and connection
        cursor.close()
        db.close()
        
        # serialize and return a jsonifed response of students with 'students_schema.jsonify(students)'
        return students_schema.jsonify(students)
        
        

# Create Route "add_student" & Test POST endpoint with Postman
@app.route('/add_student', methods=['POST'])
def add_student():
    #Connect to database
    db = db_connection()
    # gets our json data
    new_student = request.get_json()
    # validate json with schema
    errors = student_schema.validate(new_student)
    # create conditional based on if errors
    if (errors):
        return jsonify(errors), 404
    # part 3: add student to database
    else:
        # create "cursor" object to control database
        cursor = db.cursor()
        # new_student details
        new_student_details = (new_student['first_name'], new_student['last_name'], new_student['email'], new_student['phone_num'], new_student['start_date'])
        # write query to INSERT INTO students with "%s" placeholders for each entry
        query = '''
            INSERT INTO students (
                first_name,
                last_name,
                email,
                phone_num,
                start_date
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            )
        '''
        
        # execute query with parameterized values
        # NOTE: The second argument must be a tuple or a list with all parameters rather than passing multiple arguments
        cursor.execute(query, new_student_details)
            
        # commit the changes to db
        db.commit()
        
        # close cursor and connection
        cursor.close()
        db.close()
        
        # return jsonfied response
        return jsonify({'message': f'New student: {new_student["first_name"]} was added to the database!'})
           

# create a dynamic route "get_student" to grab specific data
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    #Connect to database
    db = db_connection()
    if (db):
        # create "cursor" object to control database, dictionary=True will return objects as dictionaries rather than tuples.
        cursor = db.cursor(dictionary=True)
        # write query to a single student
        query = f'''
            SELECT *
            FROM students
            WHERE id={student_id}
        '''
        # execute query with cursor
        cursor.execute(query)
        
        # fetch one object and store into "student" variable
        student = cursor.fetchone()
        
        # close cursor and connection
        cursor.close()
        db.close()
        
        if (student):
            # serialize and return a jsonifed response of students with 'student_schema.jsonify(student)'
            return student_schema.jsonify(student)        
        else:
            return jsonify({'message': 'Student not found!'})


# create a dynamic route "update_student"
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    #Connect to database
    db = db_connection()
    # gets our json data
    updated_student = request.get_json()
    # validate json with schema
    errors = student_schema.validate(updated_student)
    # create conditional based on if errors
    if (errors):
        return jsonify(errors), 404
    else:
        # create "cursor" object to control database
        cursor = db.cursor()
        # check if student exists
        query = f'''
            SELECT *
            FROM students
            WHERE id={student_id}
        '''
        # execute query
        cursor.execute(query)
        
        # fetch one student object
        student = cursor.fetchone()
        
        # if we get a valid student object
        if (student):
            # new_student details
            updated_student_details = (updated_student['first_name'], updated_student['last_name'], updated_student['email'], updated_student['phone_num'], updated_student['start_date'])
            
            # write query to INSERT INTO students with "%s" placeholders for each entry
            query = f'''
                UPDATE students
                SET
                    first_name = %s,
                    last_name = %s,
                    email = %s,
                    phone_num = %s,
                    start_date = %s
                WHERE id={student_id}
            '''
            # execute query with parameterized values
            # NOTE: The second argument must be a tuple or a list with all parameters rather than passing multiple arguments
            cursor.execute(query, updated_student_details)
                
            # commit the changes to db
            db.commit()
            # close cursor and connection
            cursor.close()
            db.close()
            
            # return jsonfied response
            return jsonify({'message': f'{updated_student["first_name"]} has been updated!'})
        else:
            return jsonify({'message': 'Student not found!'})    

# create dynamic route "delete_student"
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    #Connect to database
    db = db_connection()
    if (db):
        # create "cursor" object to control database
        cursor = db.cursor()
        # check if student exists
        query = f'''
            SELECT *
            FROM students
            WHERE id={student_id}
        '''
        # execute query
        cursor.execute(query)
        
        # fetch one student object
        student = cursor.fetchone()
        
        # if we get a valid student object
        if (student):
            # write delete query
            query = f'''
                DELETE FROM students
                WHERE id={student_id}
            '''
            
            #execute query
            cursor.execute(query)
                
            # commit the changes to db
            db.commit()
            
            # close cursor and connection
            cursor.close()
            db.close()
            
            # return jsonfied response
            return jsonify({'message': f'Student id: {student_id} has been deleted!'})
        else:
            return jsonify({'message': 'Student not found!'}) 