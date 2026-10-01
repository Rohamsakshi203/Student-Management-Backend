from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2


app = FastAPI()

connection = psycopg2.connect(
    host='localhost',
    port='5432',
    database='postgres',
    user='postgres',
    password='Sakshi@123'
)

cursor = connection.cursor()


# Student model for POST request
class Student(BaseModel):
    id: int
    name: str
    course: str


# Get all students
@app.get('/students')
def get_all_students():

    cursor.execute('SELECT * FROM students')

    rows = cursor.fetchall()

    # [(101, 'Sakshi Roham', 'AI'), (102, 'Komal', 'React')]

    result = []

    for row in rows:
        result.append({
            'id': row[0],
            'name': row[1],
            'course': row[2]
        })

    return result


# Get single student
@app.get('/students/{id}')
def get_single_student(id: int):

    cursor.execute(
        'SELECT * FROM students WHERE id=%s',
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail='Invalid Student ID'
        )

    return {
        'id': row[0],
        'name': row[1],
        'course': row[2]
    }


# Create student record
@app.post('/students')
def create_student_record(student: Student):
    try:

        cursor.execute(
            'INSERT INTO students (id, name, course) VALUES (%s, %s, %s)',
            (student.id, student.name, student.course)
        )

        connection.commit()
        raise HTTPException(status_code=201, detail='Student Record Created Successfully')
    except psycopg2.IntegrityError:
        connection.rollback()
        raise HTTPException (status_code=404, detail='Student ID Already Exists')

    