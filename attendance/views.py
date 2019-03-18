from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
from attendance.utils import check_for_attendance
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



def home(request):
    return render(request, 'face_rest_api/templates')

# @login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage('media')
        filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        face_info = check_for_attendance(myfile.name)
        response = {
            'faces' : face_info,
            'uploaded_file_url': 'media/' + myfile.name
            # 'uploaded_file_url': myfile.name
            # 'uploaded_file_url': '..\\media\\' + myfile.name
        }
        return render(request, 'upload.html', response)
    return render(request, 'upload.html')

def hex_test(req):
    return render(req, 'hex_test.html')

@csrf_exempt
def andr_file(request):
    file_upload_secret_key = 'hush!It$ a seCreT'
    if request.method == 'POST' and request.FILES['image'] and request.POST['key'] == file_upload_secret_key:
        myfile = request.FILES['image']
        fs = FileSystemStorage('media')
        filename = fs.save(myfile.name, myfile)
        return HttpResponse('File Uploaded')
    return HttpResponse('Bad Request')




