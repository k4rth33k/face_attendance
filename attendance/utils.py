from django.core.files.storage import FileSystemStorage
import requests
import cognitive_face as CF
import sqlite3
# from models import Attendance

personGroupId = 'grp1'

def handle_uploaded_file(f):
    print('handle_uploaded_file')
    fs = FileSystemStorage()
    fs.save(f.name, f)

def face_api_detect(img_path):
    headers = {'Content-Type': 'application/octet-stream', 
                    'Ocp-Apim-Subscription-Key':'aad3f5ef6ec94d8fa4e7a77f930c84e1'}
    face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'
 
    data = open(img_path, 'rb')
    response = requests.post(face_api_url , headers=headers, data=data)
    return (response.json())

def check_for_attendance(filename):
    Key = 'aad3f5ef6ec94d8fa4e7a77f930c84e1'
    CF.Key.set(Key)
    connect = sqlite3.connect("db.sqlite3")
    c = connect.cursor()

    img_path = 'media\\' + filename
    res = CF.face.detect(img_path) 
    faceIds = []
    for face in res:
        faceIds.append(face['faceId'])
    res = CF.face.identify(faceIds, personGroupId)
    # print(res)
    response = []
    for face in res:
        if not face['candidates']:
            response.append(('Unknown',0.0))
            # print('#############################')
        else:
            personId = face['candidates'][0]['personId']
            confidence = face['candidates'][0]['confidence']
            c.execute('SELECT * FROM Students WHERE personID = ?', (personId,))
            row = c.fetchone()
            response.append((row[1], confidence))
            # print('############################')
    print(response)
    return response

def put_attendance(filename, subject_name):
    Key = 'aad3f5ef6ec94d8fa4e7a77f930c84e1'
    CF.Key.set(Key)
    connect = sqlite3.connect("db.sqlite3")
    c = connect.cursor()

    img_path = 'media\\' + filename
    res = CF.face.detect(img_path) 
    faceIds = []
    for face in res:
        faceIds.append(face['faceId'])
    res = CF.face.identify(faceIds, personGroupId)
    # print(res)
    attendance = []
    for face in res:
        if not face['candidates']:
            attendance.append(('Unknown',0.0))
            # print('#############################')
        else:
            personId = face['candidates'][0]['personId']
            confidence = face['candidates'][0]['confidence']
            c.execute('SELECT * FROM Students WHERE personID = ?', (personId,))
            row = c.fetchone()
            attendance.append((row[1], confidence))
            # print('############################')
    att_students = []
    c.execute('SELECT Student FROM Attendance')
    temp_names = c.fetchall()
    for x in temp_names:
        att_students.append(x[0])
    for name_conf in attendance:
        if name_conf[0] not in att_students:
            c.execute("INSERT INTO Attendance VALUES(?,?)", (name_conf[0],subject_name,))
        else:
            c.execute("SELECT Subjects FROM Attendance WHERE Student = ?", (name_conf[0],))
            subjects = c.fetchone()[0]
            subjects += ',' + subject_name
            c.execute("UPDATE Attendance SET Subjects = ? WHERE Student = ?",(subjects,name_conf[0],))
    connect.commit()

    # students = Attendance.objects.get(student_name = 'test')
    # print(students)


def get_attendance():
    connect = sqlite3.connect("db.sqlite3")
    c = connect.cursor()
    c.execute("SELECT * FROM Subjects")
    subjects = c.fetchall()
    c.execute("SELECT * FROM Attendance")
    attendance = c.fetchall()
    response = []
    response.append(attendance)
    response.append(subjects)
    return response