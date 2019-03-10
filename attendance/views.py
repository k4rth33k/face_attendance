from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
from attendance.utils import check_for_attendance

def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage('media')
        filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        face_info = check_for_attendance(myfile.name)
        response = {
            'faces' : face_info,
            'uploaded_file_url': '..\\media\\' + myfile.name
        }

        return render(request, 'upload.html', response)
    return render(request, 'upload.html')

'''
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def upload_file(request):
    if request.method == 'POST':
        # uploaded_file = request.FILES['image_file']
        print(request.FILES['docfile'])
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        # print(uploaded_file.name)   
    return render(request, 'upload.html')

'''

