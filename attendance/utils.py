from django.core.files.storage import FileSystemStorage
import requests
import cognitive_face as CF
import sqlite3
import os
from random import shuffle
import time
import json
from PIL import Image
# from models import Attendance

personGroupId = 'class1'
# Key = 'aad3f5ef6ec94d8fa4e7a77f930c84e1'
Key = 'f1f9523961ba4f6dad267e14d1d24f3f'


BASE_URL = 'https://centralindia.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

def face_api_detect(img_path):
    headers = {'Content-Type': 'application/octet-stream', 
                    'Ocp-Apim-Subscription-Key':'f1f9523961ba4f6dad267e14d1d24f3f'}
    face_api_url = 'https://centralindia.api.cognitive.microsoft.com/face/v1.0/detect?recognitionModel=recognition_02'
 
    data = open(img_path, 'rb')
    response = requests.post(face_api_url , headers=headers, data=data)
    return (response.json())

def face_api_identify(face_ids):
    headers = {'Content-Type': 'application/json', 
                    'Ocp-Apim-Subscription-Key':'f1f9523961ba4f6dad267e14d1d24f3f'}
    face_api_url = 'https://centralindia.api.cognitive.microsoft.com/face/v1.0/identify'

    data = {
        'personGroupId' : personGroupId,
        'faceIds' : face_ids
    }
    json_data = json.dumps(data)

    response = requests.post(face_api_url , headers=headers, data=json_data)
    return (response.json())

def check_for_attendance(filename):
    CF.Key.set(Key)
    connect = sqlite3.connect("db.sqlite3")
    c = connect.cursor()

    img_path = 'media\\' + filename
    # res = CF.face.detect(img_path)
    res = face_api_detect(img_path)
    faceIds = []
    for face in res:
        faceIds.append(face['faceId'])
    # res = CF.face.identify(faceIds, personGroupId)
    res = face_api_identify(faceIds)
    print('######111111111', res, type(res))

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
    print('########', response)
    return response

def put_attendance(filename, subject_name):
    CF.Key.set(Key)
    connect = sqlite3.connect("db.sqlite3")
    c = connect.cursor()

    img_path = 'media\\' + filename
    #Image Pre-processing -- Reducing Size
    image = Image.open(img_path)
    image.save(img_path, quality=80, optimized=True)
    #
    res = face_api_detect(img_path) #Calling Face API for detection
    print('debug->detect',res)
    faceIds = []
    for face in res:
        faceIds.append(face['faceId'])
    res = face_api_identify(faceIds) #Calling Face API for identification
    print('debug->identify',res)
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
            if row[1] is not None and confidence is not None:
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


def get_attendance():
    connect = sqlite3.connect("db.sqlite3")
    c = connect.cursor()
    c.execute("SELECT * FROM Subjects")
    temp_subjects = c.fetchall()
    subjects = []
    for sub in temp_subjects:
        subjects.append(sub[0])
    c.execute("SELECT * FROM Attendance")
    temp_att = c.fetchall()
    attendance = {}
    for names_subs in temp_att:
        temp_list = names_subs[1].split(',')
        attendance[names_subs[0]] = temp_list
    c.execute("SELECT Name FROM Students ORDER BY ID")
    students = c.fetchall()
    response = []
    response.append(attendance)
    response.append(subjects)
    response.append(students)
    return response

def clear_attendance():
    connect = sqlite3.connect("db.sqlite3")
    c = connect.cursor()
    c.execute("DELETE FROM Attendance")
    connect.commit()

def add_person_faces():
    personId = 'd3b0b08c-240f-4786-87d6-cd43aaffdee6'
    headers = {'Content-Type': 'application/octet-stream', 
                    'Ocp-Apim-Subscription-Key':'f1f9523961ba4f6dad267e14d1d24f3f'}
    face_api_url = 'https://centralindia.api.cognitive.microsoft.com/face/v1.0/persongroups/class1/persons/'+ personId +'/persistedFaces'
    
    path = "D:\\code\\innovators-project\\attendace-altered-git\\attendance-face-recog\\dataset\\hruday_new"
    items = os.listdir(path)
    shuffle(items)
    for img_file in items:
        data = open(path + '\\' + img_file, 'rb')
        response = requests.post(face_api_url , headers=headers, data=data)
        time.sleep(3)
        print(img_file)
        print (response.json())

